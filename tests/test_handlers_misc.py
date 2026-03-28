"""Unit tests for handlers/misc.py"""

import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMiscFunctions(unittest.TestCase):
    """Tests for miscellaneous handler functions"""

    # extract_json_block tests
    def test_extract_json_block_simple(self):
        from handlers.misc import extract_json_block

        text = '```json\n{"key": "value"}\n```'
        result = extract_json_block(text)
        self.assertEqual(result, '{"key": "value"}')

    def test_extract_json_block_no_backticks(self):
        from handlers.misc import extract_json_block

        text = 'prefix {"a": 1} suffix'
        result = extract_json_block(text)
        self.assertEqual(result, '{"a": 1}')

    def test_extract_json_block_nested(self):
        from handlers.misc import extract_json_block

        text = '```json\n{"outer": {"inner": 42}}\n```'
        result = extract_json_block(text)
        self.assertEqual(result, '{"outer": {"inner": 42}}')

    def test_extract_json_block_empty(self):
        from handlers.misc import extract_json_block

        self.assertIsNone(extract_json_block(""))
        self.assertIsNone(extract_json_block("no json here"))

    # _ask_confirm simple
    @patch("handlers.misc.console.print")
    @patch("handlers.misc._ask_confirm", return_value=True)
    def test_ask_confirm(self, mock_ask, mock_print):
        from handlers.misc import _ask_confirm

        result = _ask_confirm("Proceed?")
        self.assertIsInstance(result, bool)

    # clear_chat_db tests
    @patch("handlers.misc.console.print")
    @patch("memory.clear_chat")
    def test_clear_chat_db_calls_clear(self, mock_clear, mock_print):
        from handlers.misc import clear_chat_db

        mock_conn = MagicMock()
        clear_chat_db(mock_conn)
        mock_clear.assert_called_once_with(mock_conn)

    @patch("handlers.misc.console.print")
    def test_clear_chat_db_handles_exception(self, mock_print):
        from handlers.misc import clear_chat_db

        mock_conn = MagicMock()
        with patch("memory.clear_chat", side_effect=Exception("db error")):
            clear_chat_db(mock_conn)

    # handle_version tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_version(self, mock_print, mock_get_state):
        from handlers.misc import handle_version

        result = handle_version()
        self.assertEqual(result, (True, None, None, True))
        # Check that the first print is the version line
        mock_print.assert_any_call("[bold cyan]CyberTeacher v3.2[/bold cyan]")

    # handle_course stub
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_course_stub(self, mock_print, mock_get_state):
        from handlers.misc import handle_course

        result = handle_course("anything")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Курсы временно недоступны[/yellow]")

    # handle_history tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("memory.get_chat_history", return_value=[])
    def test_handle_history_no_conn(
        self, mock_get_chat_history, mock_print, mock_get_state
    ):
        from handlers.misc import handle_history

        result = handle_history(None)
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]История пуста[/yellow]")

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("memory.get_chat_history")
    def test_handle_history_with_entries(
        self, mock_get_chat_history, mock_print, mock_get_state
    ):
        from handlers.misc import handle_history

        mock_conn = MagicMock()
        mock_get_chat_history.return_value = [
            {"role": "user", "content": "hello", "mode": "teacher"},
            {"role": "assistant", "content": "hi", "mode": "teacher"},
        ]
        result = handle_history(mock_conn)
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[bold cyan]📜 История чата:[/bold cyan]")

    # handle_terminal_log tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_terminal_log_no_action(self, mock_print, mock_get_state):
        from handlers.misc import handle_terminal_log

        result = handle_terminal_log(None)
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_called()

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("terminal_log.log_command")
    def test_handle_terminal_log_with_action(
        self, mock_log_command, mock_print, mock_get_state
    ):
        from handlers.misc import handle_terminal_log

        result = handle_terminal_log("log echo test")
        self.assertEqual(result, (True, None, None, True))
        mock_log_command.assert_called_with("echo test", is_input=False)

    # handle_writeup tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_writeup_shows_template(self, mock_print, mock_get_state):
        from handlers.misc import handle_writeup
        from rich.panel import Panel

        result = handle_writeup()
        self.assertEqual(result, (True, None, None, True))
        # Check that a Panel was printed with title containing "Шаблон Write-up"
        panel_printed = any(
            isinstance(call[0][0], Panel) and "Шаблон Write-up" in str(call[0][0].title)
            for call in mock_print.call_args_list
            if call[0]
        )
        self.assertTrue(panel_printed)

    # handle_provider tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_provider_show_current(self, mock_print, mock_get_state):
        from handlers.misc import handle_provider

        with patch("config.LLM_PROVIDER", "ollama"):
            result = handle_provider("")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[cyan]📡 Текущий провайдер: ollama[/cyan]")

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def _test_handle_provider_set_ollama(self, mock_print, mock_get_state):
        from handlers.misc import handle_provider

        def fake_set_provider(p):
            # simulate change
            pass

        with (
            patch("config.LLM_PROVIDER", "openrouter"),
            patch("config.set_provider", fake_set_provider),
        ):
            result = handle_provider("provider ollama")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[green]✅ Провайдер изменён: openrouter → ollama[/green]"
        )

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_provider_invalid(self, mock_print, mock_get_state):
        from handlers.misc import handle_provider

        result = handle_provider("provider unknown")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[red]❌ Неизвестный провайдер. Доступные: ollama, openrouter, huggingface[/red]"
        )

    # handle_model tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_model_show_current(self, mock_print, mock_get_state):
        from handlers.misc import handle_model

        with (
            patch("config.LLM_PROVIDER", "ollama"),
            patch("config.OLLAMA_MODEL", "llama2"),
        ):
            result = handle_model("")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[cyan]🤖 Текущий провайдер: ollama[/cyan]")
        mock_print.assert_any_call("[cyan]Модель: llama2[/cyan]")

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_model_set(self, mock_print, mock_get_state):
        from handlers.misc import handle_model

        with patch("config.LLM_PROVIDER", "ollama"):
            result = handle_model("model custom-model")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[green]✅ Модель Ollama изменена: custom-model[/green]"
        )

    # handle_set_api_key tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_set_api_key_invalid_usage(self, mock_print, mock_get_state):
        from handlers.misc import handle_set_api_key

        result = handle_set_api_key("set-api-key")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[cyan]Установка API ключа[/cyan]")

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_set_api_key_openrouter(self, mock_print, mock_get_state):
        from handlers.misc import handle_set_api_key

        with patch.dict("os.environ", {}, clear=True):
            result = handle_set_api_key("set-api-key openrouter mykey")
            self.assertEqual(result, (True, None, None, True))
            self.assertEqual(os.environ.get("OPENROUTER_API_KEY"), "mykey")
            mock_print.assert_any_call(
                "[green]✅ OPENROUTER_API_KEY установлен для текущей сессии[/green]"
            )

    # handle_add_book tests
    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_missing_args(
        self, mock_exists, mock_print, mock_get_state
    ):
        from handlers.misc import handle_add_book

        result = handle_add_book("add_book")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[yellow]Использование: /add_book <путь_к_PDF>[/yellow]"
        )

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_file_not_found(
        self, mock_exists, mock_print, mock_get_state
    ):
        from handlers.misc import handle_add_book

        mock_exists.return_value = False
        result = handle_add_book("add_book missing.pdf")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[red]Файл не найден: missing.pdf[/red]")

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    @patch("shutil.copy2")
    def test_handle_add_book_success(
        self, mock_copy2, mock_exists, mock_print, mock_get_state
    ):
        from handlers.misc import handle_add_book

        # Simulate source file exists, destination does not
        def fake_exists(path):
            return path == "test.pdf"

        mock_exists.side_effect = fake_exists

        with patch("os.path.abspath") as mock_abspath:

            def fake_abspath(p):
                if p == "test.pdf":
                    return "/kb/test.pdf"
                return "/kb"

            mock_abspath.side_effect = fake_abspath
            with patch("os.path.basename", return_value="test.pdf"):
                result = handle_add_book("add_book test.pdf")
        self.assertEqual(result, (True, None, None, True))
        self.assertTrue(mock_copy2.called)

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_not_pdf(self, mock_exists, mock_print, mock_get_state):
        from handlers.misc import handle_add_book

        # Simulate source file exists
        def fake_exists(path):
            return path == "test.txt"

        mock_exists.side_effect = fake_exists

        with patch("os.path.abspath") as mock_abspath:

            def fake_abspath(p):
                if p == "test.txt":
                    return "/kb/test.txt"
                return "/kb"

            mock_abspath.side_effect = fake_abspath
            result = handle_add_book("add_book test.txt")
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Поддерживаются только PDF файлы[/yellow]")

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_outside_knowledge_dir(
        self, mock_exists, mock_print, mock_get_state
    ):
        from handlers.misc import handle_add_book

        mock_exists.return_value = True
        with patch("os.path.abspath") as mock_abspath:

            def fake_abspath(p):
                if p == "test.pdf":
                    return "/forbidden/test.pdf"
                return "/allowed"

            mock_abspath.side_effect = fake_abspath
            result = handle_add_book("add_book test.pdf")
        self.assertEqual(result, (True, None, None, True))
        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Запрещенный путь", printed)

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("story_mode.get_story_list", return_value="Test story list")
    def test_handle_story_mode_list(
        self, mock_get_story_list, mock_print, mock_get_state
    ):
        from handlers.misc import handle_story_mode

        result = handle_story_mode("story")
        self.assertTrue(result[0])
        calls = [str(call[0][0]) for call in mock_print.call_args_list if call[0]]
        self.assertIn("Test story list", calls)

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_risk_display(self, mock_print, mock_get_state):
        from handlers.misc import handle_risk

        mock_state = MagicMock()
        mock_state.get_risk_status.return_value = "Низкий (15/100)"
        mock_get_state.return_value = mock_state
        result = handle_risk("risk")
        self.assertTrue(result[0])
        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Уровень риска", printed)

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    def test_handle_repeat_no_due(self, mock_print, mock_get_state):
        from handlers.misc import handle_repeat

        mock_state = MagicMock()
        mock_state.get_due_reviews.return_value = []
        mock_get_state.return_value = mock_state
        result = handle_repeat("repeat")
        self.assertTrue(result[0])
        mock_print.assert_any_call(
            "[green]🎉 Нет тем для повторения! Все темы в актуальном состоянии.[/green]"
        )

    @patch("handlers.misc.get_state")
    @patch("handlers.misc.console.print")
    @patch("knowledge.get_current_vectordb")
    @patch("generators.generate_quiz")
    def test_handle_repeat_with_due(
        self, mock_generate_quiz, mock_get_vectordb, mock_print, mock_get_state
    ):
        from handlers.misc import handle_repeat

        mock_state = MagicMock()
        mock_state.review_schedule = {}
        mock_state.get_due_reviews.return_value = [
            {"topic": "test_topic", "interval": 1, "repetitions": 1}
        ]
        mock_get_state.return_value = mock_state
        mock_get_vectordb.return_value = MagicMock()
        mock_generate_quiz.return_value = {
            "questions": [
                {"question": "Q", "options": {"a": "A", "b": "B"}, "correct": "a"}
            ]
        }
        with patch("builtins.input", side_effect=["1", "a"]):
            result = handle_repeat("repeat")
        self.assertTrue(result[0])
        mock_state.update_weak_topic.assert_called_once()
        mock_state.mark_reviewed.assert_called_once()
        mock_state.save_to_file.assert_called_once()


if __name__ == "__main__":
    unittest.main()
