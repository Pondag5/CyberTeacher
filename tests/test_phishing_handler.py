"""
Tests for phishing handler.
"""

import unittest
from unittest.mock import patch, MagicMock

from handlers.phishing import (
    PHISHING_TEMPLATES,
    PHISHING_CRITERIA,
    handle_phishing,
    _show_templates,
    _show_tips,
)


class TestPhishingHandler(unittest.TestCase):
    """Tests for /phishing command handler."""

    def test_templates_not_empty(self):
        self.assertGreater(len(PHISHING_TEMPLATES), 3)

    def test_templates_have_required_keys(self):
        for tid, t in PHISHING_TEMPLATES.items():
            self.assertIn("name", t)
            self.assertIn("scenario", t)
            self.assertIn("elements", t)

    def test_criteria_not_empty(self):
        self.assertGreater(len(PHISHING_CRITERIA), 3)

    @patch("handlers.phishing.console")
    def test_show_templates(self, mock_console):
        _show_templates()
        mock_console.print.assert_called()

    @patch("handlers.phishing.console")
    def test_show_tips(self, mock_console):
        _show_tips()
        mock_console.print.assert_called()

    @patch("handlers.phishing.console")
    def test_handle_phishing_no_args(self, mock_console):
        success, _, _, continue_loop = handle_phishing("/phishing")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.phishing.console")
    def test_handle_phishing_templates(self, mock_console):
        with patch("handlers.phishing._show_templates") as mock_show:
            success, _, _, continue_loop = handle_phishing("/phishing templates")

            self.assertTrue(success)
            mock_show.assert_called_once()

    @patch("handlers.phishing.console")
    def test_handle_phishing_tips(self, mock_console):
        with patch("handlers.phishing._show_tips") as mock_show:
            success, _, _, continue_loop = handle_phishing("/phishing tips")

            self.assertTrue(success)
            mock_show.assert_called_once()

    @patch("handlers.phishing.console")
    def test_handle_phishing_generate_invalid_type(self, mock_console):
        success, _, _, continue_loop = handle_phishing("/phishing generate invalid_type")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.phishing.console")
    def test_handle_phishing_unknown_subcommand(self, mock_console):
        success, _, _, continue_loop = handle_phishing("/phishing unknown")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.phishing.get_context")
    @patch("handlers.phishing.console")
    def test_handle_phishing_generate_llm_unavailable(self, mock_console, mock_get_context):
        import config
        mock_state = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        with patch.object(config.LazyLoader, "get_llm", return_value=None):
            success, _, _, continue_loop = handle_phishing("/phishing generate bank")

            self.assertTrue(success)
            mock_console.print.assert_called()


if __name__ == "__main__":
    unittest.main()
