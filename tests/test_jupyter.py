"""Тесты для модуля Jupyter Notebook Support (M-12)."""

import unittest
from unittest.mock import MagicMock, patch

from handlers.jupyter import (
    NOTEBOOK_TEMPLATES,
    _open_notebook,
    _run_cell,
    _submit_notebook,
    handle_jupyter,
)


class TestJupyter(unittest.TestCase):
    """Тесты Jupyter Notebook."""

    def test_display_notebooks(self):
        """Отображение списка шаблонов."""
        with patch("handlers.jupyter.console.print"):
            result, action_taken = handle_jupyter("")
            self.assertTrue(action_taken)

    def test_open_valid_notebook(self):
        """Открытие существующего ноутбука."""
        with patch("handlers.jupyter.console.print"):
            success = _open_notebook("crypto_basics")
            self.assertTrue(success)

    def test_open_invalid_notebook(self):
        """Открытие несуществующего ноутбука."""
        with patch("handlers.jupyter.console.print"):
            success = _open_notebook("nonexistent")
            self.assertFalse(success)

    def test_run_cell(self):
        """Выполнение ячейки."""
        with patch("handlers.jupyter.console.print"):
            with patch("handlers.jupyter.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_notebook = "crypto_basics"
                mock_state.completed_cells = []
                mock_state.xp = 0
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _run_cell(1)
                self.assertTrue(success)

    def test_run_cell_invalid_id(self):
        """Выполнение ячейки с неверным ID."""
        with patch("handlers.jupyter.console.print"):
            with patch("handlers.jupyter.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_notebook = "crypto_basics"
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _run_cell(99)
                self.assertFalse(success)

    def test_run_cell_without_notebook(self):
        """Выполнение ячейки без открытого ноутбука."""
        with patch("handlers.jupyter.console.print"):
            with patch("handlers.jupyter.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_notebook = None
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _run_cell(1)
                self.assertFalse(success)

    def test_submit_complete(self):
        """Отправка завершённого ноутбука."""
        with patch("handlers.jupyter.console.print"):
            with patch("handlers.jupyter.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_notebook = "crypto_basics"
                mock_state.completed_cells = [1, 2, 3]
                mock_state.xp = 0
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _submit_notebook()
                self.assertTrue(success)

    def test_submit_incomplete(self):
        """Отправка незавершённого ноутбука."""
        with patch("handlers.jupyter.console.print"):
            with patch("handlers.jupyter.get_context") as mock_get_context:
                mock_state = MagicMock()
                mock_state.current_notebook = "crypto_basics"
                mock_state.completed_cells = [1]
                mock_ctx = MagicMock()
                mock_ctx.state = mock_state
                mock_get_context.return_value = mock_ctx
                success = _submit_notebook()
                self.assertFalse(success)

    def test_help_command(self):
        """Вызов справки /jupyter help."""
        with patch("handlers.jupyter.console.print"):
            result, action_taken = handle_jupyter("help")
            self.assertTrue(action_taken)

    def test_unknown_subcommand(self):
        """Неизвестная подкоманда."""
        with patch("handlers.jupyter.console.print"):
            result, action_taken = handle_jupyter("unknown")
            self.assertTrue(action_taken)

    def test_notebooks_structure(self):
        """Проверка структуры шаблонов."""
        self.assertGreater(len(NOTEBOOK_TEMPLATES), 0)
        for nid, nb in NOTEBOOK_TEMPLATES.items():
            self.assertIn("title", nb)
            self.assertIn("description", nb)
            self.assertIn("cells", nb)
            self.assertIn("xp", nb)
            self.assertIsInstance(nb["cells"], list)


if __name__ == "__main__":
    unittest.main()
