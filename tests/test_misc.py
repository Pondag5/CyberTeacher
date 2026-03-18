# -*- coding: utf-8 -*-
"""Тесты для misc.handlers (функции-утилиты)"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from handlers import misc
from state import get_state
from memory import init_db, save_message, get_chat_history


class TestCheckOpenAnswer(unittest.TestCase):
    """Тесты для check_open_answer (оценка развернутых ответов)"""

    def test_exact_match(self):
        """Почти точное совпадение с ключевыми пунктами"""
        question = "Что такое XSS?"
        user_ans = "XSS — кросс-сайт скриптинг, это инъекция JS в страницу."
        key_points = ["кросс-сайт", "скриптинг", "инъекция", "JavaScript"]
        result = misc.check_open_answer(question, user_ans, key_points)
        self.assertIsInstance(result, dict)
        self.assertIn("score", result)
        self.assertIn("feedback", result)
        self.assertGreater(result["score"], 0)

    def test_empty_answer(self):
        """Пустой ответ"""
        result = misc.check_open_answer("Вопрос?", "", ["точка1"])
        self.assertEqual(result["score"], 0)
        self.assertIn("Спасибо", result["feedback"])

    def test_long_irrelevant(self):
        """Длинный, но нерелевантный ответ"""
        user_ans = "Это длинный текст, который ничего не говорит о теме." * 5
        result = misc.check_open_answer("Вопрос?", user_ans, ["ключевое"])
        self.assertEqual(result["score"], 0)


class TestStoryMode(unittest.TestCase):
    """Тесты для переключения story mode"""

    def test_toggle_story_mode(self):
        state = get_state()
        initial = state.story_mode
        misc.handle_story_mode()
        self.assertEqual(state.story_mode, not initial)
        # Reset
        misc.handle_story_mode()
        self.assertEqual(state.story_mode, initial)


class TestVersion(unittest.TestCase):
    """Тесты для команды version"""

    def test_handle_version_prints(self):
        # mock console
        with patch.object(misc, "console", MagicMock()) as mock_console:
            misc.handle_version()
            # Проверим, что print был вызван с строкой, содержащей "CyberTeacher"
            called = any(
                "CyberTeacher" in str(args)
                for args, kwargs in mock_console.print.call_args_list
            )
            self.assertTrue(called)


class TestAddBook(unittest.TestCase):
    """Тесты для добавления книги"""

    def test_add_book_success(self):
        # Создаем временный PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"%PDF-1.4 fake")
            tmp_path = tmp.name
        try:
            with (
                patch.object(misc, "console", MagicMock()),
                patch("handlers.misc.save_book_to_kb") as mock_save,
                patch("handlers.misc.os.path.isfile", return_value=True),
            ):
                misc.handle_add_book(tmp_path)
                mock_save.assert_called_once()
        finally:
            os.unlink(tmp_path)

    def test_add_book_missing_file(self):
        with patch.object(misc, "console", MagicMock()) as mock_console:
            misc.handle_add_book("/nonexistent/file.pdf")
            # Должен быть вывод об ошибке
            mock_console.print.assert_called()
            args, _ = mock_console.print.call_args
            self.assertIn("не найден", str(args[0]))


class TestHistory(unittest.TestCase):
    """Тесты для команды history"""

    @classmethod
    def setUpClass(cls):
        cls.conn = init_db(":memory:")
        save_message(cls.conn, "user", "Привет", "teacher")
        save_message(cls.conn, "assistant", "Привет, как дела?", "teacher")

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_handle_history_shows_messages(self):
        with (
            patch.object(misc, "console", MagicMock()) as mock_console,
            patch.object(misc, "get_conn", return_value=self.conn),
        ):
            misc.handle_history()
            # Проверим, что выведены оба сообщения
            prints = [
                str(args[0]) for args, _ in mock_console.print.call_args_list if args
            ]
            self.assertTrue(any("Привет" in p for p in prints))
            self.assertTrue(any("как дела" in p for p in prints))


class TestTerminalLog(unittest.TestCase):
    """Тесты для логирования терминала"""

    def test_save_terminal_log(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / "logs"
            log_dir.mkdir()
            # Патчим LOG_DIR в misc
            with patch.object(misc, "LOG_DIR", log_dir):
                misc.save_terminal_log("user", "/test command")
                # Проверим создание файла
                files = list(log_dir.glob("terminal_*.log"))
                self.assertEqual(len(files), 1)
                content = files[0].read_text(encoding="utf-8")
                self.assertIn("/test command", content)


class TestNews(unittest.TestCase):
    """Тесты для команды news"""

    @patch("handlers.misc.fetch_news")
    def test_handle_news_with_news(self, mock_fetch):
        mock_fetch.return_value = {"news": [{"title": "Test", "link": "http://test"}]}
        with patch.object(misc, "console", MagicMock()) as mock_console:
            misc.handle_news()
            # Проверяем, что выведен заголовок
            prints = [
                str(args[0]) for args, _ in mock_console.print.call_args_list if args
            ]
            self.assertTrue(any("Новости" in p for p in prints))

    @patch("handlers.misc.fetch_news")
    def test_handle_news_no_news(self, mock_fetch):
        mock_fetch.return_value = {"news": []}
        with patch.object(misc, "console", MagicMock()) as mock_console:
            misc.handle_news()
            prints = [
                str(args[0]) for args, _ in mock_console.print.call_args_list if args
            ]
            self.assertTrue(any("Нет новостей" in p for p in prints))


if __name__ == "__main__":
    unittest.main()
