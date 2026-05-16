"""
Tests for language handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from handlers.lang import handle_lang


class TestLangHandler(unittest.TestCase):
    """Tests for /lang command handler."""

    @patch("handlers.lang.get_available_languages")
    @patch("handlers.lang.get_context")
    @patch("handlers.lang.console")
    def test_show_languages(self, mock_console, mock_get_context, mock_get_langs):
        mock_state = MagicMock()
        mock_state.language = "ru"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_get_langs.return_value = [
            {"code": "en", "name": "English"},
            {"code": "ru", "name": "Русский"},
        ]

        success, _, _, continue_loop = handle_lang("/lang")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.lang.get_available_languages")
    @patch("handlers.lang.get_context")
    @patch("handlers.lang.console")
    def test_switch_to_english(self, mock_console, mock_get_context, mock_get_langs):
        mock_state = MagicMock()
        mock_state.language = "ru"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_get_langs.return_value = [
            {"code": "en", "name": "English"},
            {"code": "ru", "name": "Русский"},
        ]

        success, _, _, continue_loop = handle_lang("/lang en")

        self.assertTrue(success)
        self.assertEqual(mock_state.language, "en")
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.lang.get_available_languages")
    @patch("handlers.lang.get_context")
    @patch("handlers.lang.console")
    def test_switch_to_russian(self, mock_console, mock_get_context, mock_get_langs):
        mock_state = MagicMock()
        mock_state.language = "en"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_get_langs.return_value = [
            {"code": "en", "name": "English"},
            {"code": "ru", "name": "Русский"},
        ]

        success, _, _, continue_loop = handle_lang("/lang ru")

        self.assertTrue(success)
        self.assertEqual(mock_state.language, "ru")
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.lang.get_available_languages")
    @patch("handlers.lang.get_context")
    @patch("handlers.lang.console")
    def test_switch_to_unsupported_language(self, mock_console, mock_get_context, mock_get_langs):
        mock_state = MagicMock()
        mock_state.language = "ru"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_get_langs.return_value = [
            {"code": "en", "name": "English"},
            {"code": "ru", "name": "Русский"},
        ]

        success, _, _, continue_loop = handle_lang("/lang fr")

        self.assertTrue(success)
        mock_ctx.save_state.assert_not_called()


if __name__ == "__main__":
    unittest.main()
