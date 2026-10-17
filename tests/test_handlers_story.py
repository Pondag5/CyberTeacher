"""Unit tests for story_mode.py (selected functions)"""

import unittest
from unittest.mock import MagicMock, patch

from story_mode import (
    get_level,
    get_story_list,
    start_story_mode,
    submit_flag,
)


class TestGetLevel(unittest.TestCase):
    def test_get_level_script_kiddie(self):
        self.assertEqual(get_level(0), "Script Kiddie")
        self.assertEqual(get_level(50), "Script Kiddie")

    def test_get_level_hacker(self):
        self.assertEqual(get_level(100), "Hacker")
        self.assertEqual(get_level(150), "Hacker")

    def test_get_level_penetration_tester(self):
        self.assertEqual(get_level(300), "Penetration Tester")
        self.assertEqual(get_level(500), "Penetration Tester")

    def test_get_level_security_expert(self):
        self.assertEqual(get_level(600), "Security Expert")
        self.assertEqual(get_level(999), "Security Expert")

    def test_get_level_master_hacker(self):
        self.assertEqual(get_level(1000), "Master Hacker")
        self.assertEqual(get_level(1500), "Master Hacker")

    def test_get_level_legend(self):
        self.assertEqual(get_level(2000), "Legend")
        self.assertEqual(get_level(5000), "Legend")


class TestStartStoryMode(unittest.TestCase):
    @patch("story_mode.get_state")
    def test_start_story_mode_returns_string(self, mock_get_state):
        mock_state = MagicMock()
        mock_state.xp = 0
        mock_state.story_completed = []
        mock_get_state.return_value = mock_state
        result = start_story_mode(1)
        self.assertIsInstance(result, str)
        self.assertIn("ЭПИЗОД #1", result)


class TestSubmitFlag(unittest.TestCase):
    @patch("story_mode.get_state")
    def test_submit_invalid_flag(self, mock_get_state):
        mock_state = MagicMock()
        mock_state.xp = 0
        mock_state.story_completed = []
        mock_get_state.return_value = mock_state
        result = submit_flag("WRONG_FLAG")
        self.assertIn("Неверный флаг", result)

    @patch("story_mode.get_state")
    def test_submit_valid_flag(self, mock_get_state):
        mock_state = MagicMock()
        mock_state.xp = 0
        mock_state.story_completed = []
        mock_get_state.return_value = mock_state
        result = submit_flag("FLAG{SQL_1nj3ct10n}")
        self.assertIn("ПРОЙДЕН", result)
        self.assertIn(1, mock_state.story_completed)


class TestGetStoryList(unittest.TestCase):
    @patch("story_mode.get_state")
    def test_get_story_list_returns_string(self, mock_get_state):
        mock_state = MagicMock()
        mock_state.xp = 0
        mock_state.story_completed = []
        mock_get_state.return_value = mock_state
        result = get_story_list()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        self.assertIn("Первое", result)
        self.assertIn("XSS", result)


if __name__ == "__main__":
    unittest.main()
