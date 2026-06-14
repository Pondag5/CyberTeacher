"""Unit tests for handlers/offline.py"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestOfflineHandler(unittest.TestCase):
    def setUp(self):
        self.state_patcher = patch("handlers.offline.get_context")
        self.mock_get_context = self.state_patcher.start()
        self.mock_ctx = MagicMock()
        self.mock_state = MagicMock()
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

    def tearDown(self):
        self.state_patcher.stop()

    @patch("handlers.offline.console.print")
    def test_offline_turn_on(self, mock_print):
        from handlers.offline import handle_offline

        result = handle_offline("/offline on")
        self.assertTrue(self.mock_state.offline_mode)
        self.assertTrue(result[0])

    @patch("handlers.offline.console.print")
    def test_offline_turn_off(self, mock_print):
        self.mock_state.offline_mode = True
        from handlers.offline import handle_offline

        result = handle_offline("/offline off")
        self.assertFalse(self.mock_state.offline_mode)
        self.assertTrue(result[0])

    @patch("handlers.offline.console.print")
    def test_offline_status(self, mock_print):
        from handlers.offline import handle_offline

        result = handle_offline("/offline")
        self.assertTrue(result[0])

    @patch("handlers.offline.console.print")
    def test_offline_status_when_enabled(self, mock_print):
        self.mock_state.offline_mode = True
        from handlers.offline import handle_offline

        result = handle_offline("/offline status")
        self.assertTrue(result[0])
