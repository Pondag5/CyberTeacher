"""
Tests for theme handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from di import AppContext
from handlers.theme import THEMES, handle_theme, get_theme_colors


class TestThemeHandler(unittest.TestCase):
    """Tests for /theme command handler."""

    def test_themes_not_empty(self):
        self.assertGreater(len(THEMES), 3)

    def test_themes_have_required_keys(self):
        for theme_id, theme in THEMES.items():
            self.assertIn("name", theme)
            self.assertIn("border", theme)
            self.assertIn("primary", theme)
            self.assertIn("success", theme)
            self.assertIn("warning", theme)
            self.assertIn("error", theme)

    @patch("handlers.theme.get_context")
    @patch("handlers.theme.console")
    def test_list_themes(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.current_theme = "default"
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_theme("/theme")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.theme.get_context")
    @patch("handlers.theme.console")
    def test_set_valid_theme(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_theme("/theme dark")

        self.assertTrue(success)
        self.assertEqual(mock_state.current_theme, "dark")
        mock_ctx.save_state.assert_called_once()

    @patch("handlers.theme.get_context")
    @patch("handlers.theme.console")
    def test_set_invalid_theme(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_theme("/theme nonexistent")

        self.assertTrue(success)
        mock_ctx.save_state.assert_not_called()

    @patch("handlers.theme.get_context")
    def test_get_theme_colors_default(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.current_theme = "default"
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        colors = get_theme_colors()
        self.assertEqual(colors["border"], "cyan")

    @patch("handlers.theme.get_context")
    def test_get_theme_colors_dark(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.current_theme = "dark"
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        colors = get_theme_colors()
        self.assertEqual(colors["border"], "green")

    @patch("handlers.theme.get_context")
    def test_get_theme_colors_fallback(self, mock_get_context):
        mock_state = MagicMock()
        del mock_state.current_theme
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        colors = get_theme_colors()
        self.assertEqual(colors["border"], "cyan")

    @patch("handlers.theme.get_context")
    @patch("handlers.theme.console")
    def test_list_themes(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.current_theme = "default"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_theme("/theme")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.theme.get_context")
    @patch("handlers.theme.console")
    def test_set_invalid_theme(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        success, _, _, continue_loop = handle_theme("/theme nonexistent")

        self.assertTrue(success)
        mock_ctx.save_state.assert_not_called()

    @patch("handlers.theme.get_context")
    def test_get_theme_colors_default(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.current_theme = "default"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        colors = get_theme_colors()
        self.assertEqual(colors["border"], "cyan")

    @patch("handlers.theme.get_context")
    def test_get_theme_colors_dark(self, mock_get_context):
        mock_state = MagicMock()
        mock_state.current_theme = "dark"
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        colors = get_theme_colors()
        self.assertEqual(colors["border"], "green")

    @patch("handlers.theme.get_context")
    def test_get_theme_colors_fallback(self, mock_get_context):
        mock_state = MagicMock()
        del mock_state.current_theme
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        colors = get_theme_colors()
        self.assertEqual(colors["border"], "cyan")

    @patch("handlers.theme.get_context")
    @patch("handlers.theme.console")
    def test_set_theme_initializes_if_missing(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        del mock_state.current_theme
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        handle_theme("/theme")

        self.assertEqual(mock_state.current_theme, "default")
        mock_ctx.save_state.assert_called()


if __name__ == "__main__":
    unittest.main()
