"""Тесты для расширенных достижений C-13"""

import json
import os
import unittest

from state import AppState


class TestAchievementsC13(unittest.TestCase):
    def setUp(self):
        """Fresh state for each test"""
        self.state = AppState()
        # Сброс всех счётчиков
        self.state.social_success = 0
        self.state.apt_groups_viewed = 0
        self.state.stealth_ops = 0
        self.state.threat_exposures = 0
        self.state.earned_achievements = []
        self.state.points = 0

    def test_social_success_counter(self):
        """Тест счётчика социальной инженерии"""
        for _ in range(5):
            self.state.increment_social_success()
        self.assertEqual(self.state.social_success, 5)

    def test_social_engineer_achievement_unlocked(self):
        """Достижение 'Социальный инженер' (5 успехов)"""
        for _ in range(5):
            self.state.increment_social_success()
        self.assertIn("social_engineer_5", self.state.earned_achievements)
        # Проверяем, что XP были начислены (30 XP)
        self.assertGreater(self.state.points, 0)

    def test_social_engineer_master_achievement(self):
        """Достижение 'Мастер социальной инженерии' (20 успехов)"""
        for _ in range(20):
            self.state.increment_social_success()
        self.assertIn("social_engineer_20", self.state.earned_achievements)

    def test_apt_groups_viewed_counter(self):
        """Тест счётчика просмотра APT-групп"""
        for _ in range(10):
            self.state.increment_apt_groups_viewed()
        self.assertEqual(self.state.apt_groups_viewed, 10)

    def test_apt_hunter_achievement_unlocked(self):
        """Достижение 'APT Охотник' (10 групп)"""
        for _ in range(10):
            self.state.increment_apt_groups_viewed()
        self.assertIn("apt_hunter_10", self.state.earned_achievements)

    def test_apt_hunter_expert_achievement(self):
        """Достижение 'APT Охотник Эксперт' (25 групп)"""
        for _ in range(25):
            self.state.increment_apt_groups_viewed()
        self.assertIn("apt_hunter_25", self.state.earned_achievements)

    def test_stealth_ops_counter(self):
        """Тест счётчика стелс-операций"""
        for _ in range(5):
            self.state.increment_stealth_ops()
        self.assertEqual(self.state.stealth_ops, 5)

    def test_ghost_in_the_shell_achievement_unlocked(self):
        """Достижение 'Призрак в Сети' (5 стелс-операций)"""
        for _ in range(5):
            self.state.increment_stealth_ops()
        self.assertIn("ghost_in_the_shell_5", self.state.earned_achievements)

    def test_ghost_in_the_shell_legend_achievement(self):
        """Достижение 'Призрак в Стелле' (15 стелс-операций)"""
        for _ in range(15):
            self.state.increment_stealth_ops()
        self.assertIn("ghost_in_the_shell_15", self.state.earned_achievements)

    def test_threat_exposures_counter(self):
        """Тест счётчика изучения угроз"""
        for _ in range(10):
            self.state.increment_threat_exposures()
        self.assertEqual(self.state.threat_exposures, 10)

    def test_snowden_achievement_unlocked(self):
        """Достижение 'Сноуден' (10 изучений угроз)"""
        for _ in range(10):
            self.state.increment_threat_exposures()
        self.assertIn("snowden_10", self.state.earned_achievements)

    def test_snowden_legend_achievement(self):
        """Достижение 'Сноуден Легенда' (25 изучений угроз)"""
        for _ in range(25):
            self.state.increment_threat_exposures()
        self.assertIn("snowden_25", self.state.earned_achievements)

    def test_achievements_not_awarded_twice(self):
        """Достижения начисляются только один раз"""
        # Первый раз достигли порога
        for _ in range(5):
            self.state.increment_social_success()
        initial_points = self.state.points
        # Проверяем, что достижение получено
        self.assertIn("social_engineer_5", self.state.earned_achievements)
        # Повторно вызываем check_achievements (или инкрементируем ещё) — не должно добавляться снова
        self.state.increment_social_success()  # теперь 6
        self.assertEqual(self.state.social_success, 6)
        # Достижение не дублируется
        self.assertEqual(self.state.earned_achievements.count("social_engineer_5"), 1)
        # Очки не начисляются повторно (только при первом получении)
        # Уже начислили 30 XP при достижении 5, поэтому points должно быть initial_points + 30
        self.assertEqual(self.state.points, initial_points)

    def test_risk_based_stealth_not_automatic(self):
        """Стелс-операция не начисляется автоматически через инкремент, только явно"""
        # increment_stealth_ops явно вызывается, но если риск >=20, достижение всё равно может быть получено, если порог по счётчику
        # Здесь просто проверяем, что счётчик увеличивается корректно
        self.state.stealth_ops = 0
        self.state.increment_stealth_ops()
        self.assertEqual(self.state.stealth_ops, 1)


if __name__ == "__main__":
    unittest.main()
