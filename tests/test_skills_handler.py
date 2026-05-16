"""
Tests for skills handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from handlers.skills import (
    SKILL_CATEGORIES,
    handle_skills,
    handle_reputation,
    handle_depth,
    handle_skills_list,
    _track_skill,
)


class TestSkillsHandler(unittest.TestCase):
    """Tests for /skills, /reputation, /depth commands."""

    def test_skill_categories_not_empty(self):
        self.assertGreater(len(SKILL_CATEGORIES), 5)

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_skills_no_args(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_skills("/skills")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_track_skill_success(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.get_skill_level.return_value = 2
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = _track_skill("sql_injection", "ok")

        self.assertTrue(success)
        mock_state.track_skill.assert_called_once()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_track_skill_failure(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.get_skill_level.return_value = 1
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = _track_skill("xss", "fail")

        self.assertTrue(success)
        mock_state.track_skill.assert_called_once()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_reputation(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.reputation = 150
        mock_state.get_handle.return_value = "Новичок"
        mock_state.HANDLES = [(0, "Новичок"), (100, "Хакер"), (500, "Эксперт")]
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_reputation("/reputation")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_depth_show(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.get_explanation_depth.return_value = "normal"
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_depth("/depth")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_depth_set_beginner(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_depth("/depth beginner")

        self.assertTrue(success)
        mock_state.set_explanation_depth.assert_called_once_with("beginner")
        mock_state.save_to_file.assert_called_once()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_depth_set_expert(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_depth("/depth expert")

        self.assertTrue(success)
        mock_state.set_explanation_depth.assert_called_once_with("expert")

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_depth_invalid(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_depth("/depth invalid")

        self.assertTrue(success)
        mock_state.set_explanation_depth.assert_not_called()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_skills_list_empty(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.get_all_skills.return_value = []
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_skills_list("/skills")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.skills.get_state")
    @patch("handlers.skills.console")
    def test_handle_skills_list_with_skills(self, mock_console, mock_get_state):
        mock_state = MagicMock()
        mock_state.get_all_skills.return_value = [
            {"name": "sql_injection", "level": 3, "xp": 45, "success_rate": 80, "attempts": 5},
            {"name": "xss", "level": 2, "xp": 30, "success_rate": 60, "attempts": 3},
        ]
        mock_get_state.return_value = mock_state

        success, _, _, continue_loop = handle_skills_list("/skills")

        self.assertTrue(success)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
