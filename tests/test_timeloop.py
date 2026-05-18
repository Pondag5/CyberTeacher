"""Тесты для модуля Time Loop (M-18)."""

import unittest
from unittest.mock import MagicMock, patch

from handlers.timeloop import (
    STORY_NODES,
    _make_choice,
    _reset_timeloop,
    _start_timeloop,
    handle_timeloop,
)


class TestTimeLoop(unittest.TestCase):
    """Тесты временной петли."""

    def test_start_timeloop(self):
        """Начало временной петли."""
        with patch("handlers.timeloop.console.print"):
            with patch("handlers.timeloop.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_node = None
                mock_state.loop_count = 0
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                _start_timeloop()
                self.assertEqual(mock_state.current_node, "start")

    def test_make_choice_valid(self):
        """Валидный выбор."""
        with patch("handlers.timeloop.console.print"):
            with patch("handlers.timeloop.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_node = "start"
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                _make_choice("1")
                self.assertEqual(mock_state.current_node, "check_logs")

    def test_make_choice_invalid(self):
        """Невалидный выбор."""
        with patch("handlers.timeloop.console.print"):
            with patch("handlers.timeloop.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_node = "start"
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                _make_choice("9")
                # Узел не должен измениться
                self.assertEqual(mock_state.current_node, "start")

    def test_make_choice_without_node(self):
        """Выбор без начатой петли."""
        with patch("handlers.timeloop.console.print"):
            with patch("handlers.timeloop.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_node = None
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                _make_choice("1")
                # Должно показать предупреждение

    def test_reset_timeloop(self):
        """Сброс петли."""
        with patch("handlers.timeloop.console.print"):
            with patch("handlers.timeloop.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_node = "check_logs"
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                _reset_timeloop()
                self.assertIsNone(mock_state.current_node)

    def test_help_command(self):
        """Вызов справки /timeloop help."""
        with patch("handlers.timeloop.console.print"):
            result, action_taken = handle_timeloop("help")
            self.assertTrue(action_taken)

    def test_unknown_subcommand(self):
        """Неизвестная подкоманда."""
        with patch("handlers.timeloop.console.print"):
            result, action_taken = handle_timeloop("unknown")
            self.assertTrue(action_taken)

    def test_story_nodes_structure(self):
        """Проверка структуры узлов сюжета."""
        self.assertGreater(len(STORY_NODES), 0)
        for nid, node in STORY_NODES.items():
            self.assertIn("text", node)
            # Узел должен иметь либо choices, либо ending
            self.assertTrue("choices" in node or "ending" in node)


if __name__ == "__main__":
    unittest.main()
