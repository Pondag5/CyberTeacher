"""Тесты для модуля Cross-platform Sync (M-20)."""

import json
import os
import unittest
from unittest.mock import patch

from handlers.sync import (
    handle_sync,
    _export_progress,
    _import_progress,
    _generate_user_id,
)


class TestCrossPlatformSync(unittest.TestCase):
    """Тесты синхронизации."""

    def setUp(self):
        """Настройка тестов."""
        self.test_file = "test_sync.json"

    def tearDown(self):
        """Очистка после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_export_progress(self):
        """Экспорт прогресса."""
        with patch("handlers.sync.console.print"):
            with patch("handlers.sync.get_state") as mock_state:
                mock = mock_state.return_value
                mock.xp = 100
                mock.level = 2
                mock.completed_quizzes = ["quiz1"]
                mock.completed_tasks = []
                mock.weak_topics = ["crypto"]
                mock.achievements = []
                mock.skills = {}
                mock.reputation = 50
                mock.sync_id = "test123"
                success = _export_progress(self.test_file)
                self.assertTrue(success)
                self.assertTrue(os.path.exists(self.test_file))

    def test_import_progress(self):
        """Импорт прогресса."""
        # Сначала создадим файл
        with patch("handlers.sync.console.print"):
            with patch("handlers.sync.get_state") as mock_state:
                mock = mock_state.return_value
                mock.xp = 100
                mock.level = 2
                mock.completed_quizzes = ["quiz1"]
                mock.completed_tasks = []
                mock.weak_topics = ["crypto"]
                mock.achievements = []
                mock.skills = {}
                mock.reputation = 50
                mock.sync_id = "test123"
                _export_progress(self.test_file)

        # Теперь импортируем
        with patch("handlers.sync.console.print"):
            with patch("handlers.sync.get_state") as mock_state:
                mock = mock_state.return_value
                mock.xp = 0
                mock.level = 1
                mock.completed_quizzes = []
                mock.completed_tasks = []
                mock.weak_topics = []
                mock.achievements = []
                mock.skills = {}
                mock.reputation = 0
                success = _import_progress(self.test_file)
                self.assertTrue(success)
                self.assertEqual(mock.xp, 100)
                self.assertEqual(mock.level, 2)

    def test_import_nonexistent_file(self):
        """Импорт несуществующего файла."""
        with patch("handlers.sync.console.print"):
            success = _import_progress("nonexistent.json")
            self.assertFalse(success)

    def test_generate_user_id(self):
        """Генерация ID пользователя."""
        with patch("handlers.sync.get_state") as mock_state:
            del mock_state.return_value.sync_id
            user_id = _generate_user_id()
            self.assertIsInstance(user_id, str)
            self.assertGreater(len(user_id), 0)

    def test_sync_help(self):
        """Вызов справки /sync help."""
        with patch("handlers.sync.console.print"):
            result, action_taken = handle_sync("help")
            self.assertTrue(action_taken)

    def test_sync_id(self):
        """Показ ID /sync id."""
        with patch("handlers.sync.console.print"):
            result, action_taken = handle_sync("id")
            self.assertTrue(action_taken)

    def test_sync_unknown_subcommand(self):
        """Неизвестная подкоманда."""
        with patch("handlers.sync.console.print"):
            result, action_taken = handle_sync("unknown")
            self.assertTrue(action_taken)


if __name__ == "__main__":
    unittest.main()
