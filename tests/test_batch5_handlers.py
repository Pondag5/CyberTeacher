"""
Tests for assignment_templates and threats handlers.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# ── Assignment Templates Handler ──────────────────────────────
class TestAssignmentTemplatesHandler(unittest.TestCase):
    """Tests for /templates command."""

    @patch("handlers.assignment_templates.console")
    def test_templates_no_args(self, mock_console):
        from handlers.assignment_templates import handle_assignment_templates
        success, _, _, continue_loop = handle_assignment_templates("/templates")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.assignment_templates.console")
    def test_templates_list(self, mock_console):
        from handlers.assignment_templates import handle_assignment_templates
        success, _, _, continue_loop = handle_assignment_templates("/templates list")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.assignment_templates.console")
    def test_templates_show_valid(self, mock_console):
        from handlers.assignment_templates import handle_assignment_templates
        success, _, _, continue_loop = handle_assignment_templates("/templates show web_discovery")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.assignment_templates.console")
    def test_templates_show_invalid(self, mock_console):
        from handlers.assignment_templates import handle_assignment_templates
        success, _, _, continue_loop = handle_assignment_templates("/templates show nonexistent")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.assignment_templates.console")
    def test_templates_generate_valid(self, mock_console):
        from handlers.assignment_templates import handle_assignment_templates
        with patch("handlers.assignment_templates.get_state") as mock_get_state:
            mock_state = MagicMock()
            mock_get_state.return_value = mock_state

            success, _, _, continue_loop = handle_assignment_templates("/templates generate web_discovery")

            self.assertTrue(success)
            self.assertIsNotNone(mock_state.active_assignment)

    @patch("handlers.assignment_templates.console")
    def test_templates_generate_invalid(self, mock_console):
        from handlers.assignment_templates import handle_assignment_templates
        with patch("handlers.assignment_templates.get_state") as mock_get_state:
            mock_state = MagicMock()
            mock_get_state.return_value = mock_state

            success, _, _, continue_loop = handle_assignment_templates("/templates generate nonexistent")

            self.assertTrue(success)
            mock_console.print.assert_called()

    def test_default_templates_not_empty(self):
        from handlers.assignment_templates import DEFAULT_TEMPLATES
        self.assertGreater(len(DEFAULT_TEMPLATES), 3)

    def test_default_templates_have_required_keys(self):
        from handlers.assignment_templates import DEFAULT_TEMPLATES
        required = ["name", "category", "difficulty", "description", "objective"]
        for tid, t in DEFAULT_TEMPLATES.items():
            for key in required:
                self.assertIn(key, t, f"Template {tid} missing key: {key}")


# ── Threats Handler ───────────────────────────────────────────
class TestThreatsHandler(unittest.TestCase):
    """Tests for /threats and /groups commands."""

    @patch("handlers.threats.console")
    def test_threats_no_args(self, mock_console):
        from handlers.threats import handle_threats
        success, _, _, continue_loop = handle_threats("/threats")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called()

    @patch("handlers.threats.console")
    def test_threats_group_not_found(self, mock_console):
        from handlers.threats import handle_threats
        success, _, _, continue_loop = handle_threats("/threats nonexistent_group_xyz")

        self.assertTrue(success)
        mock_console.print.assert_called()

    @patch("handlers.threats.console")
    def test_groups_no_threats_dir(self, mock_console):
        from handlers.threats import handle_groups
        with patch("handlers.threats.THREATS_DIR", "/nonexistent/path"):
            success, _, _, continue_loop = handle_groups("/groups")

            self.assertTrue(success)
            mock_console.print.assert_called()

    @patch("handlers.threats.console")
    def test_threat_summary_llm_unavailable(self, mock_console):
        mock_raw_news = [
            {"title": "APT attack detected", "desc": "New APT group", "source": "test", "link": "http://test.com"}
        ]
        with patch("news_fetcher.fetch_news", return_value=mock_raw_news):
            with patch("config.LazyLoader.get_llm", return_value=None):
                from handlers.threats import handle_threat_summary
                success, _, _, continue_loop = handle_threat_summary("/threat summary")

                self.assertTrue(success)

    @patch("handlers.threats.console")
    def test_threat_summary_no_news(self, mock_console):
        with patch("news_fetcher.fetch_news", return_value=[]):
            from handlers.threats import handle_threat_summary
            success, _, _, continue_loop = handle_threat_summary("/threat summary")

            self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
