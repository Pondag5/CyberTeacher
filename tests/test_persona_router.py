"""Tests for persona_router.py — dynamic persona selection."""

import unittest
from unittest.mock import MagicMock, patch

from state import AppState


class TestPersonaRouter(unittest.TestCase):
    def setUp(self):
        self.state = AppState()
        from persona_router import (
            list_personas,
            get_preferred_persona,
            set_preferred_persona,
            get_persona_prompt,
            get_persona_info,
            select_persona,
        )

        self.list_personas = list_personas
        self.get_preferred_persona = get_preferred_persona
        self.set_preferred_persona = set_preferred_persona
        self.get_persona_prompt = get_persona_prompt
        self.get_persona_info = get_persona_info
        self.select_persona = select_persona

    def test_list_personas_returns_four(self):
        personas = self.list_personas()
        self.assertEqual(len(personas), 4)
        ids = {p["id"] for p in personas}
        self.assertEqual(ids, {"rick", "doc", "analyst", "ghost"})

    def test_default_preferred_is_auto(self):
        self.assertEqual(self.get_preferred_persona(), "auto")

    def test_set_preferred_persona(self):
        self.assertTrue(self.set_preferred_persona("ghost"))
        self.assertEqual(self.get_preferred_persona(), "ghost")
        self.assertTrue(self.set_preferred_persona("auto"))
        self.assertEqual(self.get_preferred_persona(), "auto")
        self.assertFalse(self.set_preferred_persona("invalid"))

    def test_get_persona_info(self):
        info = self.get_persona_info("rick")
        self.assertEqual(info["id"], "rick")
        self.assertEqual(info["name"], "Rick")
        self.assertEqual(info["emoji"], "🧪")

    def test_get_persona_prompt_contains_persona_tag(self):
        prompt = self.get_persona_prompt("rick")
        self.assertIn("[PERSONA: RICK]", prompt)
        prompt = self.get_persona_prompt("doc")
        self.assertIn("[PERSONA: DOC]", prompt)

    def test_select_persona_forced(self):
        self.assertEqual(self.select_persona(self.state, "", forced="ghost"), "ghost")
        self.assertEqual(self.select_persona(self.state, "", forced="doc"), "doc")

    def test_select_persona_preferred(self):
        self.set_preferred_persona("analyst")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": False,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": False,
                "is_night": False,
            }
            # Use global state since set_preferred_persona saves there
            from state import get_state

            global_state = get_state()
            self.assertEqual(self.select_persona(global_state, ""), "analyst")

    def test_select_persona_auto_high_risk(self):
        self.set_preferred_persona("auto")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": True,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": False,
                "is_night": False,
            }
            self.assertEqual(self.select_persona(self.state, ""), "ghost")

    def test_select_persona_auto_stealth(self):
        self.set_preferred_persona("auto")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": False,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": True,
                "is_night": False,
            }
            self.assertEqual(self.select_persona(self.state, ""), "ghost")

    def test_select_persona_auto_late_night(self):
        self.set_preferred_persona("auto")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": False,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": False,
                "is_night": True,
            }
            self.assertEqual(self.select_persona(self.state, ""), "doc")

    def test_select_persona_auto_chaos_keywords(self):
        self.set_preferred_persona("auto")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": False,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": False,
                "is_night": False,
            }
            self.assertEqual(
                self.select_persona(self.state, "run exploit brute force scan"), "rick"
            )

    def test_select_persona_auto_learning_keywords(self):
        self.set_preferred_persona("auto")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": False,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": False,
                "is_night": False,
            }
            self.assertEqual(
                self.select_persona(self.state, "quiz me on this topic"), "doc"
            )

    def test_select_persona_default_fallback(self):
        self.set_preferred_persona("auto")
        with patch("persona_router._get_context_hints") as mock_ctx:
            mock_ctx.return_value = {
                "risk_high": False,
                "noise_high": False,
                "cp_high": False,
                "stealth_on": False,
                "is_night": False,
            }
            self.assertEqual(self.select_persona(self.state, "hello"), "rick")


if __name__ == "__main__":
    unittest.main()
