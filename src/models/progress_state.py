"""
Learning progress, achievements, shop, and risk state.
"""

import time
from typing import Any, Callable

from pydantic import BaseModel, Field


class ProgressState(BaseModel):
    """Combined progress, achievements, shop, and risk."""

    # Learning
    current_course: str | None = None
    current_topic: int = Field(default=0, ge=0)
    course_progress: dict[str, int] = Field(default_factory=dict)
    learning_context: dict[str, Any] = Field(default_factory=lambda: {
        "current_course": None, "current_topic": None,
        "current_lab": None, "last_action": None,
    })

    # Achievements
    total_flags_collected: int = Field(default=0, ge=0)
    assignments_completed: int = Field(default=0, ge=0)
    labs_started: int = Field(default=0, ge=0)
    quizzes_taken: int = Field(default=0, ge=0)
    news_checked: int = Field(default=0, ge=0)
    messages_sent: int = Field(default=0, ge=0)
    earned_achievements: list[str] = Field(default_factory=list)
    social_success: int = Field(default=0, ge=0)
    apt_groups_viewed: int = Field(default=0, ge=0)
    stealth_ops: int = Field(default=0, ge=0)
    threat_exposures: int = Field(default=0, ge=0)
    points: float = Field(default=0.0, ge=0.0)

    # XP Boosts
    xp_boost_multiplier: float = Field(default=1.0, ge=0.0)
    xp_boost_expiry: float = Field(default=0.0, ge=0.0)

    # Shop / inventory
    owned_themes: list[str] = Field(default_factory=list)
    current_theme: str = Field(default="default")
    unlocked_topics: list[str] = Field(default_factory=list)
    hint_credits: int = Field(default=3, ge=0)
    selected_tools: list[str] = Field(default_factory=list)
    purchase_history: list[dict[str, Any]] = Field(default_factory=list)

    # Trace timer (H-03)
    trace_deadline: float | None = None
    trace_hint: str | None = None

    # Missions (H-05)
    missions_completed: list[str] = Field(default_factory=list)
    active_mission: str | None = None

    # Tracks (M-29)
    tracks_enrolled: list[str] = Field(default_factory=list)
    track_progress: dict[str, dict[str, Any]] = Field(default_factory=dict)

    # Hints (M-30)
    hints_used: int = Field(default=0, ge=0)
    last_hint_time: float = Field(default_factory=time.time)
    hint_cooldown: int = Field(default=30, gt=0)

    # Risk (уже есть, но оставим для совместимости)
    risk_level: int = Field(default=0, ge=0, le=100)

    # News
    last_news: str | None = None
    news_analyzed: int = Field(default=0, ge=0)

    # Features flags
    feature_flags: dict[str, bool] = Field(default_factory=dict)

    # Emotions
    emotion_mode: str = Field(default="neutral")

    # Writeups & Bounty
    last_writeup_activity: dict[str, Any] | None = None
    writeup_history: list[dict[str, Any]] = Field(default_factory=list)
    bounty_reports: list[dict[str, Any]] = Field(default_factory=list)

    # CTF / Phishing / Mermaid
    ctf_flags_generated: int = Field(default=0, ge=0)
    phishing_generated: int = Field(default=0, ge=0)
    mermaid_views: int = Field(default=0, ge=0)

    # Investigation
    found_evidence: list[str] = Field(default_factory=list)
    current_case: str | None = None

    # Exploits
    exploit_success: list[dict[str, Any]] = Field(default_factory=list)
    current_challenge: dict[str, Any] | None = None

    # Assignments
    active_assignment: dict[str, Any] | None = None
    collect_flag: Callable[[str], bool] | None = None  # заглушка для метода
    is_assignment_complete: Callable[[], bool] | None = None

    # Learning methods
    def set_learning_context(self, course=None, topic=None, lab=None, action=None) -> None:
        if course:
            self.learning_context["current_course"] = course
        if topic:
            self.learning_context["current_topic"] = topic
        if lab:
            self.learning_context["current_lab"] = lab
        if action:
            self.learning_context["last_action"] = action

    def get_learning_context(self) -> dict[str, Any]:
        return self.learning_context

    def reset_course(self) -> None:
        self.current_course = None
        self.current_topic = 0

    def set_course(self, course_id: str) -> None:
        self.current_course = course_id
        self.current_topic = 0

    def next_topic(self) -> None:
        self.current_topic += 1

    # Achievement methods
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

    # XP methods
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

    # Risk methods (делегируем на поле risk_level)
    def increase_risk(self, amount: int = 10) -> None:
        self.risk_level = min(100, self.risk_level + amount)

    def decrease_risk(self, amount: int = 5) -> None:
        self.risk_level = max(0, self.risk_level - amount)

    def reset_risk(self) -> None:
        self.risk_level = 0

    def get_risk_status(self) -> str:
        if self.risk_level < 20:
            return "🟢 Низкий"
        if self.risk_level < 50:
            return "🟡 Умеренный"
        if self.risk_level < 80:
            return "🟠 Высокий"
        return "🔴 Критический"

    # Shop methods
    def apply_item_effect(self, item: dict) -> str | None:
        item_type = item.get("type")
        if item_type == "theme":
            theme_id = item.get("value")
            if theme_id and theme_id not in self.owned_themes:
                self.owned_themes.append(theme_id)
                return "theme"
        if item_type == "unlock_topic":
            topic = item.get("value")
            if topic and topic not in self.unlocked_topics:
                self.unlocked_topics.append(topic)
                return "unlock_topic"
        if item_type == "xp_boost":
            self.apply_xp_boost(item.get("multiplier", 2.0), item.get("duration_hours", 1))
            return "xp_boost"
        if item_type == "consumable" and item.get("effect") == "hint_credit":
            self.hint_credits += item.get("quantity", 1)
            return "hint_credit"
        return None

    model_config = {"validate_assignment": True}