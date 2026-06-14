"""Unit tests for handlers/mood.py"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestMoodHandler(unittest.TestCase):
    def setUp(self):
        self.state_patcher = patch("handlers.mood.get_context")
        self.mock_get_context = self.state_patcher.start()
        self.mock_ctx = MagicMock()
        self.mock_state = MagicMock()
        self.mock_state.communication_mood = "normal"
        self.mock_ctx.state = self.mock_state
        self.mock_get_context.return_value = self.mock_ctx

    def tearDown(self):
        self.state_patcher.stop()

    @patch("handlers.mood.console.print")
    def test_mood_list(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood list")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_set_normal(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood normal")
        self.assertEqual(self.mock_state.communication_mood, "normal")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_set_hacker(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood hacker")
        self.assertEqual(self.mock_state.communication_mood, "hacker")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_set_formal(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood formal")
        self.assertEqual(self.mock_state.communication_mood, "formal")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_set_casual(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood casual")
        self.assertEqual(self.mock_state.communication_mood, "casual")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_set_minimal(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood minimal")
        self.assertEqual(self.mock_state.communication_mood, "minimal")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_invalid(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood nonexistent")
        self.assertEqual(self.mock_state.communication_mood, "normal")
        self.assertTrue(result[0])

    @patch("handlers.mood.console.print")
    def test_mood_defaults_to_list(self, mock_print):
        from handlers.mood import handle_mood

        result = handle_mood("/mood")
        self.assertTrue(result[0])

    def test_get_mood_prompt_modifier_default(self):
        from handlers.mood import get_mood_prompt_modifier

        modifier = get_mood_prompt_modifier()
        self.assertIn("понятным", modifier)

    def test_get_mood_prompt_modifier_hacker(self):
        self.mock_state.communication_mood = "hacker"
        from handlers.mood import get_mood_prompt_modifier

        modifier = get_mood_prompt_modifier()
        self.assertIn("сленге", modifier)

    def test_get_mood_prompt_modifier_formal(self):
        self.mock_state.communication_mood = "formal"
        from handlers.mood import get_mood_prompt_modifier

        modifier = get_mood_prompt_modifier()
        self.assertIn("академическим", modifier)
