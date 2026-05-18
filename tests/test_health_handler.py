"""
Tests for health handler.
"""

import unittest
from unittest.mock import MagicMock, patch

from di import AppContext


class TestHealthHandler(unittest.TestCase):
    """Tests for /health command handler."""

    @patch("handlers.health.get_context")
    @patch("handlers.health.console")
    def test_health_returns_success(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.start_time = 0
        mock_state.llm_call_count = 10
        mock_state.llm_total_time = 5.0
        mock_state.llm_total_tokens = 1000
        mock_state.cache_hits = 8
        mock_state.cache_misses = 2
        mock_state.current_mode = "teacher"
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        from handlers.health import handle_health
        success, _, _, continue_loop = handle_health("/health")

        self.assertTrue(success)
        self.assertTrue(continue_loop)
        mock_console.print.assert_called_once()

    @patch("handlers.health.get_context")
    @patch("handlers.health.console")
    def test_health_zero_cache_division(self, mock_console, mock_get_context):
        mock_state = MagicMock()
        mock_state.start_time = 0
        mock_state.llm_call_count = 0
        mock_state.llm_total_time = 0.0
        mock_state.llm_total_tokens = 0
        mock_state.cache_hits = 0
        mock_state.cache_misses = 0
        mock_state.current_mode = "ctf"
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        from handlers.health import handle_health
        success, _, _, continue_loop = handle_health("/health")

        self.assertTrue(success)
        mock_console.print.assert_called_once()

    @patch("handlers.health.get_context")
    @patch("handlers.health.console")
    def test_health_uptime_calculation(self, mock_console, mock_get_context):
        import time
        mock_state = MagicMock()
        mock_state.start_time = time.time() - 3661  # 1h 1m 1s
        mock_state.llm_call_count = 5
        mock_state.llm_total_time = 2.5
        mock_state.llm_total_tokens = 500
        mock_state.cache_hits = 3
        mock_state.cache_misses = 2
        mock_state.current_mode = "expert"
        mock_ctx = AppContext(state=mock_state)
        mock_get_context.return_value = mock_ctx

        from handlers.health import handle_health
        handle_health("/health")

        mock_console.print.assert_called_once()


if __name__ == "__main__":
    unittest.main()
