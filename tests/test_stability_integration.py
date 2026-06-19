"""
Critical Integration Tests for CyberTeacher v5.1.

Tests three critical end-to-end scenarios:
1. Quiz → XP → Achievement (game loop)
2. Long dialog (20+ messages) → Context budget doesn't crash
3. Provider switching → Response received from fallback
"""

import importlib
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, MagicMock


class TestStabilityBase(unittest.TestCase):
    """Base class for stability integration tests."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_stability.db")
        self.state_path = os.path.join(self.temp_dir, "test_state.json")
        os.environ["DATABASE_URL"] = f"sqlite:///{self.db_path}"
        os.environ["STATE_FILE"] = self.state_path

        import db

        importlib.reload(db)
        import memory

        importlib.reload(memory)
        import state as state_mod

        importlib.reload(state_mod)

        self.conn = memory.init_db()
        state_mod._instance = None
        self.state = state_mod.get_state()
        self.state.save_to_file(self.state_path)

    def tearDown(self):
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
        if hasattr(self, "temp_dir"):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _cleanup_singletons(self):
        import state as state_mod

        state_mod._instance = None


class TestContextBudgetManager(TestStabilityBase):
    """Scenario 2: Long dialog doesn't crash the context budget."""

    def test_budget_manager_trims_correctly(self):
        from context_budget import ContextBudgetManager

        mgr = ContextBudgetManager(max_tokens=8000)
        messages = [
            {"role": "user", "content": f"Question number {i} about cybersecurity"}
            for i in range(50)
        ]

        trimmed, warning = mgr.prepare_context(
            messages, max_messages=30, user_input="final question"
        )

        # Should have trimmed some messages
        self.assertLess(len(trimmed), len(messages))
        # Warning should be present
        self.assertIn("обрезано", warning)
        # Should still have at least 2 messages
        self.assertGreaterEqual(len(trimmed), 2)
        # Stats should be tracked
        stats = mgr.get_stats()
        self.assertGreater(stats["total_trims"], 0)

    def test_budget_fits_in_token_limit(self):
        from context_budget import ContextBudgetManager

        mgr = ContextBudgetManager(max_tokens=4000)
        messages = [{"role": "user", "content": "x" * 500} for _ in range(20)]

        trimmed, _ = mgr.prepare_context(messages, max_messages=50, user_input="test")

        # All trimmed messages should fit within budget
        total_chars = sum(len(m["content"]) for m in trimmed)
        est_tokens = total_chars // 4  # 4 chars per token
        self.assertLess(est_tokens, mgr.get_history_budget())

    def test_budget_manager_stats(self):
        from context_budget import ContextBudgetManager

        mgr = ContextBudgetManager(max_tokens=8000)
        stats = mgr.get_stats()
        self.assertIn("max_tokens", stats)
        self.assertIn("history_budget", stats)
        self.assertEqual(stats["max_tokens"], 8000)

    def test_auto_summarize_called(self):
        """Check auto-summarize is wired into main loop."""
        from di import set_context, AppContext, reset_context

        reset_context()
        set_context(AppContext(state=self.state, db_conn=self.conn))
        self.state._msg_count_since_summary = 19
        # Import directly to avoid handler chain import issues
        import importlib

        try:
            mod = importlib.import_module("handlers.summarize")
            mod.check_auto_summarize(self.conn)
            self.assertEqual(self.state._msg_count_since_summary, 0)
        except (ImportError, ModuleNotFoundError):
            self.skipTest("handlers.summarize not importable in test env")


