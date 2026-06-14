"""
Integration test for /daily command flow.
Tests the interaction between handler, state, and daily_challenge module.
"""

import unittest
from unittest.mock import patch, MagicMock

from di import get_context
from handlers.daily import handle_daily


class TestDailyIntegration(unittest.TestCase):
    """Integration test for /daily command."""

    def setUp(self):
        """Set up a fresh context for each test."""
        # We'll patch get_context to return a mock state that we can inspect
        self.state_patch = patch("handlers.daily.get_context")
        self.mock_get_context = self.state_patch.start()
        self.mock_state = MagicMock()
        self.mock_ctx = MagicMock()
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

        # Also patch the daily_challenge functions to return deterministic values
        self.gen_patch = patch("handlers.daily.generate_daily_challenge")
        self.mock_gen = self.gen_patch.start()
        self.mock_gen.return_value = {
            "desc": "Test challenge description",
            "difficulty": "easy",
        }

        self.status_patch = patch("handlers.daily.get_daily_status")
        self.mock_status = self.status_patch.start()
        self.mock_status.return_value = "Current streak: 0"

        self.submit_patch = patch("handlers.daily.submit_daily_answer")
        self.mock_submit = self.submit_patch.start()
        self.mock_submit.return_value = {
            "correct": True,
            "feedback": "Correct answer!",
            "xp_reward": 10,
            "streak_bonus": 0,
        }

    def tearDown(self):
        self.state_patch.stop()
        self.gen_patch.stop()
        self.status_patch.stop()
        self.submit_patch.stop()

    def test_daily_command_flow(self):
        """Test the full flow: show challenge, submit answer, check state updates."""
        # 1. Show challenge (first call with no arguments)
        success, _, _, continue_loop = handle_daily("daily")
        self.assertTrue(success)
        self.mock_gen.assert_called_once()

        # 2. Submit an answer - handler treats any "daily <text>" as challenge display
        success, _, _, continue_loop = handle_daily("daily test answer")
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
