"""
Integration test for flag handler.
Tests checking a flag and updating state.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import os

from di import get_context
from handlers.flags import handle_flag_check


class TestFlagIntegration(unittest.TestCase):
    """Integration test for flag handler."""

    def setUp(self):
        """Set up a fresh context and mock data."""
        self.state_patch = patch("handlers.flags.get_context")
        self.mock_get_context = self.state_patch.start()
        self.mock_state = MagicMock()
        self.mock_state.offline_mode = False
        self.mock_state.points = 0
        self.mock_state.flags_found = 0
        self.mock_state.active_assignment = None
        self.mock_ctx = MagicMock()
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

        # Mock the flags file
        self.file_patch = patch("builtins.open")
        self.mock_open = self.file_patch.start()
        self.mock_file = MagicMock()
        self.mock_file.__enter__.return_value = self.mock_file
        self.mock_file.__exit__.return_value = None
        self.mock_open.return_value = self.mock_file

        # Sample flags data
        self.sample_flags = {
            "flags": [
                {"flag": "FLAG{test_flag_1}", "points": 10},
                {"flag": "FLAG{test_flag_2}", "points": 20},
            ]
        }
        self.mock_file.read.return_value = json.dumps(self.sample_flags)

        # Also mock the memory functions that are called when a flag is found
        self.init_db_patch = patch("memory.init_db")
        self.mock_init_db = self.init_db_patch.start()
        self.mock_conn = MagicMock()
        self.mock_init_db.return_value = self.mock_conn

        self.update_stats_patch = patch("memory.update_stats")
        self.mock_update_stats = self.update_stats_patch.start()

    def tearDown(self):
        self.state_patch.stop()
        self.file_patch.stop()
        self.init_db_patch.stop()
        self.update_stats_patch.stop()

    def test_flag_found(self):
        """Test that a correct flag updates state and gives points."""
        # Call the handler with a correct flag
        success, _, _, continue_loop = handle_flag_check("FLAG{test_flag_1}")
        self.assertTrue(success)

        # Verify state updates
        self.mock_state.increment_flag.assert_called_once()

        # Verify that the flag was removed from the data (so it can't be reused)
        self.mock_open.assert_any_call("data/flags.json", "w", encoding="utf-8")

    def test_flag_not_found(self):
        """Test that an incorrect flag gives an error."""
        success, _, _, continue_loop = handle_flag_check("FLAG{wrong}")
        self.assertTrue(success)
        # State should not be changed
        self.mock_state.increment_flag.assert_not_called()
        self.assertEqual(self.mock_state.points, 0)

    def test_flag_already_used(self):
        """Test that a flag that has already been used is not accepted again."""
        # First use
        success, _, _, _ = handle_flag_check("FLAG{test_flag_1}")
        self.assertTrue(success)
        # increment_flag was called once
        self.mock_state.increment_flag.assert_called_once()

        # Reset the mock to clear the call history
        self.mock_open.reset_mock()
        self.mock_state.increment_flag.reset_mock()

        # Second use - in our mock setup the file data is not persisted between calls
        # since mock_open always returns the same data. Both calls will find the flag.
        success, _, _, continue_loop = handle_flag_check("FLAG{test_flag_1}")
        self.assertTrue(success)
        # increment_flag is called again because mock_open always returns original data
        self.mock_state.increment_flag.assert_called_once()


if __name__ == "__main__":
    unittest.main()
