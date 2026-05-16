"""
Tests for missions handler.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from handlers.missions import (
    _load_mission,
    _list_missions,
    _start_mission,
    _submit_mission,
    handle_missions,
)


class TestMissionsHandler(unittest.TestCase):
    """Tests for /missions command handler."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.patcher = patch("handlers.missions.MISSIONS_DIR", self.tmpdir.name)
        self.patcher.start()

        # Create a test mission
        self.test_mission = {
            "id": "test_mission",
            "title": "Test Mission",
            "description": "A test mission",
            "category": "web",
            "difficulty": 2,
            "xp_reward": 100,
            "labs": ["lab1"],
            "steps": [
                {"order": 1, "objective": "Step 1", "hint": "Hint 1", "flag": "FLAG{test}"},
                {"order": 2, "objective": "Step 2", "hint": "Hint 2", "flag": "FLAG{test2}"},
            ],
        }
        path = os.path.join(self.tmpdir.name, "test_mission.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.test_mission, f)

    def tearDown(self):
        self.patcher.stop()
        self.tmpdir.cleanup()

    def test_load_mission_exists(self):
        result = _load_mission("test_mission")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "test_mission")

    def test_load_mission_not_exists(self):
        result = _load_mission("nonexistent")
        self.assertIsNone(result)

    @patch("handlers.missions.get_state")
    @patch("handlers.missions.console")
    def test_list_missions(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.missions_completed = []
        mock_get_state.return_value = mock_state

        _list_missions()
        mock_console.print.assert_called()

    @patch("handlers.missions.get_state")
    @patch("handlers.missions.console")
    def test_start_mission(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.missions_completed = []
        mock_get_state.return_value = mock_state

        result = _start_mission("test_mission")

        self.assertEqual(mock_state.active_mission, "test_mission")
        self.assertEqual(mock_state.hints_used, 0)

    @patch("handlers.missions.get_state")
    @patch("handlers.missions.console")
    def test_start_mission_not_found(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        result = _start_mission("nonexistent")

        self.assertIn("не найдена", result)

    @patch("handlers.missions.get_state")
    @patch("handlers.missions.console")
    def test_submit_mission_success(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.missions_completed = []
        mock_state.exploit_success = []
        mock_state.points = 0
        mock_get_state.return_value = mock_state

        result = _submit_mission("test_mission")

        self.assertIn("завершена", result)
        self.assertIn("test_mission", mock_state.missions_completed)
        mock_state.save_to_file.assert_called_once()

    @patch("handlers.missions.get_state")
    @patch("handlers.missions.console")
    def test_submit_mission_already_completed(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.missions_completed = ["test_mission"]
        mock_get_state.return_value = mock_state

        result = _submit_mission("test_mission")

        self.assertIn("уже завершена", result)

    @patch("handlers.missions.get_state")
    @patch("handlers.missions.console")
    def test_submit_mission_not_found(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        result = _submit_mission("nonexistent")

        self.assertIn("не найдена", result)

    @patch("handlers.missions.console")
    def test_handle_missions_no_args(self, mock_console):
        success, _, _, continue_loop = handle_missions("/missions")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.missions.console")
    def test_handle_missions_invalid_cmd(self, mock_console):
        success, _, _, continue_loop = handle_missions("/mission invalid")

        self.assertTrue(success)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
