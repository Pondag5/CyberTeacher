"""Unit tests for story_mode.py (selected functions)"""

import unittest
from unittest.mock import MagicMock, patch
from story_mode import get_level, StoryPlayer, get_story_list


class TestGetLevel(unittest.TestCase):
    def test_get_level_script_kiddie(self):
        self.assertEqual(get_level(0), "Script Kiddie")
        self.assertEqual(get_level(50), "Script Kiddie")

    def test_get_level_hacker(self):
        self.assertEqual(get_level(100), "Hacker")
        self.assertEqual(get_level(150), "Hacker")

    def test_get_level_penetration_tester(self):
        self.assertEqual(get_level(300), "Penetration Tester")
        self.assertEqual(get_level(500), "Penetration Tester")

    def test_get_level_security_expert(self):
        self.assertEqual(get_level(600), "Security Expert")
        self.assertEqual(get_level(999), "Security Expert")

    def test_get_level_master_hacker(self):
        self.assertEqual(get_level(1000), "Master Hacker")
        self.assertEqual(get_level(1500), "Master Hacker")

    def test_get_level_legend(self):
        self.assertEqual(get_level(2000), "Legend")
        self.assertEqual(get_level(5000), "Legend")


class TestStoryPlayer(unittest.TestCase):
    def test_init_defaults(self):
        player = StoryPlayer()
        self.assertEqual(player.xp, 0)
        self.assertEqual(player.completed_episodes, [])
        self.assertEqual(player.current_episode, 1)

    def test_complete_episode_adds_and_gives_xp(self):
        player = StoryPlayer()
        player.complete_episode(1, 100)
        self.assertIn(1, player.completed_episodes)
        self.assertEqual(player.xp, 100)

    def test_complete_episode_duplicate(self):
        player = StoryPlayer()
        player.complete_episode(1, 100)
        player.complete_episode(1, 100)  # duplicate
        self.assertEqual(len(player.completed_episodes), 1)
        self.assertEqual(player.xp, 100)  # no additional XP

    def test_level_property(self):
        player = StoryPlayer()
        player.xp = 250
        self.assertEqual(player.level, "Hacker")

    def test_check_achievements_first_blood(self):
        player = StoryPlayer()
        achievements = player.check_achievements()
        # No achievements initially
        self.assertFalse(any(a == "first_blood" for a in achievements))
        # Complete first episode
        player.complete_episode(1, 100)
        achievements = player.check_achievements()
        self.assertIn("first_blood", achievements)

    def test_check_achievements_web_hacker(self):
        player = StoryPlayer()
        # Complete 5 web episodes (ids 1-5)
        for ep_id in range(1, 6):
            player.complete_episode(ep_id, 100)
        achievements = player.check_achievements()
        self.assertIn("web_hacker", achievements)

    def test_check_achievements_behavior(self):
        player = StoryPlayer()
        player.complete_episode(1, 100)
        ach1 = player.check_achievements()
        self.assertIn("first_blood", ach1)
        # Subsequent call still includes it due to implementation
        ach2 = player.check_achievements()
        self.assertIn("first_blood", ach2)


class TestGetStoryList(unittest.TestCase):
    def test_get_story_list_returns_string(self):
        result = get_story_list()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Check for some episode title substrings
        self.assertIn("Первое", result)
        self.assertIn("XSS", result)
        self.assertIn("CSRF ловушка", result)


if __name__ == "__main__":
    unittest.main()
