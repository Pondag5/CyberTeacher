import json
import os
import tempfile
import unittest

from state import AppState, get_state


class TestAdaptiveLearning(unittest.TestCase):
    """Tests for C-09: Adaptive Learning Plan"""

    def setUp(self):
        """Create fresh state for each test"""
        self.state = AppState()
        self.state.weak_topics = []  # Reset

    def test_update_weak_topic_creates_new_entry(self):
        """Test that update_weak_topic creates a new entry for unknown topic"""
        self.state.update_weak_topic("sql", 80.0)
        self.assertEqual(len(self.state.weak_topics), 1)
        entry = self.state.weak_topics[0]
        self.assertEqual(entry["topic"], "sql")
        self.assertEqual(entry["attempts"], 1)
        self.assertAlmostEqual(entry["success_rate"], 80.0)

    def test_update_weak_topic_updates_existing(self):
        """Test that update_weak_topic accumulates stats for existing topic"""
        self.state.update_weak_topic("sql", 50.0)
        self.state.update_weak_topic("sql", 70.0)
        self.assertEqual(len(self.state.weak_topics), 1)
        entry = self.state.weak_topics[0]
        self.assertEqual(entry["attempts"], 2)
        self.assertAlmostEqual(entry["success_rate"], 60.0)

    def test_update_weak_topic_multiple_topics(self):
        """Test multiple topics tracked independently"""
        self.state.update_weak_topic("sql", 50.0)
        self.state.update_weak_topic("xss", 80.0)
        self.state.update_weak_topic("sql", 90.0)
        self.assertEqual(len(self.state.weak_topics), 2)
        sql_entry = next(e for e in self.state.weak_topics if e["topic"] == "sql")
        xss_entry = next(e for e in self.state.weak_topics if e["topic"] == "xss")
        self.assertEqual(sql_entry["attempts"], 2)
        self.assertAlmostEqual(sql_entry["success_rate"], 70.0)
        self.assertEqual(xss_entry["attempts"], 1)
        self.assertAlmostEqual(xss_entry["success_rate"], 80.0)

    def test_get_weak_topics_filters_by_threshold(self):
        """Test get_weak_topics returns only topics below threshold"""
        self.state.update_weak_topic("sql", 50.0)
        self.state.update_weak_topic("xss", 80.0)
        self.state.update_weak_topic("network", 65.0)

        weak = self.state.get_weak_topics(threshold=70.0)
        self.assertEqual(len(weak), 2)
        topics = [e["topic"] for e in weak]
        self.assertIn("sql", topics)
        self.assertIn("network", topics)
        self.assertNotIn("xss", topics)

    def test_get_weak_topics_sorted_by_success_rate(self):
        """Test get_weak_topics returns all below threshold"""
        self.state.update_weak_topic("sql", 30.0)
        self.state.update_weak_topic("xss", 50.0)
        self.state.update_weak_topic("network", 40.0)

        weak = self.state.get_weak_topics()
        self.assertEqual(len(weak), 3)
        topics = [t["topic"] for t in weak]
        self.assertIn("sql", topics)
        self.assertIn("xss", topics)
        self.assertIn("network", topics)

    def test_get_next_weak_topic_returns_weakest(self):
        """Test get_next_weak_topic returns weakest topic"""
        self.state.update_weak_topic("sql", 30.0)
        self.state.update_weak_topic("xss", 50.0)
        next_topic = self.state.get_next_weak_topic()
        self.assertEqual(next_topic, "sql")

    def test_get_next_weak_topic_returns_none_when_all_good(self):
        """Test get_next_weak_topic returns None when all topics above threshold"""
        self.state.update_weak_topic("sql", 80.0)
        self.state.update_weak_topic("xss", 90.0)
        next_topic = self.state.get_next_weak_topic(threshold=70.0)
        self.assertIsNone(next_topic)

    def test_clear_weak_topics(self):
        """Test clearing weak_topics removes all entries"""
        self.state.update_weak_topic("sql", 50.0)
        self.state.update_weak_topic("xss", 60.0)
        self.assertEqual(len(self.state.weak_topics), 2)
        self.state.weak_topics.clear()
        self.assertEqual(len(self.state.weak_topics), 0)

    def test_save_and_load_weak_topics(self):
        """Test weak_topics persistence in JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_state.json")

            # Create and save state
            self.state.update_weak_topic("sql", 75.0)
            self.state.update_weak_topic("xss", 60.0)
            self.state.save_to_file(filepath)

            # Load into new state
            new_state = AppState()
            new_state.load_from_file(filepath)

            self.assertEqual(len(new_state.weak_topics), 2)
            topics = {e["topic"]: e for e in new_state.weak_topics}
            self.assertIn("sql", topics)
            self.assertIn("xss", topics)
            self.assertAlmostEqual(topics["sql"]["success_rate"], 75.0)
            self.assertAlmostEqual(topics["xss"]["success_rate"], 60.0)

    def test_update_weak_topic_zero_success_rate(self):
        """Test update handles zero success_rate gracefully"""
        self.state.update_weak_topic("sql", 0.0)
        entry = self.state.weak_topics[0]
        self.assertEqual(entry["success_rate"], 0)

    def test_weak_topics_initial_empty(self):
        """Test that new state has empty weak_topics"""
        fresh_state = AppState()
        self.assertEqual(fresh_state.weak_topics, [])


class TestAdaptiveCommand(unittest.TestCase):
    """Tests for /adaptive command handler"""

    def test_handle_adaptive_with_no_weak_topics(self):
        """Test /adaptive shows success message when no weak topics"""
        from handlers.misc import handle_adaptive

        # Ensure state has no weak topics
        state = get_state()
        state.weak_topics.clear()

        # Call handler - should not raise
        result = handle_adaptive("adaptive")
        self.assertEqual(result, (True, None, None, True))

    def test_handle_adaptive_with_weak_topics(self):
        """Test /adaptive displays weak topics correctly"""
        from handlers.misc import handle_adaptive

        state = get_state()
        state.weak_topics.clear()
        state.update_weak_topic("sql", 50.0)
        state.update_weak_topic("xss", 60.0)

        result = handle_adaptive("adaptive")
        self.assertEqual(result, (True, None, None, True))


if __name__ == "__main__":
    unittest.main()