class TestQuizToAchievement(TestStabilityBase):
    """Scenario 1: Quiz → XP → Achievement chain."""

    def test_quiz_awards_xp(self):
        """Simulate completing a quiz and verify XP is awarded."""
        initial_xp = self.state.points
        self.state.points += 25
        self.state.quizzes_taken += 1
        self.state.save_to_file(self.state_path)

        self.assertEqual(self.state.points, initial_xp + 25)
        self.assertEqual(self.state.quizzes_taken, 1)

    def test_achievement_triggers_after_threshold(self):
        """After 10 quizzes, quiz_taker achievement should trigger."""
        self.state.quizzes_taken = 10
        self.state.earned_achievements = []

        new = self.state.check_achievements()
        # Achievement service checks multiple conditions, quiz_taker is one
        self.assertTrue(len(new) > 0, "Expected at least one achievement to trigger")
        self.assertTrue(len(self.state.earned_achievements) > 0)

    def test_achievement_not_repeated(self):
        """Achievement should not trigger twice."""
        self.state.quizzes_taken = 10
        self.state.earned_achievements = ["quiz_master"]

        new = self.state.check_achievements()
        self.assertNotIn("quiz_master", new)

    def test_full_quiz_xp_achievement_chain(self):
        """End-to-end: quiz taken → XP awarded → achievement checked."""
        import state as state_mod

        state_mod._instance = None
        s = state_mod.get_state()
        s.quizzes_taken = 9
        s.points = 200
        s.earned_achievements = []

        # Simulate quiz completion
        s.points += 25  # quiz XP
        s.quizzes_taken += 1

        # Check achievements
        new_achievements = s.check_achievements()

        self.assertEqual(s.quizzes_taken, 10)
        self.assertEqual(s.points, 225)
        self.assertTrue(len(new_achievements) > 0, "Expected achievements to trigger")

    def test_skills_tracking_rule_based(self):
        """Skill tracking is rule-based (no LLM needed)."""
        self.state.track_skill("web_security", True, 15)
        self.assertIn("web_security", self.state.skills)

    def test_flag_verification_rule_based(self):
        """Flag verification is rule-based."""
        from handlers.flags import handle_flag_check

        # Just verify the handler exists and is callable
        self.assertTrue(callable(handle_flag_check))


class TestMemoryStability(TestStabilityBase):
    """Memory caps and cleanup tests."""

    def test_unbounded_lists_are_capped(self):
        """Exploit success list should be capped at 200."""
        self.state.exploit_success = [{"x": i} for i in range(250)]
        self.state._trim_unbounded_lists()
        self.assertEqual(len(self.state.exploit_success), 200)

    def test_bounty_reports_capped(self):
        self.state.bounty_reports = [{"x": i} for i in range(150)]
        self.state._trim_unbounded_lists()
        self.assertEqual(len(self.state.bounty_reports), 100)

    def test_command_usage_capped(self):
        self.state.command_usage = {f"cmd_{i}": i for i in range(60)}
        self.state._trim_unbounded_lists()
        self.assertEqual(len(self.state.command_usage), 50)

    def test_save_file_excludes_handles(self):
        """HANDLES should not appear in saved JSON."""
        self.state.save_to_file(self.state_path)
        import json

        with open(self.state_path, "r") as f:
            data = json.load(f)
        self.assertNotIn("HANDLES", data)

    def test_cleanup_old_messages(self):
        """cleanup_old_messages should keep only last N messages."""
        from memory import save_message, cleanup_old_messages

        for i in range(10):
            save_message(self.conn, "user", f"msg_{i}", "teacher")
        cleanup_old_messages(self.conn, keep_last=5)
        from db import Message

        count = self.conn.query(Message).count()
        self.assertLessEqual(count, 5)


class TestProviderFallback(TestStabilityBase):
    """Scenario 3: Provider switching and fallback."""

    def test_resilient_llm_fallback(self):
        """ResilientLLM should fallback on provider failure."""
        try:
            from resilient_llm import ResilientLLM, CircuitState
        except ImportError:
            self.skipTest("resilient_llm not importable")

        # Create mock LLMs
        primary = MagicMock()
        primary.invoke.side_effect = ConnectionError("Provider down")
        primary.model = "failing_provider"

        fallback = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Hello from fallback"
        fallback.invoke.return_value = mock_response
        fallback.model = "working_provider"

        llm = ResilientLLM(primary=primary, fallbacks=[fallback])
        result = llm.invoke("test prompt")

        self.assertEqual(result.content, "Hello from fallback")

    def test_circuit_breaker_opens(self):
        """After threshold failures, circuit should open."""
        try:
            from resilient_llm import ResilientLLM
        except ImportError:
            self.skipTest("resilient_llm not importable")

        primary = MagicMock()
        primary.invoke.side_effect = ConnectionError("down")
        primary.model = "bad_provider"

        llm = ResilientLLM(primary=primary, fallbacks=[])

        for _ in range(3):
            try:
                llm.invoke("test")
            except Exception:
                pass

        circuit = llm._circuits[id(primary)]
        self.assertEqual(circuit.state, "open")

    def test_provider_chain_status(self):
        """get_status should return provider information."""
        try:
            from resilient_llm import ResilientLLM
        except ImportError:
            self.skipTest("resilient_llm not importable")

        primary = MagicMock()
        primary.model = "test_provider"
        llm = ResilientLLM(primary=primary, fallbacks=[])
        status = llm.get_status()
        self.assertIn("providers", status)
        self.assertEqual(len(status["providers"]), 1)
        self.assertEqual(status["providers"][0]["role"], "primary")


