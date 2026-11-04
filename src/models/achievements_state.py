"""
Achievements, XP, and progress tracking.
"""

import time
from typing import Any

from pydantic import BaseModel, Field, model_validator


class AchievementsState(BaseModel):
    """Achievements, XP, and progress tracking."""

    total_flags_collected: int = Field(default=0, ge=0)
    assignments_completed: int = Field(default=0, ge=0)
    labs_started: int = Field(default=0, ge=0)
    quizzes_taken: int = Field(default=0, ge=0)
    news_checked: int = Field(default=0, ge=0)
    messages_sent: int = Field(default=0, ge=0)
    earned_achievements: list[str] = Field(default_factory=list)

    # New counters for extended achievements (C-13)
    social_success: int = Field(default=0, ge=0)
    apt_groups_viewed: int = Field(default=0, ge=0)
    stealth_ops: int = Field(default=0, ge=0)
    threat_exposures: int = Field(default=0, ge=0)

    # XP and boosts
    points: float = Field(default=0.0, ge=0.0)
    xp_boost_multiplier: float = Field(default=1.0, ge=0.0)
    xp_boost_expiry: float = Field(default=0.0, ge=0.0)

    def increment_flag(self) -> None:
        self.total_flags_collected += 1

    def complete_assignment(self) -> None:
        self.assignments_completed += 1

    def start_lab(self) -> None:
        self.labs_started += 1

    def take_quiz(self) -> None:
        self.quizzes_taken += 1

    def check_news(self) -> None:
        self.news_checked += 1

    def send_message(self) -> None:
        self.messages_sent += 1

    def increment_social_success(self) -> None:
        self.social_success += 1

    def increment_apt_groups_viewed(self) -> None:
        self.apt_groups_viewed += 1

    def increment_stealth_ops(self) -> None:
        self.stealth_ops += 1

    def increment_threat_exposures(self) -> None:
        self.threat_exposures += 1

    def get_xp_multiplier(self) -> float:
        now = time.time()
        if self.xp_boost_expiry > 0 and now < self.xp_boost_expiry:
            return self.xp_boost_multiplier
        self.xp_boost_multiplier = 1.0
        self.xp_boost_expiry = 0.0
        return 1.0

    def apply_xp_boost(self, multiplier: float, duration_hours: float) -> None:
        self.xp_boost_multiplier = max(0.0, multiplier)
        self.xp_boost_expiry = time.time() + max(0.0, duration_hours) * 3600

    @model_validator(mode="after")
    def validate_xp_boost(self) -> "AchievementsState":
        if self.xp_boost_expiry > 0 and self.xp_boost_multiplier <= 1.0:
            self.xp_boost_expiry = 0.0
        return self