"""
Tests for new services: weak_topics, spaced_repetition, skill_tracker, achievements.
"""

import json
import os
import tempfile
import time
import unittest

from services.weak_topics_service import (
    get_next_weak_topic,
    get_weak_topics,
    update_weak_topic,
)
from services.spaced_repetition_service import (
    compute_next_review,
    get_due_reviews,
    schedule_review,
)
from services.skill_tracker_service import (
    get_all_skills,
    get_skill_level,
    track_skill,
)
from services.achievement_service import (
    check_achievement,
    check_achievements,
    load_achievements,
)


class TestWeakTopicsService(unittest.TestCase):
    """Tests for weak_topics_service."""

    def test_update_creates_new_topic(self):
        topics = []
        update_weak_topic(topics, "sql", 5.0, 10.0)
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0]["topic"], "sql")
        self.assertEqual(topics[0]["success_rate"], 50.0)

    def test_update_accumulates_existing(self):
        topics = [{"topic": "sql", "attempts": 1, "total_score": 5.0, "max_score": 10.0, "success_rate": 50.0}]
        update_weak_topic(topics, "sql", 8.0, 10.0)
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0]["attempts"], 2)
        self.assertAlmostEqual(topics[0]["success_rate"], 65.0)

    def test_update_zero_max_score(self):
        topics = []
        update_weak_topic(topics, "xss", 0.0, 0.0)
        self.assertEqual(topics[0]["success_rate"], 0)

    def test_get_weak_topics_filters(self):
        topics = [
            {"topic": "sql", "success_rate": 40.0},
            {"topic": "xss", "success_rate": 80.0},
            {"topic": "csrf", "success_rate": 60.0},
        ]
        weak = get_weak_topics(topics, 70.0)
        self.assertEqual(len(weak), 2)
        self.assertEqual(weak[0]["topic"], "sql")

    def test_get_next_weak_topic_returns_weakest(self):
        topics = [
            {"topic": "sql", "success_rate": 40.0},
            {"topic": "xss", "success_rate": 60.0},
        ]
        self.assertEqual(get_next_weak_topic(topics, 70.0), "sql")

    def test_get_next_weak_topic_none_when_all_good(self):
        topics = [{"topic": "sql", "success_rate": 90.0}]
        self.assertIsNone(get_next_weak_topic(topics, 70.0))


class TestSpacedRepetitionService(unittest.TestCase):
    """Tests for spaced_repetition_service."""

    def test_compute_next_review(self):
        now = time.time()
        next_review = compute_next_review(1)
        self.assertAlmostEqual(next_review - now, 86400, delta=1000)

    def test_schedule_review_first_time(self):
        schedule = {}
        schedule_review(schedule, "sql", 8.0, 10.0)
        self.assertIn("sql", schedule)
        self.assertEqual(schedule["sql"]["repetitions"], 0)
        self.assertEqual(schedule["sql"]["interval"], 1)
        self.assertEqual(schedule["sql"]["ef"], 2.5)

    def test_schedule_review_bad_quality_resets(self):
        schedule = {}
        schedule_review(schedule, "sql", 8.0, 10.0)
        schedule_review(schedule, "sql", 1.0, 10.0)
        self.assertEqual(schedule["sql"]["repetitions"], 0)
        self.assertEqual(schedule["sql"]["interval"], 1)

    def test_schedule_review_good_quality_increments(self):
        schedule = {}
        schedule_review(schedule, "sql", 9.0, 10.0)
        self.assertEqual(schedule["sql"]["repetitions"], 0)
        self.assertEqual(schedule["sql"]["interval"], 1)
        schedule_review(schedule, "sql", 9.0, 10.0)
        self.assertEqual(schedule["sql"]["repetitions"], 1)
        self.assertEqual(schedule["sql"]["interval"], 1)
        schedule_review(schedule, "sql", 9.0, 10.0)
        self.assertEqual(schedule["sql"]["repetitions"], 2)
        self.assertEqual(schedule["sql"]["interval"], 3)

    def test_get_due_reviews_empty(self):
        schedule = {}
        schedule_review(schedule, "sql", 9.0, 10.0)
        due = get_due_reviews(schedule)
        self.assertEqual(len(due), 0)

    def test_get_due_reviews_returns_past(self):
        schedule = {
            "sql": {
                "repetitions": 0,
                "interval": 1,
                "next_review": time.time() - 1000,
                "last_grade": 8.0,
                "ef": 2.5,
            }
        }
        due = get_due_reviews(schedule)
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0]["topic"], "sql")


