"""Unit tests for handlers/versus.py"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestVersusHandler(unittest.TestCase):
    def setUp(self):
        self.state_patcher = patch("handlers.versus.get_context")
        self.mock_get_context = self.state_patcher.start()
        self.mock_ctx = MagicMock()
        self.mock_state = MagicMock()
        self.mock_state.current_versus = None
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

    def tearDown(self):
        self.state_patcher.stop()

    def test_versus_scenarios_defined(self):
        from handlers.versus import VERSUS_SCENARIOS

        self.assertIn("web", VERSUS_SCENARIOS)
        self.assertIn("network", VERSUS_SCENARIOS)
        self.assertIn("crypto", VERSUS_SCENARIOS)
        self.assertIn("forensics", VERSUS_SCENARIOS)

    @patch("handlers.versus.console.print")
    def test_versus_list(self, mock_print):
        from handlers.versus import handle_versus

        result = handle_versus("/versus list")
        self.assertTrue(result[0])

    @patch("handlers.versus.console.print")
    def test_versus_start_unknown(self, mock_print):
        from handlers.versus import handle_versus

        result = handle_versus("/versus start unknown")
        self.assertTrue(result[0])

    @patch("handlers.versus.console.print")
    def test_versus_empty(self, mock_print):
        from handlers.versus import handle_versus

        result = handle_versus("/versus")
        self.assertTrue(result[0])

    @patch("handlers.versus.console.print")
    def test_versus_status_no_active(self, mock_print):
        from handlers.versus import handle_versus

        result = handle_versus("/versus status")
        self.assertTrue(result[0])