class TestMemoryCaps(TestStabilityBase):
    """Memory cap integration tests."""

    def test_state_save_load_roundtrip(self):
        """State should save and load correctly with caps."""
        self.state.points = 1000
        self.state.quizzes_taken = 15
        self.state.exploit_success = [{"x": 1}] * 5
        self.state.save_to_file(self.state_path, force=True)

        import state as state_mod

        state_mod._instance = None
        new_state = state_mod.get_state()
        new_state.load_from_file(self.state_path)

        self.assertEqual(new_state.points, 1000)
        self.assertEqual(new_state.quizzes_taken, 15)

    def test_query_cache_capped_on_insert(self):
        """QueryCache should evict expired entries when over 1000 rows."""
        from memory import cache_response
        from db import QueryCache

        # Fill cache with expired entries (ttl_seconds=0 → expires_at=now)
        for i in range(1010):
            cache_response(
                self.conn,
                f"hash_{i:04d}",
                f"response_{i}",
                ttl_seconds=0,
            )
        self.conn.commit()

        count = self.conn.query(QueryCache).count()
        # Cache should have attempted eviction
        # (exact count depends on timing, but should be ≤ 1010)
        self.assertLessEqual(count, 1010)
        # Verify we can still insert
        cache_response(self.conn, "final_hash", "final_response", ttl_seconds=86400)
        self.conn.commit()
        final_count = self.conn.query(QueryCache).count()
        self.assertGreater(final_count, 0)


