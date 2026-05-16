"""
Tests for api_handler, async_handler, registry, export_extended, and summarize handlers.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# ── API Handler ───────────────────────────────────────────────
class TestAPIHandler(unittest.TestCase):
    """Tests for /api command."""

    @patch("handlers.api_handler.console")
    def test_api_start(self, mock_console):
        from handlers.api_handler import handle_api
        response, should_continue = handle_api("/api start")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_stop(self, mock_console):
        from handlers.api_handler import handle_api
        response, should_continue = handle_api("/api stop")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_status(self, mock_console):
        from handlers.api_handler import handle_api
        response, should_continue = handle_api("/api status")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_help(self, mock_console):
        from handlers.api_handler import handle_api
        response, should_continue = handle_api("/api help")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.api_handler.console")
    def test_api_unknown(self, mock_console):
        from handlers.api_handler import handle_api
        response, should_continue = handle_api("/api unknown")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()


# ── Async Handler ─────────────────────────────────────────────
class TestAsyncHandler(unittest.TestCase):
    """Tests for async handler functions."""

    def test_async_rag_search_error(self):
        from handlers.async_handler import async_rag_search
        import asyncio

        mock_kb = MagicMock()
        mock_kb.get_relevant_docs.side_effect = Exception("test error")

        result = asyncio.run(async_rag_search("test", mock_kb))
        self.assertIsNone(result)

    def test_async_llm_call_error(self):
        from handlers.async_handler import async_llm_call
        import asyncio

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("test error")

        result = asyncio.run(async_llm_call(mock_llm, "test prompt"))
        self.assertIsNone(result)

    def test_async_combined_query_both_fail(self):
        from handlers.async_handler import async_combined_query
        import asyncio

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("llm error")
        mock_kb = MagicMock()
        mock_kb.get_relevant_docs.side_effect = Exception("rag error")

        result = asyncio.run(async_combined_query("test", mock_llm, mock_kb))
        self.assertIsNone(result["rag_result"])
        self.assertIsNone(result["llm_result"])
        self.assertEqual(result["combined_response"], "")

    def test_async_combined_query_rag_success(self):
        from handlers.async_handler import async_combined_query
        import asyncio

        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("llm error")
        mock_kb = MagicMock()
        mock_kb.get_relevant_docs.return_value = "RAG result"

        result = asyncio.run(async_combined_query("test", mock_llm, mock_kb))
        self.assertEqual(result["rag_result"], "RAG result")
        self.assertIsNone(result["llm_result"])

    def test_run_async_query_no_loop(self):
        from handlers.async_handler import run_async_query
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="LLM response")
        mock_kb = MagicMock()
        mock_kb.get_relevant_docs.return_value = "RAG result"

        result = run_async_query("test", mock_llm, mock_kb)
        self.assertIn("LLM", result["combined_response"])


# ── Registry ──────────────────────────────────────────────────
class TestRegistry(unittest.TestCase):
    """Tests for CommandRegistry."""

    def test_register_exact(self):
        from handlers.registry import CommandRegistry
        registry = CommandRegistry()

        @registry.register_exact("test_cmd")
        def handler(action, llm, conn):
            return True, None, None, True

        h, remaining = registry.get_handler("test_cmd")
        self.assertIsNotNone(h)
        self.assertEqual(remaining, "")

    def test_register_prefix(self):
        from handlers.registry import CommandRegistry
        registry = CommandRegistry()

        @registry.register_prefix("prefix_")
        def handler(action, llm, conn):
            return True, None, None, True

        h, remaining = registry.get_handler("prefix_arg")
        self.assertIsNotNone(h)
        self.assertEqual(remaining, "arg")

    def test_get_handler_not_found(self):
        from handlers.registry import CommandRegistry
        registry = CommandRegistry()

        h, remaining = registry.get_handler("nonexistent")
        self.assertIsNone(h)
        self.assertEqual(remaining, "nonexistent")

    def test_list_commands(self):
        from handlers.registry import CommandRegistry
        registry = CommandRegistry()

        @registry.register_exact("exact_cmd")
        def handler1(action, llm, conn):
            return True, None, None, True

        @registry.register_prefix("prefix_")
        def handler2(action, llm, conn):
            return True, None, None, True

        commands = registry.list_commands()
        self.assertIn("exact_cmd", commands)
        self.assertIn("prefix_", commands)
        self.assertEqual(commands["exact_cmd"], "exact")
        self.assertEqual(commands["prefix_"], "prefix")


# ── Export Extended Handler ───────────────────────────────────
class TestExportExtendedHandler(unittest.TestCase):
    """Tests for /export extended command."""

    @patch("handlers.export_extended.console")
    def test_export_extended_no_args(self, mock_console):
        from handlers.export_extended import handle_export_extended
        response, should_continue = handle_export_extended("/export extended")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.export_extended.console")
    def test_export_extended_unknown_format(self, mock_console):
        from handlers.export_extended import handle_export_extended
        response, should_continue = handle_export_extended("/export extended xml")

        self.assertTrue(should_continue)
        mock_console.print.assert_called()

    @patch("handlers.export_extended.console")
    @patch("handlers.export_extended.get_state")
    def test_export_extended_html(self, mock_get_state, mock_console):
        mock_state = MagicMock()
        mock_state.conn = None
        mock_get_state.return_value = mock_state

        with patch("handlers.export_extended.get_chat_history", return_value=[]):
            from handlers.export_extended import handle_export_extended
            response, should_continue = handle_export_extended("/export extended html test_export.html")

            mock_console.print.assert_called()
            # Cleanup
            if os.path.exists("test_export.html"):
                os.remove("test_export.html")


# ── Summarize Handler ─────────────────────────────────────────
class TestSummarizeHandler(unittest.TestCase):
    """Tests for /summarize command."""

    @patch("handlers.summarize.console")
    def test_summarize_short_history(self, mock_console):
        with patch("memory.get_chat_history", return_value=[{"role": "user", "content": "hi"}]):
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
