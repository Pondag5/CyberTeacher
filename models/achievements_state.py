"""
Achievements, XP, and progress tracking.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class AchievementsState(BaseModel):
    """Achievements, XP, and progress tracking."""

    # Статистика для достижений
    total_flags_collected: int = Field(default=0, ge=0)
    assignments_completed: int = Field(default=0, ge=0)
    labs_started: int = Field(default=0, ge=0)
    quizzes_taken: int = Field(default=0, ge=0)
    news_checked: int = Field(default=0, ge=0)
    messages_sent: int = Field(default=0, ge=0)
    earned_achievements: list[str] = Field(default_factory=list)

    # Новые счётчики для расширенных достижений (C-13)
    social_success: int = Field(
        default=0, ge=0
    )  # Успешные сценарии социальной инженерии
    apt_groups_viewed: int = Field(default=0, ge=0)  # Просмотренные досье APT-групп
    stealth_ops: int = Field(
        default=0, ge=0
    )  # Стелс-операции (задания с низким уровнем риска)
    threat_exposures: int = Field(
        default=0, ge=0
    )  # Изучение угроз (анализ сводок, новости)

    # XP и бусты
    points: float = Field(default=0.0, ge=0.0)  # float для поддержки XP multipliers
    xp_boost_multiplier: float = Field(default=1.0, ge=0.0)
    xp_boost_expiry: float = Field(default=0.0, ge=0.0)  # timestamp

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
        self.xp_boost_multiplier = max(0.0, multiplier)
        self.xp_boost_expiry = time.time() + max(0.0, duration_hours) * 3600

    @model_validator(mode="after")
    def validate_xp_boost(self):
        """Validate XP boost fields consistency."""
        if self.xp_boost_expiry > 0 and self.xp_boost_multiplier <= 1.0:
            # If expiry is set but multiplier is not boosting, reset expiry
            self.xp_boost_expiry = 0.0
        return self
