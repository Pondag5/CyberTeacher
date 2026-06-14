"""Unit tests for handlers/context.py"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestContextHandler(unittest.TestCase):
    @patch("handlers.context.get_context")
    @patch("handlers.context.console.print")
    def test_context_stats(self, mock_print, mock_get_context):
        mock_ctx = MagicMock()
        mock_ctx.state._msg_count_since_summary = 5
        mock_get_context.return_value = mock_ctx

        from handlers.context import handle_context

        with patch("db.init_db") as mock_init_db:
            mock_conn = MagicMock()
            mock_init_db.return_value = mock_conn
            with patch("memory.get_chat_history", return_value=[]):
                result = handle_context("/context stats")
                self.assertTrue(result[0])

    @patch("handlers.context.console.print")
    def test_context_clear(self, mock_print):
        from handlers.context import handle_context

        with patch("db.init_db") as mock_init_db:
            mock_conn = MagicMock()
            mock_init_db.return_value = mock_conn
            result = handle_context("/context clear")
            self.assertTrue(result[0])
            mock_conn.execute.assert_called_once()
            mock_conn.commit.assert_called_once()

    @patch("handlers.context.console.print")
    def test_context_help(self, mock_print):
        from handlers.context import handle_context

        result = handle_context("/context help")
        self.assertTrue(result[0])

    @patch.dict(os.environ, {"LLM_PROVIDER": "mock"}, clear=False)
    @patch("handlers.context.console.print")
    def test_context_defaults_to_stats(self, mock_print):
        from handlers.context import handle_context

        with patch("db.init_db") as mock_init_db:
            mock_conn = MagicMock()
            mock_init_db.return_value = mock_conn
            with patch("memory.get_chat_history", return_value=[]):
                result = handle_context("/context")
                self.assertTrue(result[0])
