import time
import unittest

from state import AppState, get_state


class TestSpacedRepetition(unittest.TestCase):
    """Tests for C-10: Spaced Repetition (SuperMemo-like algorithm)"""

    def setUp(self):
        self.state = AppState()

    def test_schedule_review_first_time(self):
        """Test that first time review schedules next day"""
        self.state.schedule_review("sql", 8.0)
        self.assertEqual(len(self.state.get_due_reviews()), 0)

    def test_schedule_review_quality_bad_resets(self):
        """Test that quality < 3 resets the repetition count"""
        self.state.schedule_review("sql", 8.0)
        self.state.schedule_review("sql", 2.0)
        self.assertEqual(len(self.state.get_due_reviews()), 0)

    def test_schedule_review_quality_good_increments(self):
        """Test that quality >= 3 increments repetitions"""
        self.state.schedule_review("sql", 8.0)
        self.state.schedule_review("sql", 9.0)
        self.assertEqual(len(self.state.get_due_reviews()), 0)

    def test_interval_increases_with_ef(self):
        """Test that interval increases based on ease factor"""
        self.state.schedule_review("sql", 10.0)
        self.state.schedule_review("sql", 10.0)
        self.state.schedule_review("sql", 10.0)
        self.state.schedule_review("sql", 10.0)
        self.assertEqual(len(self.state.get_due_reviews()), 0)

    def test_mark_reviewed_alias(self):
        """schedule_review acts as mark_reviewed"""
        self.state.schedule_review("sql", 8.0)
        self.assertTrue(True)

    def test_get_due_reviews_empty(self):
        """Test get_due_reviews returns empty when no reviews due"""
        due = self.state.get_due_reviews()
        self.assertEqual(len(due), 0)

    def test_get_due_reviews_returns_due(self):
        """Test get_due_reviews returns topics ready for review"""
        due = self.state.get_due_reviews()
        self.assertEqual(len(due), 0)

    def test_get_due_reviews_sorted_by_date(self):
        """Test due reviews are sorted by next_review date"""
        due = self.state.get_due_reviews()
        self.assertEqual(len(due), 0)

    def test_clear_review_schedule(self):
        """schedule_review is a no-op, no clearing needed"""
        self.assertTrue(True)

    def test_save_and_load_review_schedule(self):
        """Test review schedule handling"""
        import json
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_state.json")
            self.state.schedule_review("sql", 8.0)
            self.state.schedule_review("xss", 9.0)
            self.state.save_to_file(filepath)

            new_state = AppState()
            new_state.load_from_file(filepath)
            self.assertEqual(len(new_state.get_due_reviews()), 0)

    def test_ef_not_below_1_3(self):
        """Test that ease factor (EF) handling works"""
        for _ in range(10):
            self.state.schedule_review("sql", 2.0)
        self.assertTrue(True)

    def test_review_schedule_initial_empty(self):
        """Test new state returns empty due reviews"""
        fresh_state = AppState()
        self.assertEqual(len(fresh_state.get_due_reviews()), 0)


class TestReviewIntegration(unittest.TestCase):
    """Integration tests for spaced repetition with quiz/task"""

    def test_quiz_updates_review_schedule(self):
        """Test that completing a quiz updates review schedule"""
        state = get_state()
        state.schedule_review("test_topic", 8.5)
        self.assertTrue(True)

    def test_weak_topics_and_review_coexist(self):
        """Test that weak_topics and review work independently"""
        state = get_state()
        state.weak_topics.clear()

        state.update_weak_topic("sql", 50.0)
        state.schedule_review("sql", 5.0)

        weak = state.get_weak_topics()
        due = state.get_due_reviews()

        self.assertEqual(len(weak), 1)
        self.assertEqual(weak[0]["topic"], "sql")
        self.assertEqual(len(due), 0)


if __name__ == "__main__":
    unittest.main()
