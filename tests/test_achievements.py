"""Тесты для обработчика достижений (handlers/achievements.py)"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from handlers.achievements import handle_achievements
from state import get_state


class TestAchievements(unittest.TestCase):
    """Тесты для /achievements"""

    def setUp(self):
        self.state = get_state()
        self.state.earned_achievements = []

    @patch("handlers.achievements.console.print")
    def test_missing_file(self, mock_print):
        # Патчим os.path.exists, чтобы вернуть False
        with patch("handlers.achievements.os.path.exists", return_value=False):
            action_taken, response, extra, is_json = handle_achievements()
        self.assertTrue(action_taken)
        self.assertIsNone(response)
        self.assertTrue(mock_print.called)

    @patch("handlers.achievements.console.print")
    def test_list_all_achievements(self, mock_print):
        data = {
            "achievements": [
                {
                    "id": "ach1",
                    "name": "First Flag",
                    "points": 10,
                    "condition": {"type": "flags_total", "threshold": 1},
                },
                {
                    "id": "ach2",
                    "name": "Quiz Master",
                    "points": 20,
                    "condition": {"type": "quizzes_taken", "threshold": 5},
                },
            ]
        }
        # Создадим временный файл achievements.json
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            tmp_path = f.name
        try:
            with patch("handlers.achievements.os.path.exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=json.dumps(data))):
                    action_taken, response, extra, is_json = handle_achievements()
            self.assertTrue(action_taken)
            self.assertTrue(mock_print.called)
        finally:
            os.unlink(tmp_path)

    @patch("handlers.achievements.console.print")
    def test_shows_earned_achievements(self, mock_print):
        self.state.earned_achievements = ["ach1"]
        data = {
            "achievements": [
                {
                    "id": "ach1",
                    "name": "First Flag",
                    "points": 10,
                    "condition": {"type": "flags_total", "threshold": 1},
                },
                {
                    "id": "ach2",
                    "name": "Second",
                    "points": 20,
                    "condition": {"type": "quizzes_taken", "threshold": 5},
                },
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            tmp_path = f.name
        try:
            with patch("handlers.achievements.os.path.exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=json.dumps(data))):
                    handle_achievements()
            # Ожидаем несколько вызовов print (таблица + возможны дополнительные сообщения)
            self.assertGreaterEqual(mock_print.call_count, 2)
        finally:
            os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main()
