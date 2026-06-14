"""Tests for handlers/event_engine.py — narrative event system."""

import json
import os
import tempfile
import time
import unittest
from unittest.mock import patch, MagicMock


# Apply event_engine_path patching before import
# We patch EVENTS_PATH to a temp file in setUp, but the module-level
# EVENTS_PATH is set at import time. To control it, we patch after import.
class TestEventEngine(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.events_file = os.path.join(self.tmpdir, "narrative_events.json")
        self._write_events([])
        # Clean singleton state between tests
        from state import get_state

        state = get_state()
        state.fired_events = []

    def _write_events(self, events):
        with open(self.events_file, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False)

    def _get_engine(self):
        """Import and return event_engine module with patched EVENTS_PATH."""
        import importlib
        import handlers.event_engine as ee

        importlib.reload(ee)
        ee.EVENTS_PATH = self.events_file
        return ee

    # --- Loading ---

    def test_load_events_empty(self):
        ee = self._get_engine()
        self.assertEqual(ee.load_events(), [])

    def test_load_events_missing_file(self):
        os.remove(self.events_file)
        ee = self._get_engine()
        self.assertEqual(ee.load_events(), [])

    def test_load_events_bad_json(self):
        with open(self.events_file, "w") as f:
            f.write("not json")
        ee = self._get_engine()
        self.assertEqual(ee.load_events(), [])

    def test_load_events_success(self):
        events = [{"id": "test_event", "title": "Test"}]
        self._write_events(events)
        ee = self._get_engine()
        self.assertEqual(ee.load_events(), events)

    # --- Metric resolution ---

    def test_resolve_metric_xp(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 150
        self.assertEqual(ee._resolve_metric("xp"), 150)

    def test_resolve_metric_stealth_ops(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.stealth_ops = 5
        self.assertEqual(ee._resolve_metric("stealth_ops"), 5)

    def test_resolve_metric_digital_debts(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.digital_debts = 3
        self.assertEqual(ee._resolve_metric("digital_debts"), 3)

    def test_resolve_metric_dirty_logs(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.dirty_logs = [{"source": "a"}, {"source": "b"}]
        self.assertEqual(ee._resolve_metric("dirty_logs"), 2)

    def test_resolve_metric_flags_captured(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.flags_captured = 10
        self.assertEqual(ee._resolve_metric("flags_captured"), 10)

    def test_resolve_metric_current_chapter(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.current_chapter = 3
        self.assertEqual(ee._resolve_metric("current_chapter"), 3)

    def test_resolve_metric_noise_level(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.noise_level = 25
        self.assertEqual(ee._resolve_metric("noise_level"), 25)

    def test_resolve_metric_achievements_count(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.earned_achievements = ["ach1", "ach2", "ach3"]
        self.assertEqual(ee._resolve_metric("achievements_count"), 3)

    def test_resolve_metric_night_sessions_default(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        # night_sessions may not be set — should return 0
        val = ee._resolve_metric("night_sessions")
        self.assertIsInstance(val, (int, float))

    def test_resolve_metric_trace_default(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        val = ee._resolve_metric("trace")
        self.assertIsInstance(val, (int, float))

    def test_resolve_metric_unknown(self):
        ee = self._get_engine()
        self.assertEqual(ee._resolve_metric("nonexistent"), 0)

    # --- Trigger evaluation ---

    def test_trigger_threshold_ge_true(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 100
        self.assertTrue(
            ee._check_trigger(
                {"type": "threshold", "metric": "xp", "op": ">=", "value": 100}
            )
        )

    def test_trigger_threshold_ge_false(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 99
        self.assertFalse(
            ee._check_trigger(
                {"type": "threshold", "metric": "xp", "op": ">=", "value": 100}
            )
        )

    def test_trigger_threshold_le_true(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.digital_debts = 0
        self.assertTrue(
            ee._check_trigger(
                {"type": "threshold", "metric": "digital_debts", "op": "<=", "value": 0}
            )
        )

    def test_trigger_threshold_gt(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.stealth_ops = 11
        self.assertTrue(
            ee._check_trigger(
                {"type": "threshold", "metric": "stealth_ops", "op": ">", "value": 10}
            )
        )

    def test_trigger_threshold_lt(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.noise_level = 5
        self.assertTrue(
            ee._check_trigger(
                {"type": "threshold", "metric": "noise_level", "op": "<", "value": 10}
            )
        )

    def test_trigger_threshold_eq(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.current_chapter = 3
        self.assertTrue(
            ee._check_trigger(
                {
                    "type": "threshold",
                    "metric": "current_chapter",
                    "op": "==",
                    "value": 3,
                }
            )
        )

    def test_trigger_and_both_true(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.current_chapter = 3
        state.stealth_ops = 2
        self.assertTrue(
            ee._check_trigger(
                {
                    "type": "and",
                    "triggers": [
                        {
                            "type": "threshold",
                            "metric": "current_chapter",
                            "op": ">=",
                            "value": 3,
                        },
                        {
                            "type": "threshold",
                            "metric": "stealth_ops",
                            "op": ">=",
                            "value": 2,
                        },
                    ],
                }
            )
        )

    def test_trigger_and_one_false(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.current_chapter = 3
        state.stealth_ops = 1
        self.assertFalse(
            ee._check_trigger(
                {
                    "type": "and",
                    "triggers": [
                        {
                            "type": "threshold",
                            "metric": "current_chapter",
                            "op": ">=",
                            "value": 3,
                        },
                        {
                            "type": "threshold",
                            "metric": "stealth_ops",
                            "op": ">=",
                            "value": 2,
                        },
                    ],
                }
            )
        )

    def test_trigger_or_one_true(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 100
        state.stealth_ops = 0
        self.assertTrue(
            ee._check_trigger(
                {
                    "type": "or",
                    "triggers": [
                        {"type": "threshold", "metric": "xp", "op": ">=", "value": 100},
                        {
                            "type": "threshold",
                            "metric": "stealth_ops",
                            "op": ">=",
                            "value": 10,
                        },
                    ],
                }
            )
        )

    def test_trigger_or_all_false(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 50
        state.stealth_ops = 0
        self.assertFalse(
            ee._check_trigger(
                {
                    "type": "or",
                    "triggers": [
                        {"type": "threshold", "metric": "xp", "op": ">=", "value": 100},
                        {
                            "type": "threshold",
                            "metric": "stealth_ops",
                            "op": ">=",
                            "value": 10,
                        },
                    ],
                }
            )
        )

    def test_trigger_unknown_type(self):
        ee = self._get_engine()
        self.assertFalse(
            ee._check_trigger({"type": "invalid_type", "metric": "xp", "value": 10})
        )

    # --- Condition evaluation ---

    def test_conditions_no_condition(self):
        ee = self._get_engine()
        self.assertTrue(ee._check_conditions({}, [], 12))

    def test_conditions_not_fired_pass(self):
        ee = self._get_engine()
        self.assertTrue(
            ee._check_conditions({"not_fired": ["event_a"]}, ["event_b"], 12)
        )

    def test_conditions_not_fired_fail(self):
        ee = self._get_engine()
        self.assertFalse(
            ee._check_conditions({"not_fired": ["event_a"]}, ["event_a", "event_b"], 12)
        )

    def test_conditions_fired_before_pass(self):
        ee = self._get_engine()
        self.assertTrue(
            ee._check_conditions(
                {"fired_before": ["event_a"]}, ["event_a", "event_b"], 12
            )
        )

    def test_conditions_fired_before_fail(self):
        ee = self._get_engine()
        self.assertFalse(
            ee._check_conditions({"fired_before": ["event_c"]}, ["event_a"], 12)
        )

    def test_conditions_time_window_min(self):
        ee = self._get_engine()
        self.assertFalse(ee._check_conditions({"min_hour": 23}, ["event_a"], 12))
        self.assertTrue(ee._check_conditions({"min_hour": 10}, ["event_a"], 12))

    def test_conditions_time_window_max(self):
        ee = self._get_engine()
        self.assertFalse(ee._check_conditions({"max_hour": 10}, ["event_a"], 12))
        self.assertTrue(ee._check_conditions({"max_hour": 23}, ["event_a"], 12))

    # --- Fired events tracking ---

    def test_get_fired_events_default(self):
        ee = self._get_engine()
        from state import get_state

        self.assertEqual(ee.get_fired_events(), [])

    def test_mark_event_fired(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        ee.mark_event_fired("test_event")
        self.assertIn("test_event", ee.get_fired_events())

    def test_mark_event_fired_duplicate(self):
        ee = self._get_engine()
        ee.mark_event_fired("test_event")
        ee.mark_event_fired("test_event")
        self.assertEqual(len(ee.get_fired_events()), 1)

    # --- Effect application ---

    def test_effects_xp(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 100
        msgs = ee._apply_effects({"xp": 50})
        self.assertEqual(state.xp, 150)
        self.assertIn("50 XP", msgs[0])

    def test_effects_negative_xp(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 100
        msgs = ee._apply_effects({"xp": -30})
        self.assertEqual(state.xp, 70)

    def test_effects_noise(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.noise_level = 10
        ee._apply_effects({"noise": 5})
        self.assertEqual(state.noise_level, 15)

    def test_effects_negative_noise(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.noise_level = 10
        ee._apply_effects({"noise": -5})
        self.assertEqual(state.noise_level, 5)

    def test_effects_trace(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        ee._apply_effects({"trace": 3})
        self.assertEqual(getattr(state, "trace_count", 0), 3)

    def test_effects_hint_block(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.hint_enabled = True
        ee._apply_effects({"hint_block": True})
        self.assertFalse(state.hint_enabled)

    def test_effects_empty(self):
        ee = self._get_engine()
        msgs = ee._apply_effects({})
        self.assertEqual(msgs, [])

    def test_effects_none(self):
        ee = self._get_engine()
        msgs = ee._apply_effects(None)
        self.assertEqual(msgs, [])

    # --- Full check_events ---

    def test_check_events_fires_threshold_event(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 100
        self._write_events(
            [
                {
                    "id": "xp_100",
                    "title": "100 XP",
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 100,
                    },
                    "action": {"type": "teacher_message", "message": "Good job!"},
                    "effects": {"xp": 30},
                }
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "xp_100")
        self.assertEqual(results[0]["message"], "Good job!")
        self.assertEqual(state.xp, 130)

    def test_check_events_once_fires_only_once(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.stealth_ops = 10
        self._write_events(
            [
                {
                    "id": "stealth_10",
                    "title": "Stealthy",
                    "trigger": {
                        "type": "threshold",
                        "metric": "stealth_ops",
                        "op": ">=",
                        "value": 10,
                    },
                    "action": {
                        "type": "teacher_message",
                        "message": "You are a ghost.",
                    },
                    "once": True,
                }
            ]
        )
        results1 = ee.check_events()
        self.assertEqual(len(results1), 1)
        results2 = ee.check_events()
        self.assertEqual(len(results2), 0)

    def test_check_events_and_trigger(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.current_chapter = 3
        state.stealth_ops = 2
        self._write_events(
            [
                {
                    "id": "chapter_3_stealth",
                    "title": "Deep Dive",
                    "trigger": {
                        "type": "and",
                        "triggers": [
                            {
                                "type": "threshold",
                                "metric": "current_chapter",
                                "op": ">=",
                                "value": 3,
                            },
                            {
                                "type": "threshold",
                                "metric": "stealth_ops",
                                "op": ">=",
                                "value": 2,
                            },
                        ],
                    },
                    "action": {"type": "teacher_message", "message": "You are deep."},
                    "effects": {"xp": 25, "noise": 5},
                }
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 1)
        effects = results[0]["effects"]
        self.assertTrue(any("25" in e and "XP" in e for e in effects))
        self.assertTrue(any("5" in e for e in effects))

    def test_check_events_condition_not_fired(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 200
        # Mark event_a as already fired
        ee.mark_event_fired("event_a")
        self._write_events(
            [
                {
                    "id": "xp_200",
                    "title": "200 XP",
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 200,
                    },
                    "condition": {"not_fired": ["event_a"]},
                    "action": {"message": "You reached 200!"},
                }
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 0)

    def test_check_events_condition_fired_before(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 200
        ee.mark_event_fired("previous_event")
        self._write_events(
            [
                {
                    "id": "xp_200",
                    "title": "200 XP",
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 200,
                    },
                    "condition": {"fired_before": ["previous_event"]},
                    "action": {"message": "You reached 200 after previous!"},
                }
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 1)

    def test_check_events_no_match(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 10
        self._write_events(
            [
                {
                    "id": "xp_100",
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 100,
                    },
                    "action": {"message": "Not yet"},
                }
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 0)

    def test_check_events_bad_event_skipped(self):
        ee = self._get_engine()
        self._write_events(
            [
                {"not_an_id": True},
                {
                    "id": "valid",
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 0,
                    },
                    "action": {"message": "ok"},
                },
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "valid")

    def test_check_events_multiple_events(self):
        ee = self._get_engine()
        from state import get_state

        state = get_state()
        state.xp = 200
        state.stealth_ops = 5
        self._write_events(
            [
                {
                    "id": "xp_100",
                    "once": True,
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 100,
                    },
                    "action": {"message": "100 XP!"},
                },
                {
                    "id": "stealth_5",
                    "once": True,
                    "trigger": {
                        "type": "threshold",
                        "metric": "stealth_ops",
                        "op": ">=",
                        "value": 5,
                    },
                    "action": {"message": "5 stealth ops!"},
                },
                {
                    "id": "xp_500",
                    "once": True,
                    "trigger": {
                        "type": "threshold",
                        "metric": "xp",
                        "op": ">=",
                        "value": 500,
                    },
                    "action": {"message": "500 XP!"},
                },
            ]
        )
        results = ee.check_events()
        self.assertEqual(len(results), 2)
        fired_ids = {r["id"] for r in results}
        self.assertIn("xp_100", fired_ids)
        self.assertIn("stealth_5", fired_ids)


if __name__ == "__main__":
    unittest.main()
