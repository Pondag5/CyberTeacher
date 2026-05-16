"""
Achievements, XP, and progress tracking.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
import time


@dataclass
class AchievementsState:
    """Achievements, XP, and progress tracking."""
    
    # Статистика для достижений
    total_flags_collected: int = 0
    assignments_completed: int = 0
    labs_started: int = 0
    quizzes_taken: int = 0
    news_checked: int = 0
    messages_sent: int = 0
    earned_achievements: List[str] = field(default_factory=list)

    # Новые счётчики для расширенных достижений (C-13)
    social_success: int = 0  # Успешные сценарии социальной инженерии
    apt_groups_viewed: int = 0  # Просмотренные досье APT-групп
    stealth_ops: int = 0  # Стелс-операции (задания с низким уровнем риска)
    threat_exposures: int = 0  # Изучение угроз (анализ сводок, новости)

    # XP и бусты
    points: float = 0.0  # float для поддержки XP multipliers
    xp_boost_multiplier: float = 1.0
    xp_boost_expiry: float = 0.0  # timestamp

    def increment_flag(self):
        """Увеличить счётчик собранных флагов"""
        self.total_flags_collected += 1

    def complete_assignment(self):
        """Отметить выполнение задания"""
        self.assignments_completed += 1

    def start_lab(self):
        """Отметить запуск лаборатории"""
        self.labs_started += 1

    def take_quiz(self):
        """Отметить прохождение квиза"""
        self.quizzes_taken += 1

    def check_news(self):
        """Отметить проверку новостей"""
        self.news_checked += 1

    def send_message(self):
        """Увеличить счётчик отправленных сообщений"""
        self.messages_sent += 1

    # === НОВЫЕ СЧЁТЧИКИ ДЛЯ РАСШИРЕННЫХ ДОСТИЖЕНИЙ (C-13) ===

    def increment_social_success(self):
        """Увеличить счётчик успешных сценариев социальной инженерии"""
        self.social_success += 1

    def increment_apt_groups_viewed(self):
        """Увеличить счётчик просмотренных досье APT-групп"""
        self.apt_groups_viewed += 1

    def increment_stealth_ops(self):
        """Увеличить счётчик стелс-операций (задания с низким риском)"""
        self.stealth_ops += 1

    def increment_threat_exposures(self):
        """Увеличить счётчик изучения угроз (сводки, анализ)"""
        self.threat_exposures += 1

    def get_xp_multiplier(self) -> float:
        """Возвращает текущий множитель XP с учетом активного буста."""
        now = time.time()
        if self.xp_boost_expiry > 0 and now < self.xp_boost_expiry:
            return self.xp_boost_multiplier
        # Бонус истек или не установлен — сбрасываем
        self.xp_boost_multiplier = 1.0
        self.xp_boost_expiry = 0.0
        return 1.0

    def apply_xp_boost(self, multiplier: float, duration_hours: float):
        """Применить XP буст."""
        self.xp_boost_multiplier = multiplier
        self.xp_boost_expiry = time.time() + duration_hours * 3600