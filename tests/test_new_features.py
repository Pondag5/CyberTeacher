"""Тесты для L-03, L-14, L-16, H-16."""

import unittest
from unittest.mock import patch

from handlers.mindmap import TOPIC_TREE, handle_mindmap
from handlers.registry import CommandRegistry, registry


class TestMindMap(unittest.TestCase):
    """Тесты mind map."""

    def test_mindmap_all(self):
        """Отображение полной карты."""
        with patch("handlers.mindmap.console.print"):
            result, action_taken = handle_mindmap("")
            self.assertTrue(action_taken)

    def test_mindmap_topic(self):
        """Отображение конкретной темы."""
        with patch("handlers.mindmap.console.print"):
            result, action_taken = handle_mindmap("Web Security")
            self.assertTrue(action_taken)

    def test_mindmap_help(self):
        """Справка."""
        with patch("handlers.mindmap.console.print"):
            result, action_taken = handle_mindmap("help")
            self.assertTrue(action_taken)

    def test_topic_tree_structure(self):
        """Проверка структуры дерева тем."""
        self.assertIn("CyberSecurity", TOPIC_TREE)
        self.assertGreater(len(TOPIC_TREE), 0)
        for topic, children in TOPIC_TREE.items():
            self.assertIsInstance(children, list)


class TestRegistry(unittest.TestCase):
    """Тесты registry pattern."""

    def test_register_exact(self):
        """Регистрация точной команды."""
        reg = CommandRegistry()

        @reg.register_exact("test")
        def handler(action):
            return "ok", True

        func, remaining = reg.get_handler("test")
        self.assertIsNotNone(func)
        self.assertEqual(remaining, "")

    def test_register_prefix(self):
        """Регистрация команды с префиксом."""
        reg = CommandRegistry()

        @reg.register_prefix("test ")
        def handler(action):
            return "ok", True

        func, remaining = reg.get_handler("test arg")
        self.assertIsNotNone(func)
        self.assertEqual(remaining, "arg")

    def test_not_found(self):
        """Команда не найдена."""
        func, remaining = registry.get_handler("nonexistent_command")
        self.assertIsNone(func)

    def test_list_commands(self):
        """Список команд."""
        commands = registry.list_commands()
        self.assertIsInstance(commands, dict)
        self.assertGreater(len(commands), 0)


class TestAsyncHandler(unittest.TestCase):
    """Тесты асинхронных обработчиков."""

    def test_run_async_query_no_llm(self):
        """Асинхронный запрос без LLM."""
        with patch("handlers.async_handler.async_rag_search", return_value="rag"):
            with patch("handlers.async_handler.async_llm_call", return_value="llm"):
                from handlers.async_handler import run_async_query
                result = run_async_query("test", None, None)
                self.assertIn("rag_result", result)
                self.assertIn("llm_result", result)
                self.assertIn("combined_response", result)


if __name__ == "__main__":
    unittest.main()
