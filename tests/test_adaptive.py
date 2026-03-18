import unittest
import tempfile
import os
import json
from state import AppState, get_state

class TestAdaptiveLearning(unittest.TestCase):
    """Tests for C-09: Adaptive Learning Plan"""
    
    def setUp(self):
        """Create fresh state for each test"""
        self.state = AppState()
        self.state.weak_topics = []  # Reset
    
    def test_update_weak_topic_creates_new_entry(self):
        """Test that update_weak_topic creates a new entry for unknown topic"""
        self.state.update_weak_topic("sql", 8.0, 10.0)
        self.assertEqual(len(self.state.weak_topics), 1)
        entry = self.state.weak_topics[0]
        self.assertEqual(entry["topic"], "sql")
        self.assertEqual(entry["attempts"], 1)
        self.assertEqual(entry["total_score"], 8.0)
        self.assertEqual(entry["max_score"], 10.0)
        self.assertAlmostEqual(entry["success_rate"], 80.0)
    
    def test_update_weak_topic_updates_existing(self):
        """Test that update_weak_topic accumulates stats for existing topic"""
        self.state.update_weak_topic("sql", 5.0, 10.0)
        self.state.update_weak_topic("sql", 7.0, 10.0)
        self.assertEqual(len(self.state.weak_topics), 1)
        entry = self.state.weak_topics[0]
        self.assertEqual(entry["attempts"], 2)
        self.assertEqual(entry["total_score"], 12.0)
        self.assertEqual(entry["max_score"], 20.0)
        self.assertAlmostEqual(entry["success_rate"], 60.0)
    
    def test_update_weak_topic_multiple_topics(self):
        """Test multiple topics tracked independently"""
        self.state.update_weak_topic("sql", 5, 10)
        self.state.update_weak_topic("xss", 8, 10)
        self.state.update_weak_topic("sql", 9, 10)
        self.assertEqual(len(self.state.weak_topics), 2)
        sql_entry = next(e for e in self.state.weak_topics if e["topic"] == "sql")
        xss_entry = next(e for e in self.state.weak_topics if e["topic"] == "xss")
        self.assertEqual(sql_entry["attempts"], 2)
        self.assertEqual(sql_entry["success_rate"], 70.0)
        self.assertEqual(xss_entry["attempts"], 1)
        self.assertEqual(xss_entry["success_rate"], 80.0)
    
    def test_get_weak_topics_filters_by_threshold(self):
        """Test get_weak_topics returns only topics below threshold"""
        self.state.update_weak_topic("sql", 50, 100)   # 50%
        self.state.update_weak_topic("xss", 80, 100)   # 80%
        self.state.update_weak_topic("network", 65, 100)  # 65%
        
        weak = self.state.get_weak_topics(threshold=70.0)
        self.assertEqual(len(weak), 2)
        topics = [e["topic"] for e in weak]
        self.assertIn("sql", topics)
        self.assertIn("network", topics)
        self.assertNotIn("xss", topics)
    
    def test_get_weak_topics_sorted_by_success_rate(self):
        """Test get_weak_topics returns weakest first"""
        self.state.update_weak_topic("sql", 30, 100)
        self.state.update_weak_topic("xss", 50, 100)
        self.state.update_weak_topic("network", 40, 100)
        
        weak = self.state.get_weak_topics()
        self.assertEqual(weak[0]["topic"], "sql")
        self.assertEqual(weak[1]["topic"], "network")
        self.assertEqual(weak[2]["topic"], "xss")
    
    def test_get_next_weak_topic_returns_weakest(self):
        """Test get_next_weak_topic returns weakest topic"""
        self.state.update_weak_topic("sql", 30, 100)
        self.state.update_weak_topic("xss", 50, 100)
        next_topic = self.state.get_next_weak_topic()
        self.assertEqual(next_topic, "sql")
    
    def test_get_next_weak_topic_returns_none_when_all_good(self):
        """Test get_next_weak_topic returns None when all topics above threshold"""
        self.state.update_weak_topic("sql", 80, 100)
        self.state.update_weak_topic("xss", 90, 100)
        next_topic = self.state.get_next_weak_topic(threshold=70.0)
        self.assertIsNone(next_topic)
    
    def test_clear_weak_topics(self):
        """Test clear_weak_topics removes all entries"""
        self.state.update_weak_topic("sql", 50, 100)
        self.state.update_weak_topic("xss", 60, 100)
        self.assertEqual(len(self.state.weak_topics), 2)
        self.state.clear_weak_topics()
        self.assertEqual(len(self.state.weak_topics), 0)
    
    def test_save_and_load_weak_topics(self):
        """Test weak_topics persistence in JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_state.json")
            
            # Create and save state
            self.state.update_weak_topic("sql", 75, 100)
            self.state.update_weak_topic("xss", 60, 100)
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
    
    def test_update_weak_topic_zero_max_score(self):
        """Test update handles zero max_score gracefully"""
        self.state.update_weak_topic("sql", 0, 0)
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
        from state import get_state
        
        # Ensure state has no weak topics
        state = get_state()
        state.clear_weak_topics()
        
        # Call handler - should not raise
        result = handle_adaptive("adaptive")
        self.assertEqual(result, (True, None, None, True))
    
    def test_handle_adaptive_with_weak_topics(self):
        """Test /adaptive displays weak topics correctly"""
        from handlers.misc import handle_adaptive
        from state import get_state
        
        state = get_state()
        state.clear_weak_topics()
        state.update_weak_topic("sql", 50.0, 100.0)
        state.update_weak_topic("xss", 60.0, 100.0)
        
        result = handle_adaptive("adaptive")
        self.assertEqual(result, (True, None, None, True))

if __name__ == '__main__':
    unittest.main()