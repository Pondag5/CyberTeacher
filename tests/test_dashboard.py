"""Tests for Learner Dashboard (M-28)"""
# isort: skip_file

import unittest
from unittest.mock import MagicMock, patch

from state import AppState
from handlers.dashboard import handle_dashboard


class TestDashboard(unittest.TestCase):
    """Test the /dashboard command"""

    def _make_state(self):
        """Helper to create a mock state with all required attributes"""
        mock_state = MagicMock(spec=AppState)
        mock_state.points = 100.0
        mock_state.quizzes_taken = 2
        mock_state.labs_started = 1
        mock_state.missions_completed = 0
        mock_state.total_flags_collected = 1
        mock_state.assignments_completed = 0
        mock_state.course_progress = {}
        mock_state.tracks_enrolled = []
        mock_state.track_progress = {}
        mock_state.weak_topics = []
        mock_state.messages_sent = 5
        mock_state.news_checked = 1
        mock_state.get_weak_topics = MagicMock(return_value=[])
        return mock_state

    @patch("handlers.dashboard.get_state")
    def test_dashboard_shows_overview(self, mock_get_state):
        """Dashboard displays key metrics"""
        mock_state = self._make_state()
        mock_state.points = 1234.5
        mock_get_state.return_value = mock_state

        success, msg, _ = handle_dashboard("dashboard", "")
        self.assertTrue(success)
        self.assertIn("Learner Dashboard", msg)
        self.assertIn("Total XP", msg)
        self.assertIn("1234", msg)

    @patch("handlers.dashboard.get_state")
    def test_dashboard_shows_weak_topics(self, mock_get_state):
        """Dashboard displays weak topics when present"""
        mock_state = self._make_state()
        weak = [{"topic": "SQLi", "success_rate": 45.0, "attempts": 3}]
        mock_state.get_weak_topics = MagicMock(return_value=weak)
        mock_get_state.return_value = mock_state

        success, msg, _ = handle_dashboard("dashboard", "")
        self.assertTrue(success)
        self.assertIn("Weak Topics", msg)
        self.assertIn("SQLi", msg)
        self.assertIn("45.0%", msg)

    @patch("handlers.dashboard.get_state")
    def test_dashboard_shows_tracks_progress(self, mock_get_state):
        """Dashboard includes track progress summary"""
        mock_state = self._make_state()
        mock_state.tracks_enrolled = ["test-track"]
        mock_state.track_progress = {
            "test-track": {"completed_topics": ["t1"], "current_topic_idx": 1}
        }
        mock_state.get_weak_topics = MagicMock(return_value=[])
        mock_get_state.return_value = mock_state

        with patch("track_engine.get_track_engine") as mock_engine_func:
            from track_engine import Track, TrackTopic

            mock_track = Track(
                id="test-track",
                name="Test Track",
                description="Test",
                level="beginner",
                topics=[TrackTopic("t1", 1, "T1", ""), TrackTopic("t2", 2, "T2", "")],
            )
            mock_engine = MagicMock()
            mock_engine.get_track.return_value = mock_track
            mock_engine_func.return_value = mock_engine

            success, msg, _ = handle_dashboard("dashboard", "")
            self.assertTrue(success)
            self.assertIn("Learning Tracks", msg)
            self.assertIn("test-track", msg)
            self.assertIn("1/2", msg)

    @patch("handlers.dashboard.get_state")
    def test_dashboard_no_weak_topics_message(self, mock_get_state):
        """Dashboard shows positive message when no weak topics"""
        mock_state = self._make_state()
        mock_state.get_weak_topics = MagicMock(return_value=[])
        mock_get_state.return_value = mock_state

        success, msg, _ = handle_dashboard("dashboard", "")
        self.assertTrue(success)
        self.assertIn("all topics >=70%", msg)


if __name__ == "__main__":
    unittest.main()
