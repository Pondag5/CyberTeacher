"""
Integration test for analytics handler.
Tests the analytics computation and AI recommendation flow.
"""

import unittest
from unittest.mock import patch, MagicMock

from di import get_context
from handlers.analytics import handle_analytics, _compute_learning_metrics


class TestAnalyticsIntegration(unittest.TestCase):
    """Integration test for analytics handler."""

    def setUp(self):
        """Set up a fresh context with mock state."""
        self.state_patch = patch("handlers.analytics.get_context")
        self.mock_get_context = self.state_patch.start()
        self.mock_state = MagicMock()
        self.mock_state.points = 1500
        self.mock_state.quizzes_taken = 15
        self.mock_state.labs_started = 8
        self.mock_state.missions_completed = 3
        self.mock_state.total_flags_collected = 25
        self.mock_state.assignments_completed = 5
        self.mock_state.tracks_enrolled = ["web_fundamentals", "network_security"]
        weak_topics_data = [
            {"topic": "SQL Injection", "success_rate": 45.0, "attempts": 10},
            {"topic": "XSS", "success_rate": 60.0, "attempts": 5},
        ]
        self.mock_state.weak_topics = weak_topics_data
        self.mock_state.get_weak_topics = MagicMock(
            return_value=[wt for wt in weak_topics_data if wt["success_rate"] < 70.0]
        )
        self.mock_state.bounty_reports = []
        self.mock_ctx = MagicMock()
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

        # Mock the LLM for AI recommendations
        self.llm_patch = patch("handlers.analytics.get_llm")
        self.mock_get_llm = self.llm_patch.start()
        self.mock_llm = MagicMock()
        self.mock_get_llm.return_value = self.mock_llm
        self.mock_llm_response = MagicMock()
        self.mock_llm_response.content = (
            "Focus on SQLi and XSS. Practice with labs and quizzes."
        )
        self.mock_llm.invoke.return_value = self.mock_llm_response

    def tearDown(self):
        self.state_patch.stop()
        self.llm_patch.stop()

    def test_compute_learning_metrics(self):
        """Test that metrics are computed correctly from state."""
        metrics = _compute_learning_metrics(self.mock_state)

        # Check basic metrics
        self.assertEqual(metrics["total_xp"], 1500)
        self.assertEqual(metrics["quizzes_taken"], 15)
        self.assertEqual(metrics["labs_started"], 8)
        self.assertEqual(metrics["missions_completed"], 3)
        self.assertEqual(metrics["flags_collected"], 25)
        self.assertEqual(metrics["assignments_completed"], 5)
        self.assertEqual(metrics["tracks_enrolled"], 2)
        self.assertEqual(metrics["weak_topics_count"], 2)
        self.assertEqual(metrics["bounty_reports"], 0)

        # Check computed metrics
        self.assertAlmostEqual(metrics["avg_weak_success"], 52.5)  # (45+60)/2

    def test_analytics_handler_flow(self):
        """Test the full analytics handler flow."""
        success, _, output, _ = handle_analytics("analytics", "")
        self.assertTrue(success)

        # Check that output contains key sections
        self.assertIn("Advanced Analytics", output)
        self.assertIn("Overview:", output)
        self.assertIn("Total XP: [cyan]1500[/cyan]", output)
        self.assertIn("SQL Injection", output)
        self.assertIn("45.0%", output)
        self.assertIn("XSS", output)
        self.assertIn("60.0%", output)
        self.assertIn("AI Tutor", output)
        self.assertIn("Focus on SQLi and XSS", output)


if __name__ == "__main__":
    unittest.main()
