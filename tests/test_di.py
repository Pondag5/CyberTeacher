"""
Tests for Dependency Injection container.
"""

import unittest
from unittest.mock import MagicMock, patch

from di import AppContext, get_context, inject, reset_context, set_context


class TestAppContext(unittest.TestCase):
    """Tests for AppContext DI container."""

    def setUp(self):
        reset_context()

    def tearDown(self):
        reset_context()

    def test_get_context_creates_instance(self):
        ctx = get_context()
        self.assertIsInstance(ctx, AppContext)

    def test_get_context_returns_singleton(self):
        ctx1 = get_context()
        ctx2 = get_context()
        self.assertIs(ctx1, ctx2)

    def test_set_context_replaces_instance(self):
        custom_ctx = AppContext()
        set_context(custom_ctx)
        self.assertIs(get_context(), custom_ctx)

    def test_reset_context_clears_instance(self):
        ctx1 = get_context()
        reset_context()
        ctx2 = get_context()
        self.assertIsNot(ctx1, ctx2)

    def test_context_has_state(self):
        ctx = get_context()
        self.assertIsNotNone(ctx.state)

    def test_context_has_settings(self):
        ctx = get_context()
        self.assertIsNotNone(ctx.settings)

    def test_context_db_conn_default_none(self):
        ctx = get_context()
        self.assertIsNone(ctx.db_conn)

    def test_context_get_llm_returns_none_when_unavailable(self):
        ctx = get_context()
        with patch("config.LazyLoader.get_llm", return_value=None):
            llm = ctx.get_llm()
            self.assertIsNone(llm)

    def test_context_get_knowledge_base(self):
        ctx = get_context()
        # Mock the knowledge module at the import location
        import sys
        mock_kb = MagicMock()
        with patch.dict(sys.modules, {"knowledge": mock_kb}):
            mock_kb.KnowledgeBase.return_value = MagicMock()
            # Force re-import by clearing cache
            ctx._knowledge_base = None
            kb = ctx.get_knowledge_base()
            self.assertIsNotNone(kb)

    def test_context_save_state(self):
        ctx = get_context()
        ctx.state.save_to_file = MagicMock()
        ctx.save_state()
        ctx.state.save_to_file.assert_called_once()


class TestInjectDecorator(unittest.TestCase):
    """Tests for @inject decorator."""

    def setUp(self):
        reset_context()

    def tearDown(self):
        reset_context()

    def test_inject_passes_context(self):
        @inject
        def test_handler(ctx, action):
            return True, ctx.state, None, True

        result = test_handler("/test")
        self.assertTrue(result[0])
        self.assertTrue(result[3])
        self.assertIsNotNone(result[1])

    def test_inject_preserves_function_name(self):
        @inject
        def my_handler(ctx, action):
            return True, None, None, True

        self.assertEqual(my_handler.__name__, "my_handler")


class TestContextIntegration(unittest.TestCase):
    """Integration tests for DI with state and settings."""

    def setUp(self):
        reset_context()

    def tearDown(self):
        reset_context()

    def test_context_state_properties(self):
        ctx = get_context()
        # Should be able to access state properties
        self.assertIsNotNone(ctx.state.current_mode)

    def test_context_settings_properties(self):
        ctx = get_context()
        # Should be able to access settings
        self.assertIsNotNone(ctx.settings.llm_provider)


if __name__ == "__main__":
    unittest.main()
