"""
Tests for api_handler and summarize handlers.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch


# ── API Handler ───────────────────────────────────────────────
class TestAPIHandler(unittest.TestCase):
    """Tests for /api command."""

    @patch("handlers.api_handler.console")
    def test_api_start(self, mock_console):
        from handlers.api_handler import handle_api

        _, _, _, should_continue = handle_api("api start")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_stop(self, mock_console):
        from handlers.api_handler import handle_api

        _, _, _, should_continue = handle_api("api stop")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_status(self, mock_console):
        from handlers.api_handler import handle_api

        _, _, _, should_continue = handle_api("api status")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_help(self, mock_console):
        from handlers.api_handler import handle_api

        _, _, _, should_continue = handle_api("api help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_empty(self, mock_console):
        from handlers.api_handler import handle_api

        _, _, _, should_continue = handle_api("api")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_unknown(self, mock_console):
        from handlers.api_handler import handle_api

        _, _, _, should_continue = handle_api("api unknown")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()


# ── Summarize Handler ─────────────────────────────────────────
class TestSummarizeHandler(unittest.TestCase):
    """Tests for /summarize command."""

    @patch("handlers.summarize.console")
    def test_summarize_short_history(self, mock_console):
        with patch(
            "memory.get_chat_history", return_value=[{"role": "user", "content": "hi"}]
        ):
            from handlers.summarize import handle_summarize

            success, _, _, continue_loop = handle_summarize("/summarize")

            self.assertTrue(success)
            self.assertTrue(continue_loop)

    def test_generate_summary_llm_unavailable(self):
        history = [{"role": "user", "content": f"Message {i}"} for i in range(30)]

        with patch("config.LazyLoader.get_llm", return_value=None):
            from handlers.summarize import _generate_summary

            result = _generate_summary(history)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
