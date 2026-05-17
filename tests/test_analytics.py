"""Tests for Advanced Analytics & AI Tutor (M-33)"""

import unittest
from unittest.mock import MagicMock, patch

from state import AppState
from handlers.analytics import (
    handle_analytics,
    _compute_learning_metrics,
    _generate_ai_recommendation,
)


class TestAnalytics(unittest.TestCase):
    """Test analytics handler"""

    def test_compute_metrics_basic(self):
        """Metrics computed from state"""
        mock_state = MagicMock(spec=AppState)
        mock_state.points = 1234.5
        mock_state.quizzes_taken = 5
        mock_state.labs_started = 2
        mock_state.missions_completed = 1
        mock_state.total_flags_collected = 10
        mock_state.assignments_completed = 3
        mock_state.tracks_enrolled = ["t1", "t2"]
        mock_state.weak_topics = []  # raw list
        mock_state.get_weak_topics = MagicMock(return_value=[])

        metrics = _compute_learning_metrics(mock_state)
        self.assertEqual(metrics["total_xp"], 1234.5)
        self.assertEqual(metrics["quizzes_taken"], 5)
        self.assertEqual(metrics["tracks_enrolled"], 2)
        self.assertEqual(metrics["weak_topics_count"], 0)
        self.assertIsNone(metrics["avg_weak_success"])

    def test_compute_metrics_with_weak_topics(self):
        """Weak topics are processed correctly"""
        mock_state = MagicMock(spec=AppState)
        mock_state.points = 100
        mock_state.quizzes_taken = 1
        mock_state.labs_started = 0
        mock_state.missions_completed = 0
        mock_state.total_flags_collected = 0
        mock_state.assignments_completed = 0
        mock_state.tracks_enrolled = []
        weak = [
            {"topic": "SQLi", "success_rate": 45.0, "attempts": 5},
            {"topic": "XSS", "success_rate": 60.0, "attempts": 3},
        ]
        mock_state.get_weak_topics = MagicMock(return_value=weak)
        mock_state.weak_topics = weak  # raw list count

        metrics = _compute_learning_metrics(mock_state)
        self.assertEqual(metrics["weak_topics_count"], 2)
        self.assertEqual(metrics["weak_topics"], weak)
        self.assertAlmostEqual(metrics["avg_weak_success"], 52.5, places=1)

    @patch("handlers.analytics.get_llm")
    def test_generate_ai_recommendation(self, mock_get_llm):
        """AI recommendation calls LLM with proper prompt"""
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "1. Focus on SQLi\n2. Do 5 quizzes\n3. Good luck!"
        mock_llm.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm

        metrics = {
            "total_xp": 500,
            "quizzes_taken": 10,
            "labs_started": 3,
            "missions_completed": 2,
            "flags_collected": 5,
            "assignments_completed": 1,
            "tracks_enrolled": 1,
            "bounty_reports": 0,
            "weak_topics_count": 2,
            "weak_topics": [{"topic": "SQLi", "success_rate": 45.0, "attempts": 5}],
            "avg_weak_success": 45.0,
        }

        rec = _generate_ai_recommendation(metrics)
        self.assertIn("SQLi", rec)  # LLM should mention weak topic
        # Check LLM was called with prompt containing metrics
        call_args = mock_llm.invoke.call_args[0][0]
        self.assertIn("XP: 500", call_args)
        self.assertIn("SQLi", call_args)

    @patch("handlers.analytics.get_llm")
    def test_generate_ai_recommendation_failure(self, mock_get_llm):
        """If LLM fails, returns warning"""
        mock_get_llm.return_value.invoke.side_effect = Exception("LLM down")
        metrics = {
            "total_xp": 0,
            "quizzes_taken": 0,
            "labs_started": 0,
            "missions_completed": 0,
            "flags_collected": 0,
            "assignments_completed": 0,
            "tracks_enrolled": 0,
            "bounty_reports": 0,
            "weak_topics_count": 0,
            "weak_topics": [],
            "avg_weak_success": None,
        }
        rec = _generate_ai_recommendation(metrics)
        self.assertIn("⚠️", rec)

    @patch("handlers.analytics.get_context")
    @patch("handlers.analytics.get_llm")
    def test_handle_analytics_returns_output(self, mock_get_llm, mock_get_context):
        """/analytics returns a formatted output"""
        mock_state = MagicMock(spec=AppState)
        mock_state.points = 500.0
        mock_state.quizzes_taken = 2
        mock_state.labs_started = 1
        mock_state.missions_completed = 0
        mock_state.total_flags_collected = 0
        mock_state.assignments_completed = 0
        mock_state.tracks_enrolled = []  # must be iterable
        mock_state.weak_topics = []
        mock_state.get_weak_topics = MagicMock(return_value=[])
        mock_state.bounty_reports = []  # should be list, not int
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "1. Practice more"
        mock_get_llm.return_value.invoke.return_value = mock_response

        success, msg, _ = handle_analytics("analytics", "")
        self.assertTrue(success)
        self.assertIn("Advanced Analytics", msg)
        self.assertIn("Total XP", msg)
        self.assertIn("500", msg)
        self.assertIn("AI Tutor Recommendation", msg)


if __name__ == "__main__":
    unittest.main()
