"""Unit tests for handlers/misc.py"""

import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

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
            try:
                clear_chat_db(mock_conn)
            except Exception:
                pass

    # handle_version tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_version(self, mock_print, mock_get_context):
        from handlers.misc import handle_version

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_version()
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[bold]CyberTeacher v5.0 (2026-05-23)[/bold]")

    # handle_course - lists courses
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_course_lists_courses(self, mock_print, mock_get_context):
        from handlers.misc import handle_course

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_course("course")
        self.assertEqual(result, (True, None, None, True))
        self.assertTrue(mock_print.called)

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_course_details(self, mock_print, mock_get_context):
        from handlers.misc import handle_course

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_course("course web-basics")
        self.assertEqual(result, (True, None, None, True))
        self.assertTrue(mock_print.called)

    # handle_history tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    @patch("memory.get_chat_history", return_value=[])
    def test_handle_history_no_conn(
        self, mock_get_chat_history, mock_print, mock_get_context
    ):
        from handlers.misc import handle_history

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_history(None)
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]История пуста[/yellow]")

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    @patch("memory.get_chat_history")
    def test_handle_history_with_entries(
        self, mock_get_chat_history, mock_print, mock_get_context
    ):
        from handlers.misc import handle_history

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        mock_conn = MagicMock()
        mock_get_chat_history.return_value = [
            {"role": "user", "content": "hello", "mode": "teacher"},
            {"role": "assistant", "content": "hi", "mode": "teacher"},
        ]
        result = handle_history(mock_conn)
        self.assertEqual(result, (True, None, None, True))

    # handle_terminal_log tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_terminal_log_no_action(self, mock_print, mock_get_context):
        from handlers.misc import handle_terminal_log

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_terminal_log(None)
        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_called()

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_terminal_log_with_action(self, mock_print, mock_get_context):
        from handlers.misc import handle_terminal_log

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_terminal_log("log echo test")
        self.assertEqual(result, (True, None, None, True))

    # handle_writeup tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_writeup_shows_template(self, mock_print, mock_get_context):
        from rich.panel import Panel

        from handlers.misc import handle_writeup

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_writeup()
        self.assertEqual(result, (True, None, None, True))
        self.assertTrue(mock_print.called)

    # handle_provider tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_provider_show_current(self, mock_print, mock_get_context):
        from handlers.misc import handle_provider

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        with patch("config.LLM_PROVIDER", "ollama"):
            result = handle_provider("")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_provider_invalid(self, mock_print, mock_get_context):
        from handlers.misc import handle_provider

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_provider("provider unknown")
        self.assertEqual(result, (True, None, None, True))

    # handle_model tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_model_show_current(self, mock_print, mock_get_context):
        from handlers.misc import handle_model

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        with (
            patch("config.LLM_PROVIDER", "ollama"),
            patch("config.OLLAMA_MODEL", "llama2"),
        ):
            result = handle_model("")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_model_set(self, mock_print, mock_get_context):
        from handlers.misc import handle_model

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        with patch("config.LLM_PROVIDER", "ollama"):
            result = handle_model("model custom-model")
        self.assertEqual(result, (True, None, None, True))

    # handle_set_api_key tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_set_api_key_invalid_usage(self, mock_print, mock_get_context):
        from handlers.misc import handle_set_api_key

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_set_api_key("set-api-key")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_set_api_key_openrouter(self, mock_print, mock_get_context):
        from handlers.misc import handle_set_api_key

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        with patch.dict("os.environ", {}, clear=True):
            result = handle_set_api_key("set-api-key openrouter mykey")
            self.assertEqual(result, (True, None, None, True))
            self.assertEqual(os.environ.get("OPENROUTER_API_KEY"), "mykey")

    # handle_add_book tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_missing_args(
        self, mock_exists, mock_print, mock_get_context
    ):
        from handlers.misc import handle_add_book

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_add_book("add_book")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_file_not_found(
        self, mock_exists, mock_print, mock_get_context
    ):
        from handlers.misc import handle_add_book

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        mock_exists.return_value = False
        result = handle_add_book("add_book missing.pdf")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_not_pdf(self, mock_exists, mock_print, mock_get_context):
        from handlers.misc import handle_add_book

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        mock_exists.return_value = True
        result = handle_add_book("add_book test.txt")
        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    @patch("os.path.exists")
    def test_handle_add_book_outside_knowledge_dir(
        self, mock_exists, mock_print, mock_get_context
    ):
        from handlers.misc import handle_add_book

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        mock_exists.return_value = True
        result = handle_add_book("add_book test.pdf")
        self.assertEqual(result, (True, None, None, True))

    # story_mode test
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_story_mode_list(self, mock_print, mock_get_context):
        from handlers.misc import handle_story_mode

        mock_ctx = MagicMock()
        mock_ctx.state = MagicMock()
        mock_get_context.return_value = mock_ctx
        result = handle_story_mode("story")
        self.assertTrue(result[0])

    # risk display test
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_risk_display(self, mock_print, mock_get_context):
        from handlers.misc import handle_risk

        mock_state = MagicMock()
        mock_state.get_risk_status.return_value = "Низкий (15/100)"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_risk("risk")
        self.assertTrue(result[0])

    # repeat tests
    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_repeat_no_due(self, mock_print, mock_get_context):
        from handlers.misc import handle_repeat

        mock_state = MagicMock()
        mock_state.get_due_reviews.return_value = []
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_repeat("repeat")
        self.assertTrue(result[0])

    @patch("handlers.misc.get_context")
    @patch("handlers.misc.console.print")
    def test_handle_repeat_with_due(self, mock_print, mock_get_context):
        from handlers.misc import handle_repeat

        mock_state = MagicMock()
        mock_state.get_due_reviews.return_value = [
            {"topic": "test_topic", "interval": 1, "repetitions": 1, "last_review": 0}
        ]
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        result = handle_repeat("repeat")
        self.assertTrue(result[0])


if __name__ == "__main__":
    unittest.main()
