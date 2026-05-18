"""
Tests for missions handler.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from handlers.missions import (
    _list_missions,
    _load_mission,
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

    @patch("handlers.missions.get_context")
    @patch("handlers.missions.console")
    def test_list_missions(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.missions_completed = []
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        _list_missions()
        mock_console.print.assert_called()

    @patch("handlers.missions.get_context")
    @patch("handlers.missions.console")
    def test_start_mission(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.missions_completed = []
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _start_mission("test_mission")

        self.assertEqual(mock_state.active_mission, "test_mission")
        self.assertEqual(mock_state.hints_used, 0)

    @patch("handlers.missions.get_context")
    @patch("handlers.missions.console")
    def test_start_mission_not_found(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _start_mission("nonexistent")

        self.assertIn("не найдена", result)

    @patch("handlers.missions.get_context")
    @patch("handlers.missions.console")
    def test_submit_mission_success(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.missions_completed = []
        mock_state.exploit_success = []
        mock_state.points = 0
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _submit_mission("test_mission")

        self.assertIn("завершена", result)
        self.assertIn("test_mission", mock_state.missions_completed)
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.missions.get_context")
    @patch("handlers.missions.console")
    def test_submit_mission_already_completed(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.missions_completed = ["test_mission"]
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = _submit_mission("test_mission")

        self.assertIn("уже завершена", result)

    @patch("handlers.missions.get_context")
    @patch("handlers.missions.console")
    def test_submit_mission_not_found(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

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
