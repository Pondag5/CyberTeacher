import time
import unittest

from state import AppState, get_state


class TestSpacedRepetition(unittest.TestCase):
    """Tests for C-10: Spaced Repetition (SuperMemo-like algorithm)"""

    def setUp(self):
        self.state = AppState()
        self.state.review_schedule = {}

    def test_schedule_review_first_time(self):
        """Test that first time review schedules next day"""
        self.state.schedule_review("sql", 8.0, 10.0)
        self.assertIn("sql", self.state.review_schedule)
        entry = self.state.review_schedule["sql"]
        self.assertEqual(entry["repetitions"], 0)
        self.assertEqual(entry["interval"], 1)
        self.assertAlmostEqual(
            entry["next_review"], self.state._compute_next_review(1), places=1
        )
        self.assertEqual(entry["ef"], 2.5)

    def test_schedule_review_quality_bad_resets(self):
        """Test that quality < 3 resets the repetition count"""
        self.state.schedule_review("sql", 8.0, 10.0)  # First, quality 4
        entry1 = self.state.review_schedule["sql"]
        self.assertEqual(entry1["repetitions"], 0)

        # Simulate bad review
        self.state.schedule_review("sql", 2.0, 10.0)  # quality 1
        entry2 = self.state.review_schedule["sql"]
        self.assertEqual(entry2["repetitions"], 0)
        self.assertEqual(entry2["interval"], 1)

    def test_schedule_review_quality_good_increments(self):
        """Test that quality >= 3 increments repetitions"""
        self.state.schedule_review("sql", 8.0, 10.0)  # quality 4
        entry1 = self.state.review_schedule["sql"]
        self.assertEqual(entry1["repetitions"], 0)

        self.state.schedule_review("sql", 9.0, 10.0)  # quality 4.5
        entry2 = self.state.review_schedule["sql"]
        self.assertEqual(entry2["repetitions"], 1)
        self.assertEqual(entry2["interval"], 1)  # First increment: 1 day

    def test_interval_increases_with_ef(self):
        """Test that interval increases based on ease factor"""
        self.state.schedule_review("sql", 10.0, 10.0)  # quality 5
        # First: repetitions=0, interval=1
        # Second: repetitions=1, interval=1 (since after 1 it becomes 3)
        # Actually second should be interval=1 and third will increase
        # Let's do three reviews
        self.state.schedule_review("sql", 10.0, 10.0)  # quality 5
        self.state.schedule_review("sql", 10.0, 10.0)  # quality 5 -> repetitions=2
        entry = self.state.review_schedule["sql"]
        # After two successful reviews: repetitions=2, interval should be 3 (day 3)
        self.assertEqual(entry["repetitions"], 2)
        self.assertEqual(entry["interval"], 3)

        # Third review
        self.state.schedule_review("sql", 10.0, 10.0)  # quality 5 -> repetitions=3
        entry = self.state.review_schedule["sql"]
        self.assertEqual(entry["repetitions"], 3)
        # interval should now be increased from 3 * EF (around 7.5)
        self.assertGreater(entry["interval"], 3)

    def test_mark_reviewed_alias(self):
        """Test that mark_reviewed is an alias for schedule_review"""
        self.state.mark_reviewed("sql", 8.0, 10.0)
        self.assertIn("sql", self.state.review_schedule)

    def test_get_due_reviews_empty(self):
        """Test get_due_reviews returns empty when no reviews due"""
        # Schedule a review far in future
        self.state.review_schedule = {
            "sql": {
                "next_review": time.time() + 86400 * 10,
                "interval": 10,
                "repetitions": 2,
            }
        }
        due = self.state.get_due_reviews()
        self.assertEqual(len(due), 0)

    def test_get_due_reviews_returns_due(self):
        """Test get_due_reviews returns topics ready for review"""
        import time

        # Schedule a review in the past (due)
        self.state.review_schedule = {
            "sql": {"next_review": time.time() - 100, "interval": 1, "repetitions": 1},
            "xss": {"next_review": time.time() + 1000, "interval": 1, "repetitions": 1},
        }
        due = self.state.get_due_reviews()
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["topic"], "sql")

    def test_get_due_reviews_sorted_by_date(self):
        """Test due reviews are sorted by next_review date"""
        import time

        now = time.time()
        self.state.review_schedule = {
            "sql": {"next_review": now + 200, "interval": 1, "repetitions": 1},
            "xss": {"next_review": now + 100, "interval": 1, "repetitions": 1},
            "network": {"next_review": now - 50, "interval": 1, "repetitions": 1},
        }
        due = self.state.get_due_reviews()
        self.assertEqual(len(due), 1)  # Only network is due
        self.assertEqual(due[0]["topic"], "network")

    def test_clear_review_schedule(self):
        """Test clearing review schedule"""
        self.state.review_schedule = {
            "sql": {"next_review": time.time(), "interval": 1, "repetitions": 1},
            "xss": {"next_review": time.time(), "interval": 1, "repetitions": 1},
        }
        self.assertEqual(len(self.state.review_schedule), 2)
        self.state.clear_review_schedule()
        self.assertEqual(len(self.state.review_schedule), 0)

    def test_save_and_load_review_schedule(self):
        """Test review_schedule persistence"""
        import json
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_state.json")

            # Create state with review schedule
            self.state.schedule_review("sql", 8.0, 10.0)
            self.state.schedule_review("xss", 9.0, 10.0)
            self.state.save_to_file(filepath)

            # Load into new state
            new_state = AppState()
            new_state.load_from_file(filepath)

            self.assertEqual(len(new_state.review_schedule), 2)
            self.assertIn("sql", new_state.review_schedule)
            self.assertIn("xss", new_state.review_schedule)

    def test_ef_not_below_1_3(self):
        """Test that ease factor (EF) never goes below 1.3"""
        # Simulate bad reviews to try to push EF down
        for _ in range(10):
            self.state.schedule_review("sql", 2.0, 10.0)  # quality 1
        entry = self.state.review_schedule["sql"]
        self.assertGreaterEqual(entry["ef"], 1.3)

    def test_review_schedule_initial_empty(self):
        """Test new state has empty review_schedule"""
        fresh_state = AppState()
        self.assertEqual(fresh_state.review_schedule, {})


class TestReviewIntegration(unittest.TestCase):
    """Integration tests for spaced repetition with quiz/task"""

    def test_quiz_updates_review_schedule(self):
        """Test that completing a quiz updates review schedule"""
        state = get_state()
        initial_count = len(state.review_schedule)

        # Simulate quiz completion by directly calling schedule_review
        topic = "test_topic"
        state.schedule_review(topic, 8.5, 10.0)

        self.assertIn(topic, state.review_schedule)
        self.assertEqual(len(state.review_schedule), initial_count + 1)

    def test_weak_topics_and_review_coexist(self):
        """Test that weak_topics and review_schedule can track same topic independently"""
        state = get_state()
        state.clear_weak_topics()
        state.clear_review_schedule()

        state.update_weak_topic("sql", 50, 100)
        state.schedule_review("sql", 5.0, 10.0)

        weak = state.get_weak_topics()
        # schedule_review sets next_review in the future, so not due immediately
        due = state.get_due_reviews()

        self.assertEqual(len(weak), 1)
        self.assertEqual(weak[0]["topic"], "sql")
        self.assertEqual(
            len(due), 0, "Newly scheduled review should not be immediately due"
        )


if __name__ == "__main__":
    unittest.main()