class TestSkillTrackerService(unittest.TestCase):
    """Tests for skill_tracker_service."""

    def test_track_skill_creates_new(self):
        tracker = {}
        track_skill(tracker, "nmap", True, 10)
        self.assertEqual(tracker["nmap"]["level"], 0)
        self.assertEqual(tracker["nmap"]["xp"], 10)
        self.assertEqual(tracker["nmap"]["attempts"], 1)
        self.assertEqual(tracker["nmap"]["successes"], 1)

    def test_track_skill_levels_up(self):
        tracker = {}
        for _ in range(6):
            track_skill(tracker, "nmap", True, 10)
        self.assertEqual(tracker["nmap"]["level"], 1)

    def test_track_skill_max_level(self):
        tracker = {}
        for _ in range(30):
            track_skill(tracker, "nmap", True, 10)
        self.assertEqual(tracker["nmap"]["level"], 5)

    def test_get_skill_level_unknown(self):
        self.assertEqual(get_skill_level({}, "nmap"), 0)

    def test_get_all_skills_sorted(self):
        tracker = {
            "nmap": {"level": 2, "xp": 100, "attempts": 10, "successes": 8},
            "sqlmap": {"level": 1, "xp": 50, "attempts": 5, "successes": 3},
        }
        skills = get_all_skills(tracker)
        self.assertEqual(skills[0]["name"], "nmap")
        self.assertEqual(skills[1]["name"], "sqlmap")


class TestAchievementService(unittest.TestCase):
    """Tests for achievement_service."""

    def test_check_achievement_not_earned(self):
        ach = {"id": "first_flag", "condition": {"type": "flags_total", "threshold": 5}, "points": 10}
        result = check_achievement(ach, [], lambda x: 3)
        self.assertFalse(result)

    def test_check_achievement_met(self):
        ach = {"id": "first_flag", "condition": {"type": "flags_total", "threshold": 5}, "points": 10}
        result = check_achievement(ach, [], lambda x: 10)
        self.assertTrue(result)

    def test_check_achievement_already_earned(self):
        ach = {"id": "first_flag", "condition": {"type": "flags_total", "threshold": 5}, "points": 10}
        result = check_achievement(ach, ["first_flag"], lambda x: 10)
        self.assertFalse(result)

    def test_check_achievement_unknown_type(self):
        ach = {"id": "unknown", "condition": {"type": "magic", "threshold": 5}, "points": 10}
        result = check_achievement(ach, [], lambda x: 100)
        self.assertFalse(result)

    def test_load_achievements_missing_file(self):
        import services.achievement_service as svc
        original = svc.ACHIEVEMENTS_FILE
        svc.ACHIEVEMENTS_FILE = "nonexistent_file.json"
        try:
            result = load_achievements()
            self.assertEqual(result, [])
        finally:
            svc.ACHIEVEMENTS_FILE = original

    def test_check_achievements_awards_xp(self):
        earned = []
        def getter(name):
            if name == "points": return 0
            if name == "xp_multiplier": return 1.0
            if name == "total_flags_collected": return 10
            return 0
        def setter(name, value):
            if name == "points":
                setter.points = value
        setter.points = 0

        ach_list = [
            {"id": "flag_master", "condition": {"type": "flags_total", "threshold": 5}, "points": 50}
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"achievements": ach_list}, f)
            temp_path = f.name

        try:
            import services.achievement_service as svc
            original = svc.ACHIEVEMENTS_FILE
            svc.ACHIEVEMENTS_FILE = temp_path
            newly = check_achievements(earned, getter, setter)
            svc.ACHIEVEMENTS_FILE = original
            self.assertEqual(len(newly), 1)
            self.assertEqual(setter.points, 50)
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
