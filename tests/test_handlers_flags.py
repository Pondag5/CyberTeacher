"""Unit tests for handlers/flags.py"""

import json
import os
import unittest
from unittest.mock import MagicMock, mock_open, patch


class MockState:
    """Mock AppState for testing"""

    def __init__(self):
        self.active_assignment = None
        self.total_flags_collected = 0
        self.earned_achievements = []
        self.points = 0.0
        self.assignments_completed = 0
        self.collected_flags = []

    def collect_flag(self, flag):
        if self.active_assignment:
            flags = self.active_assignment.get("flags", [])
            if flag in flags and flag not in self.collected_flags:
                self.collected_flags.append(flag)
                total_points = self.active_assignment.get("points", 0)
                per_flag = total_points // len(flags) if flags else total_points
                return True, per_flag
        return False, 0

    def is_assignment_complete(self):
        if not self.active_assignment:
            return False
        flags = self.active_assignment.get("flags", [])
        return len(self.collected_flags) >= len(flags)

    def increment_flag(self):
        self.total_flags_collected += 1

    def complete_assignment(self):
        self.assignments_completed += 1

    def check_achievements(self):
        return []


class TestHandlersFlags(unittest.TestCase):
    """Tests for handlers/flags module"""

    @patch("handlers.flags.get_context")
    @patch("handlers.flags.console.print")
    def test_handle_flag_check_no_flag(self, mock_print, mock_get_context):
        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers import flags

        result = flags.handle_flag_check(None)

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[cyan]Использование: /flag <FLAG{...}>[/cyan]")

    @patch("handlers.flags.get_context")
    @patch("handlers.flags.console.print")
    def test_handle_flag_check_invalid_format(self, mock_print, mock_get_context):
        mock_state = MockState()
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers import flags

        result = flags.handle_flag_check("invalid-flag")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[bold red]❌ Флаг 'invalid-flag' неверного формата.[/bold red]"
        )

    @patch("handlers.flags.get_context")
    @patch("memory.update_stats")
    @patch("memory.init_db")
    @patch("handlers.flags.console.print")
    def test_handle_flag_check_active_assignment_success(
        self, mock_print, mock_init_db, mock_update_stats, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = {
            "flags": ["FLAG{test1}", "FLAG{test2}"],
            "points": 20,
        }
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_conn = MagicMock()
        mock_init_db.return_value = mock_conn

        from handlers import flags

        result = flags.handle_flag_check("FLAG{test1}")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[bold green]✅ Флаг найден в активном задании! +10 очков[/bold green]"
        )
        self.assertEqual(mock_state.total_flags_collected, 1)
        self.assertIn("FLAG{test1}", mock_state.collected_flags)

    @patch("handlers.flags.get_context")
    @patch("memory.update_stats")
    @patch("memory.init_db")
    @patch("handlers.flags.console.print")
    def test_handle_flag_check_active_assignment_completes_task(
        self, mock_print, mock_init_db, mock_update_stats, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = {"flags": ["FLAG{onlyone}"], "points": 10}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_conn = MagicMock()
        mock_init_db.return_value = mock_conn

        from handlers import flags

        result = flags.handle_flag_check("FLAG{onlyone}")

        self.assertEqual(result, (True, None, None, True))
        self.assertEqual(mock_state.assignments_completed, 1)
        mock_print.assert_any_call(
            "[bold cyan]🎉 Задание завершено! Все флаги собраны.[/bold cyan]"
        )

    @patch("handlers.flags.get_context")
    @patch("handlers.flags.console.print")
    def test_handle_flag_check_active_assignment_failure(
        self, mock_print, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = {"flags": ["FLAG{correct}"]}
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx

        from handlers import flags

        result = flags.handle_flag_check("FLAG{wrong}")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[bold red]❌ Флаг 'FLAG{wrong}' неверный.[/bold red]"
        )

    @patch("handlers.flags.get_context")
    @patch("handlers.flags.console.print")
    @patch("os.path.exists")
    def test_handle_flag_check_global_flags_file_missing(
        self, mock_exists, mock_print, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = None
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_exists.return_value = False

        from handlers import flags

        result = flags.handle_flag_check("FLAG{any}")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[yellow]База флагов не найдена. Создайте data/flags.json[/yellow]"
        )

    @patch("handlers.flags.get_context")
    @patch("memory.update_stats")
    @patch("memory.init_db")
    @patch("handlers.flags.console.print")
    @patch("os.path.exists")
    def test_handle_flag_check_global_flags_success(
        self, mock_exists, mock_print, mock_init_db, mock_update_stats, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = None
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_conn = MagicMock()
        mock_init_db.return_value = mock_conn
        mock_exists.return_value = True

        from handlers import flags

        with patch(
            "builtins.open",
            mock_open(read_data='{"flags": [{"flag": "FLAG{global1}", "points": 15}]}'),
        ):
            result = flags.handle_flag_check("FLAG{global1}")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call("[bold green]✅ Флаг верный! +15 очков[/bold green]")
        self.assertEqual(mock_state.total_flags_collected, 1)

    @patch("handlers.flags.get_context")
    @patch("handlers.flags.console.print")
    @patch("os.path.exists")
    def test_handle_flag_check_global_flags_not_found(
        self, mock_exists, mock_print, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = None
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_exists.return_value = True

        from handlers import flags

        with patch(
            "builtins.open",
            mock_open(read_data='{"flags": [{"flag": "FLAG{other}", "points": 10}]}'),
        ):
            result = flags.handle_flag_check("FLAG{miss}")

        self.assertEqual(result, (True, None, None, True))
        mock_print.assert_any_call(
            "[bold red]❌ Флаг 'FLAG{miss}' неверный.[/bold red]"
        )

    @patch("handlers.flags.get_context")
    @patch("handlers.flags.console.print")
    @patch("os.path.exists")
    def test_handle_flag_check_global_flags_json_error(
        self, mock_exists, mock_print, mock_get_context
    ):
        mock_state = MockState()
        mock_state.active_assignment = None
        mock_ctx = MagicMock()
        mock_ctx.state = mock_state
        mock_get_context.return_value = mock_ctx
        mock_exists.return_value = True

        from handlers import flags

        with (
            patch("builtins.open", mock_open(read_data="{invalid}")),
            patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)),
        ):
            result = flags.handle_flag_check("FLAG{any}")

        self.assertEqual(result, (True, None, None, True))
        self.assertTrue(
            any("Ошибка" in str(call_arg) for call_arg in mock_print.call_args_list)
        )


if __name__ == "__main__":
    unittest.main()