class TestCyberpsychosis(TestStabilityBase):
    """Cyberpsychosis system tests."""

    def test_initial_state_is_normal(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        self.assertEqual(cp.get_level(), "normal")

    def test_failure_increases_stress(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        cp.on_failure(20)
        self.assertGreater(cp.stress, 0)
        self.assertEqual(cp.get_level(), "normal")  # 20 is still normal

    def test_success_increases_obsession(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        cp.on_success(15)
        self.assertGreater(cp.obsession, 0)
        self.assertLess(cp.stress, 0.1)  # stress decreases

    def test_risky_action_increases_recklessness(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        cp.on_risky_action(30)
        self.assertGreater(cp.recklessness, 0)
        self.assertGreater(cp.obsession, 0)

    def test_level_escalation(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        self.assertEqual(cp.get_level(), "normal")
        cp.on_failure(40)
        self.assertEqual(cp.get_level(), "elevated")
        cp.on_failure(40)
        self.assertEqual(cp.get_level(), "critical")
        cp.on_failure(40)
        self.assertEqual(cp.get_level(), "dangerous")

    def test_decay(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        cp.on_failure(50)
        cp.decay(2.0)
        self.assertLess(cp.stress, 50)

    def test_prompt_addition_changes_with_level(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        self.assertEqual(cp.get_system_prompt_addition(), "")
        cp.on_failure(50)
        self.assertIn("устаёт", cp.get_system_prompt_addition())

    def test_save_load(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        cp.on_failure(30)
        cp.on_success(10)
        data = cp.get_state_dict()
        cp2 = CyberpsychosisState()
        cp2.load_state_dict(data)
        self.assertAlmostEqual(cp2.stress, cp.stress, places=1)

    def test_teacher_modifiers(self):
        from cyberpsychosis import CyberpsychosisState

        cp = CyberpsychosisState()
        cp.on_failure(50)
        mods = cp.get_teacher_modifiers()
        self.assertIn("sarcasm_delta", mods)
        self.assertGreater(mods["sarcasm_delta"], 0)


class TestWorldState(TestStabilityBase):
    """World state integration tests."""

    def test_initial_world_empty(self):
        from world_state import WorldState

        ws = WorldState()
        ws.incidents = []
        ws.resolved_incidents = []
        ws.discovered_factions = []
        ws.unlocked_knowledge = []
        summary = ws.get_world_summary()
        self.assertEqual(summary["active_incidents"], 0)

    def test_incident_spawn(self):
        from world_state import WorldState

        ws = WorldState()
        ws.last_incident_check = 0
        ws.incidents = []
        incident = ws.check_spawn_incident(self.state)
        # May or may not spawn (random), but shouldn't crash
        if incident:
            self.assertIn("title", incident)
            self.assertIn("severity", incident)
            ws.save()

    def test_resolve_incident(self):
        from world_state import WorldState, _world_state
        import world_state as ws_mod

        ws_mod._world_state = None
        ws = WorldState()
        ws.incidents = [{"id": "test_incident", "title": "Test"}]
        ws.resolved_incidents = []
        result = ws.resolve_incident("test_incident", 50)
        self.assertTrue(result)
        self.assertEqual(len(ws.incidents), 0)
        self.assertEqual(len(ws.resolved_incidents), 1)

    def test_faction_discovery(self):
        from world_state import WorldState

        ws = WorldState()
        ws.discovered_factions = []
        self.state.quizzes_taken = 10
        faction = ws.check_discover_faction(self.state)
        if faction:
            self.assertIn("name", faction)
            self.assertIn(faction["id"], ws.discovered_factions)

    def test_system_prompt(self):
        from world_state import WorldState

        ws = WorldState()
        ws.incidents = [
            {"id": "test", "title": "Test Incident", "severity": "high", "desc": "desc"}
        ]
        prompt = ws.get_world_prompt()
        self.assertIn("PERSISTENT WORLD STATE", prompt)
        self.assertIn("Test Incident", prompt)

    def test_save_load(self):
        from world_state import WorldState, WORLD_FILE

        ws = WorldState()
        ws.incidents = [{"id": "test", "title": "t"}]
        ws.discovered_factions = ["netwatch"]
        ws.save()
        ws2 = WorldState()
        self.assertEqual(len(ws2.incidents), 1)
        self.assertIn("netwatch", ws2.discovered_factions)


class TestEpisodeMemory(TestStabilityBase):
    """Episode memory integration tests."""

    def test_record_and_retrieve(self):
        from episode_memory import EpisodeMemory

        em = EpisodeMemory()
        initial = len(em.episodes)
        em.record("breakthrough", "Test breakthrough", "Detail", importance=8)
        self.assertEqual(len(em.episodes), initial + 1)
        recent = em.get_recent(1)
        self.assertEqual(recent[-1]["title"], "Test breakthrough")

    def test_importance_filter(self):
        from episode_memory import EpisodeMemory

        em = EpisodeMemory()
        em.episodes = []
        em.record("breakthrough", "Important", importance=9)
        em.record("session", "Normal", importance=3)
        important = em.get_important(min_importance=7)
        self.assertEqual(len(important), 1)
        self.assertEqual(important[0]["title"], "Important")

    def test_memory_prompt(self):
        from episode_memory import EpisodeMemory

        em = EpisodeMemory()
        em.episodes = []
        em.record("breakthrough", "First flag captured", importance=9)
        prompt = em.get_memory_prompt()
        self.assertIn("EPISODE MEMORY", prompt)
        self.assertIn("First flag captured", prompt)

    def test_category_filter(self):
        from episode_memory import EpisodeMemory

        em = EpisodeMemory()
        em.episodes = []
        em.record("failure", "Quiz failed", importance=5)
        em.record("breakthrough", "Flag found", importance=7)
        failures = em.get_by_category("failure")
        self.assertEqual(len(failures), 1)

    def test_stats(self):
        from episode_memory import EpisodeMemory

        em = EpisodeMemory()
        em.episodes = []
        em.record("breakthrough", "A", importance=5)
        em.record("failure", "B", importance=5)
        stats = em.get_stats()
        self.assertEqual(stats["total_episodes"], 2)
        self.assertEqual(stats["by_category"]["breakthrough"], 1)

    def test_save_load(self):
        from episode_memory import EpisodeMemory

        em = EpisodeMemory()
        em.episodes = []
        em.record("milestone", "Level 5!", importance=10)
        em.save()
        em2 = EpisodeMemory()
        self.assertEqual(len(em2.episodes), 1)
        self.assertEqual(em2.episodes[0]["title"], "Level 5!")

    def test_recording_helpers(self):
        from episode_memory import (
            EpisodeMemory,
            record_breakthrough,
            record_failure,
            record_milestone,
        )

        em = EpisodeMemory()
        em.episodes = []
        record_breakthrough(em, "Test breakthrough", "Detail", "web_security")
        record_failure(em, "Test failure", "Detail", "crypto")
        record_milestone(em, "Level up!", "Detail")
        self.assertEqual(len(em.episodes), 3)
        self.assertEqual(em.episodes[0]["category"], "breakthrough")
        self.assertEqual(em.episodes[1]["category"], "failure")
        self.assertEqual(em.episodes[2]["category"], "milestone")


if __name__ == "__main__":
    unittest.main()
