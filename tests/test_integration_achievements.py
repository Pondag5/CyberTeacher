"""
Integration test for achievements handler.
Tests earning an achievement and updating state.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import os

from di import get_context
from handlers.achievements import handle_achievements


class TestAchievementsIntegration(unittest.TestCase):
    """Integration test for achievements handler."""

    def setUp(self):
        """Set up a fresh context and mock data."""
        self.state_patch = patch("handlers.achievements.get_context")
        self.mock_get_context = self.state_patch.start()
        self.mock_state = MagicMock()
        self.mock_state.earned_achievements = []
        self.mock_state.points = 0
        self.mock_ctx = MagicMock()
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

        # Mock the achievements file
        self.file_patch = patch("builtins.open")
        self.mock_open = self.file_patch.start()
        self.mock_file = MagicMock()
        self.mock_file.__enter__.return_value = self.mock_file
        self.mock_file.__exit__.return_value = None
        self.mock_open.return_value = self.mock_file

        # Sample achievements data
        self.sample_data = {
            "achievements": [
                {
                    "id": "first_blood",
                    "name": "First Blood",
                    "description": "Get your first flag",
                    "icon": "🩸",
                    "points": 10,
                },
                {
                    "id": "explorer",
                    "name": "Explorer",
                    "description": "Find 10 flags",
                    "icon": "🔍",
                    "points": 50,
                },
            ]
        }
        self.mock_file.read.return_value = json.dumps(self.sample_data)

    def tearDown(self):
        self.state_patch.stop()
        self.file_patch.stop()

    def test_earn_achievement(self):
        """Test earning an achievement updates state and console output."""
        # Call the handler to earn the first achievement
        success, _, _, continue_loop = handle_achievements(
            "/achievements earn first_blood"
        )
        self.assertTrue(success)

        # Verify state was updated
        self.assertIn("first_blood", self.mock_state.earned_achievements)
        self.assertEqual(self.mock_state.points, 10)

        # Ensure the achievement can't be earned again
        self.mock_state.earned_achievements = ["first_blood"]
        success2, _, _, _ = handle_achievements("/achievements earn first_blood")
        self.assertTrue(success2)

    def test_list_achievements(self):
        """Test listing achievements shows correct info."""
        from handlers.achievements import handle_achievements

        success, _, _, continue_loop = handle_achievements("/achievements")
        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
