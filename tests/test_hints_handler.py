"""
Tests for hints handler.
"""

import unittest
from unittest.mock import MagicMock, patch

from handlers.hints import (
    DEFAULT_PATTERNS,
    _load_patterns,
    generate_contextual_hint,
    handle_hint,
)


class TestHintsHandler(unittest.TestCase):
    """Tests for /hint command handler."""

    def test_default_patterns_not_empty(self):
        self.assertGreater(len(DEFAULT_PATTERNS), 0)

    def test_default_patterns_have_required_keys(self):
        for pattern in DEFAULT_PATTERNS:
            self.assertIn("regex", pattern)
            self.assertIn("hint", pattern)
            self.assertIn("tags", pattern)

    def test_load_patterns_uses_defaults_when_no_file(self):
        patterns = _load_patterns()
        self.assertEqual(patterns, DEFAULT_PATTERNS)

    def test_generate_contextual_hint_sqli(self):
        hint = generate_contextual_hint("curl http://example.com?id=1", {})
        self.assertIsNotNone(hint)
        self.assertIn("SQLi", hint)

    def test_generate_contextual_hint_xss(self):
        hint = generate_contextual_hint("<script>alert(1)</script>", {})
        self.assertIsNotNone(hint)
        self.assertIn("XSS", hint)

    def test_generate_contextual_hint_nmap(self):
        hint = generate_contextual_hint("nmap -p- 192.168.1.1", {})
        self.assertIsNotNone(hint)
        self.assertIn("сканирование", hint.lower())

    def test_generate_contextual_hint_no_match(self):
        hint = generate_contextual_hint("hello world", {})
        self.assertIsNone(hint)

    @patch("handlers.hints.get_context")
    @patch("handlers.hints.console")
    def test_hint_status(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.hint_enabled = True
        mock_state.hint_credits = 3
        mock_state.hints_used = 1
        mock_state.hint_cooldown = 30
        mock_state.last_hint_time = 0
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_hint("/hint status")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.hints.get_context")
    @patch("handlers.hints.console")
    def test_hint_enable(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.hint_enabled = False
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        handle_hint("/hint on")

        self.assertTrue(mock_state.hint_enabled)

    @patch("handlers.hints.get_context")
    @patch("handlers.hints.console")
    def test_hint_disable(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.hint_enabled = True
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        handle_hint("/hint off")

        self.assertFalse(mock_state.hint_enabled)

    @patch("handlers.hints.get_context")
    @patch("handlers.hints.console")
    def test_hint_get_no_credits(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.hint_credits = 0
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        handle_hint("/hint get")

        mock_console.print.assert_called()

    @patch("handlers.hints.get_context")
    @patch("handlers.hints.console")
    def test_hint_get_cooldown(self, mock_console, mock_get_context):
        import time
        mock_state = MagicMock()
        mock_state.hint_credits = 2
        mock_state.last_hint_time = time.time() - 5
        mock_state.hint_cooldown = 30
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        handle_hint("/hint get")

        mock_console.print.assert_called()

    @patch("handlers.hints.get_context")
    @patch("handlers.hints.console")
    def test_hint_clear(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.hints_used = 5
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        handle_hint("/hint clear")

        self.assertEqual(mock_state.hints_used, 0)
        mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
