"""
Learning progress, achievements, shop, and risk state.
"""

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProgressState(BaseModel):
    """Combined progress, achievements, shop, and risk."""
    
    # Learning
    current_course: Optional[str] = None
    current_topic: int = Field(default=0, ge=0)
    course_progress: Dict[str, int] = Field(default_factory=dict)
    learning_context: Dict[str, Any] = Field(default_factory=lambda: {
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
    earned_achievements: List[str] = Field(default_factory=list)
    social_success: int = Field(default=0, ge=0)
    apt_groups_viewed: int = Field(default=0, ge=0)
    stealth_ops: int = Field(default=0, ge=0)
    threat_exposures: int = Field(default=0, ge=0)
    points: float = Field(default=0.0, ge=0.0)

    # XP Boosts
    xp_boost_multiplier: float = Field(default=1.0, ge=0.0)
    xp_boost_expiry: float = Field(default=0.0, ge=0.0)

    # Shop
    owned_themes: List[str] = Field(default_factory=list)
    current_theme: str = Field(default="default")
    unlocked_topics: List[str] = Field(default_factory=list)
    hint_credits: int = Field(default=3, ge=0)
    selected_tools: List[str] = Field(default_factory=list)
    trace_deadline: Optional[float] = None
    trace_hint: Optional[str] = None
    missions_completed: List[str] = Field(default_factory=list)
    active_mission: Optional[str] = None

    # Risk
    risk_level: int = Field(default=0, ge=0, le=100)

    # Learning methods
    def set_learning_context(self, course=None, topic=None, lab=None, action=None):
        if course: self.learning_context["current_course"] = course
        if topic: self.learning_context["current_topic"] = topic
        if lab: self.learning_context["current_lab"] = lab
        if action: self.learning_context["last_action"] = action

    def get_learning_context(self) -> Dict[str, Any]:
        return self.learning_context

    def reset_course(self):
        self.current_course = None
        self.current_topic = 0

    def set_course(self, course_id: str):
        self.current_course = course_id
        self.current_topic = 0

    def next_topic(self):
        self.current_topic += 1

    # Achievement methods
    def increment_flag(self): self.total_flags_collected += 1
    def complete_assignment(self): self.assignments_completed += 1
    def start_lab(self): self.labs_started += 1
    def take_quiz(self): self.quizzes_taken += 1
    def check_news(self): self.news_checked += 1
    def send_message(self): self.messages_sent += 1
    def increment_social_success(self): self.social_success += 1
    def increment_apt_groups_viewed(self): self.apt_groups_viewed += 1
    def increment_stealth_ops(self): self.stealth_ops += 1
    def increment_threat_exposures(self): self.threat_exposures += 1

    # XP methods
    def get_xp_multiplier(self) -> float:
        now = time.time()
        if self.xp_boost_expiry > 0 and now < self.xp_boost_expiry:
            return self.xp_boost_multiplier
        self.xp_boost_multiplier = 1.0
        self.xp_boost_expiry = 0.0
        return 1.0

    def apply_xp_boost(self, multiplier: float, duration_hours: float):
        self.xp_boost_multiplier = max(0.0, multiplier)
        self.xp_boost_expiry = time.time() + max(0.0, duration_hours) * 3600

    # Risk methods
    def increase_risk(self, amount: int = 10):
        self.risk_level = min(100, self.risk_level + amount)

    def decrease_risk(self, amount: int = 5):
        self.risk_level = max(0, self.risk_level - amount)

    def reset_risk(self):
        self.risk_level = 0

    def get_risk_status(self) -> str:
        if self.risk_level < 20: return "🟢 Низкий"
        elif self.risk_level < 50: return "🟡 Умеренный"
        elif self.risk_level < 80: return "🟠 Высокий"
        else: return "🔴 Критический"

    # Shop methods
    def apply_item_effect(self, item: dict) -> str:
        item_type = item.get("type")
        if item_type == "theme":
            theme_id = item.get("value")
            if theme_id and theme_id not in self.owned_themes:
                self.owned_themes.append(theme_id)
                return "theme"
        elif item_type == "unlock_topic":
            topic = item.get("value")
            if topic and topic not in self.unlocked_topics:
                self.unlocked_topics.append(topic)
                return "unlock_topic"
        elif item_type == "xp_boost":
            self.apply_xp_boost(item.get("multiplier", 2.0), item.get("duration_hours", 1))
            return "xp_boost"
        elif item_type == "consumable":
            if item.get("effect") == "hint_credit":
                self.hint_credits += item.get("quantity", 1)
                return "hint_credit"
        return None

    model_config = {"validate_assignment": True}