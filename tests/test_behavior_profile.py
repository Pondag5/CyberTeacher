"""Tests for behavior_profile.py — hidden behavioral traits + archetype detection."""

import unittest

from state import AppState


class TestBehaviorProfile(unittest.TestCase):
    def setUp(self):
        # Each test gets a fresh state
        self.state = AppState()
        # Import here to avoid import-order issues
        from behavior_profile import get_profile, record_action

        self.get_profile = get_profile
        self.record_action = record_action

    def test_get_profile_creates_default(self):
        profile = self.get_profile(self.state)
        for trait in ["curiosity", "recklessness", "discipline", "creativity", "opsec"]:
            self.assertIn(trait, profile)
            self.assertEqual(profile[trait], 25)
        self.assertEqual(profile["stress"], 0)
        self.assertEqual(profile["archetype"], "engineer")
        self.assertEqual(profile["total_actions"], 0)

    def test_get_profile_reuses_existing(self):
        profile1 = self.get_profile(self.state)
        profile2 = self.get_profile(self.state)
        self.assertIs(profile1, profile2)

    # --- Trait adjustments ---

    def test_quiz_pass_adjusts(self):
        self.record_action(self.state, "quiz_pass")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["discipline"], 28)
        self.assertEqual(profile["stress"], 0)  # clamped at 0

    def test_quiz_fail_adjusts(self):
        self.record_action(self.state, "quiz_fail")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["stress"], 5)
        self.assertEqual(profile["curiosity"], 26)

    def test_exploit_attempt_adjusts(self):
        self.record_action(self.state, "exploit_attempt")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["recklessness"], 29)
        self.assertEqual(profile["creativity"], 27)
        self.assertEqual(profile["opsec"], 23)

    def test_exploit_success_adjusts(self):
        self.record_action(self.state, "exploit_success")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["creativity"], 29)
        self.assertEqual(profile["stress"], 0)  # clamped at 0

    def test_stealth_toggle_on_adjusts(self):
        self.record_action(self.state, "stealth_toggle_on")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["opsec"], 28)
        self.assertEqual(profile["discipline"], 26)

    def test_wipe_logs_adjusts(self):
        self.record_action(self.state, "wipe_logs")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["opsec"], 29)

    def test_mission_complete_adjusts(self):
        self.record_action(self.state, "mission_complete")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["discipline"], 28)
        self.assertEqual(profile["stress"], 0)  # clamped at 0

    def test_course_lesson_adjusts(self):
        self.record_action(self.state, "course_lesson")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["discipline"], 27)
        self.assertEqual(profile["curiosity"], 26)
        self.assertEqual(profile["stress"], 0)  # clamped at 0

    def test_ctf_flag_adjusts(self):
        self.record_action(self.state, "ctf_flag")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["creativity"], 28)
        self.assertEqual(profile["recklessness"], 27)

    def test_night_session_adjusts(self):
        self.record_action(self.state, "night_session")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["curiosity"], 27)
        self.assertEqual(profile["stress"], 2)

    def test_traits_clamped_0_100(self):
        # Push curiosity to max
        for _ in range(50):
            self.record_action(self.state, "new_topic")
        profile = self.get_profile(self.state)
        self.assertLessEqual(profile["curiosity"], 100)
        # Push stress down
        for _ in range(50):
            self.record_action(self.state, "quiz_pass")
        self.assertGreaterEqual(profile["stress"], 0)

    def test_unknown_action_ignored(self):
        self.record_action(self.state, "unknown_action")
        profile = self.get_profile(self.state)
        for trait in ["curiosity", "recklessness", "discipline", "creativity", "opsec"]:
            self.assertEqual(profile[trait], 25)

    # --- Archetype detection ---

    def test_archetype_engineer_before_10_actions(self):
        for _ in range(5):
            self.record_action(self.state, "quiz_pass")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["archetype"], "engineer")

    def test_archetype_analyst(self):
        for _ in range(12):
            self.record_action(self.state, "quiz_pass")
        for _ in range(8):
            self.record_action(self.state, "stealth_toggle_on")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["archetype"], "analyst")

    def test_archetype_researcher(self):
        for _ in range(12):
            self.record_action(self.state, "new_topic")
        for _ in range(8):
            self.record_action(self.state, "course_lesson")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["archetype"], "researcher")

    def test_archetype_script_kiddie(self):
        for _ in range(12):
            self.record_action(self.state, "exploit_attempt")
        for _ in range(5):
            self.record_action(self.state, "social_attack")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["archetype"], "script_kiddie")

    def test_archetype_ghost(self):
        for _ in range(12):
            self.record_action(self.state, "stealth_toggle_on")
        for _ in range(8):
            self.record_action(self.state, "wipe_logs")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["archetype"], "ghost")

    def test_archetype_chaotic(self):
        for _ in range(12):
            self.record_action(self.state, "exploit_success")
        for _ in range(8):
            self.record_action(self.state, "ctf_flag")
        profile = self.get_profile(self.state)
        self.assertEqual(profile["archetype"], "chaotic")

    # --- Prompt modifier ---

    def test_get_archetype_prompt_modifier_returns_string(self):
        from behavior_profile import get_archetype_prompt_modifier

        mod = get_archetype_prompt_modifier(self.state)
        self.assertIsNotNone(mod)
        self.assertIn("Инженер", mod)

    def test_get_archetype_prompt_modifier_changes_with_archetype(self):
        from behavior_profile import get_archetype_prompt_modifier

        self.record_action(self.state, "new_topic")
        for _ in range(15):
            self.record_action(self.state, "quiz_pass")
        mod = get_archetype_prompt_modifier(self.state)
        self.assertIn("Аналитик", mod)

    # --- Profile summary ---

    def test_get_profile_summary_structure(self):
        from behavior_profile import get_profile_summary

        summary = get_profile_summary(self.state)
        self.assertIn("traits", summary)
        self.assertIn("archetype", summary)
        self.assertIn("stress", summary)
        self.assertIn("total_actions", summary)
        self.assertEqual(summary["archetype"]["id"], "engineer")

    def test_get_profile_summary_traits_list(self):
        from behavior_profile import get_profile_summary

        summary = get_profile_summary(self.state)
        for trait in ["curiosity", "recklessness", "discipline", "creativity", "opsec"]:
            self.assertIn(trait, summary["traits"])


if __name__ == "__main__":
    unittest.main()
