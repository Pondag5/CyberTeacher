"""Unit tests for handlers/practice.py"""

import unittest
from unittest.mock import MagicMock, patch


class MockState:
    def __init__(self):
        self.labs_started = 0
        self.earned_achievements = []
        self.hints_used = 0
        self.trace_deadline = None
        self.trace_hint = None

    def start_lab(self):
        self.labs_started += 1

    def check_achievements(self):
        return []


class TestHandlersPractice(unittest.TestCase):
    """Tests for handlers/practice module"""

    @patch("handlers.practice.get_context")
    @patch("handlers.practice.console.print")
    def test_handle_practice_list(self, mock_print, mock_get_context):
        """Test /practice or /lab shows list of labs"""
        from handlers import practice

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = practice.handle_practice("practice")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_called()

    @patch("handlers.practice.get_context")
    @patch("handlers.practice.console.print")
    def test_handle_practice_start(self, mock_print, mock_get_context):
        """Test /lab start <name> starts lab"""
        from handlers import practice

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = practice.handle_practice("lab start mylab")

        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.practice.get_context")
    @patch("handlers.practice.console.print")
    def test_handle_practice_stop(self, mock_print, mock_get_context):
        """Test /lab stop <name> stops lab"""
        from handlers import practice

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = practice.handle_practice("lab stop mylab")

        self.assertEqual(result, (True, None, None, True))

    @patch("handlers.practice.get_context")
    @patch("handlers.practice.console.print")
    @patch("practice.get_all_running_labs")
    def test_handle_practice_status_with_labs(
        self, mock_get_running, mock_print, mock_get_context
    ):
        """Test /lab status shows running labs"""
        from handlers import practice

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_get_running.return_value = {
            "lab1": {"name": "Lab 1", "status": "running"},
            "lab2": {"name": "Lab 2", "status": "running"},
        }

        result = practice.handle_practice("lab status")

        self.assertEqual(result, (True, None, None, True))
        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Lab 1", printed)
        self.assertIn("Lab 2", printed)

    @patch("handlers.practice.get_context")
    @patch("handlers.practice.console.print")
    @patch("practice.get_all_running_labs")
    def test_handle_practice_status_no_labs(
        self, mock_get_running, mock_print, mock_get_context
    ):
        """Test /lab status shows no labs message when empty"""
        from handlers import practice

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_get_running.return_value = {}

        result = practice.handle_practice("lab status")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Нет запущенных лабораторий[/yellow]")

    @patch("handlers.practice.get_context")
    @patch("handlers.practice.console.print")
    def test_handle_practice_usage(self, mock_print, mock_get_context):
        """Test /practice with invalid args shows usage"""
        from handlers import practice

        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        result = practice.handle_practice("practice unknown")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[cyan]Использование:[/cyan]")

    @patch("handlers.practice.console.print")
    @patch("practice.get_all_running_labs")
    def test_handle_container_check_with_labs(self, mock_get_running, mock_print):
        """Test /container check shows running containers"""
        from handlers import practice

        mock_get_running.return_value = {
            "container1": {"name": "Container 1", "status": "healthy"}
        }

        result = practice.handle_container_check("")

        self.assertEqual(result, (True, None, None, True))
        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Container 1", printed)

    @patch("handlers.practice.console.print")
    @patch("practice.get_all_running_labs")
    def test_handle_container_check_no_labs(self, mock_get_running, mock_print):
        """Test /container check shows no containers message"""
        from handlers import practice

        mock_get_running.return_value = {}

        result = practice.handle_container_check("")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[yellow]Нет запущенных контейнеров[/yellow]")


if __name__ == "__main__":
    unittest.main()
