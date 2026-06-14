"""Тесты для модуля Cross-platform Sync (M-20)."""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

from handlers.sync import (
    _export_progress,
    _generate_user_id,
    _import_progress,
    handle_sync,
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
            with patch("handlers.sync.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.xp = 100
                mock_state.level = 2
                mock_state.completed_quizzes = ["quiz1"]
                mock_state.completed_tasks = []
                mock_state.weak_topics = ["crypto"]
                mock_state.achievements = []
                mock_state.skills = {}
                mock_state.reputation = 50
                mock_state.sync_id = "test123"
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _export_progress(self.test_file)
                self.assertTrue(success)
                self.assertTrue(os.path.exists(self.test_file))

    def test_import_progress(self):
        """Импорт прогресса."""
        # Сначала создадим файл
        with patch("handlers.sync.console.print"):
            with patch("handlers.sync.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.xp = 100
                mock_state.level = 2
                mock_state.completed_quizzes = ["quiz1"]
                mock_state.completed_tasks = []
                mock_state.weak_topics = ["crypto"]
                mock_state.achievements = []
                mock_state.skills = {}
                mock_state.reputation = 50
                mock_state.sync_id = "test123"
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                _export_progress(self.test_file)

        # Теперь импортируем
        with patch("handlers.sync.console.print"):
            with patch("handlers.sync.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.xp = 0
                mock_state.level = 1
                mock_state.completed_quizzes = []
                mock_state.completed_tasks = []
                mock_state.weak_topics = []
                mock_state.achievements = []
                mock_state.skills = {}
                mock_state.reputation = 0
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _import_progress(self.test_file)
                self.assertTrue(success)
                self.assertEqual(mock_state.xp, 100)
                self.assertEqual(mock_state.level, 2)

    def test_import_nonexistent_file(self):
        """Импорт несуществующего файла."""
        with patch("handlers.sync.console.print"):
            success = _import_progress("nonexistent.json")
            self.assertFalse(success)

    def test_generate_user_id(self):
        """Генерация ID пользователя."""
        with patch("handlers.sync.get_context") as mock_get_context:
            mock_state = MagicMock()
            del mock_state.sync_id
            mock_ctx = MagicMock()
            mock_ctx.state = mock_state
            mock_get_context.return_value = mock_ctx
            user_id = _generate_user_id()
            self.assertIsInstance(user_id, str)
            self.assertGreater(len(user_id), 0)

    def test_sync_help(self):
        """Вызов справки /sync help."""
        with patch("handlers.sync.console.print"):
            _, result, _, action_taken = handle_sync("help")
            self.assertTrue(action_taken)

    def test_sync_id(self):
        """Показ ID /sync id."""
        with patch("handlers.sync.console.print"):
            _, result, _, action_taken = handle_sync("id")
            self.assertTrue(action_taken)

    def test_sync_unknown_subcommand(self):
        """Неизвестная подкоманда."""
        with patch("handlers.sync.console.print"):
            _, result, _, action_taken = handle_sync("unknown")
            self.assertTrue(action_taken)


if __name__ == "__main__":
    unittest.main()
