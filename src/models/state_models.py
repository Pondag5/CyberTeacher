"""
Pydantic models for state validation and serialization.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AppStateModel(BaseModel):
    """Validation model for app_state.json loading."""

    # Learning
    current_course: str | None = None
    current_topic: int = Field(default=0, ge=0)
    learning_context: dict[str, Any] = Field(default_factory=dict)
    course_progress: dict[str, int] = Field(default_factory=dict)

    # User
    username: str = Field(default="Аноним")
    avatar: str = Field(default="🧑‍💻")
    reputation: int = Field(default=0, ge=0)
    handle: str = Field(default="Новичок")
    htb_email: str | None = None
    htb_password_enc: str | None = None
    htb_password: str | None = None
    htb_completed: list[int] = Field(default_factory=list)

    # Achievements
    points: float = Field(default=0.0, ge=0.0)
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
    xp_boost_multiplier: float = Field(default=1.0, ge=0.0)
    xp_boost_expiry: float = Field(default=0.0, ge=0.0)

    # Metrics
    llm_call_count: int = Field(default=0, ge=0)
    llm_total_time: float = Field(default=0.0, ge=0.0)
    llm_total_tokens: int = Field(default=0, ge=0)
    cache_hits: int = Field(default=0, ge=0)
    cache_misses: int = Field(default=0, ge=0)
    start_time: float = Field(default=0.0)
    request_timestamps: list[float] = Field(default_factory=list)
    command_usage: dict[str, int] = Field(default_factory=dict)

    # Persona
    current_persona: str = Field(default="teacher")
    current_mode: str = Field(default="teacher")

    # Risk
    risk_level: int = Field(default=0, ge=0, le=100)

    # Shop
    owned_themes: list[str] = Field(default_factory=list)
    current_theme: str = Field(default="default")
    unlocked_topics: list[str] = Field(default_factory=list)
    hint_credits: int = Field(default=3, ge=0)
    selected_tools: list[str] = Field(default_factory=list)
    trace_deadline: float | None = None
    trace_hint: str | None = None
    missions_completed: list[str] = Field(default_factory=list)
    active_mission: str | None = None

    # Hints
    hint_enabled: bool = Field(default=True)
    hints_used: int = Field(default=0, ge=0)
    last_hint_time: float = Field(default=0.0)
    hint_cooldown: int = Field(default=30, gt=0)

    # Explanation
    explanation_depth: str = Field(default="normal")

    # Direct AppState attributes
    last_news: str | None = None
    active_assignment: dict[str, Any] | None = None
    collected_flags: list[str] = Field(default_factory=list)
    weak_topics: list[dict[str, Any]] = Field(default_factory=list)
    review_schedule: dict[str, Any] = Field(default_factory=dict)
    feature_flags: dict[str, bool] = Field(default_factory=dict)
    last_writeup_activity: dict[str, Any] | None = None
    writeup_history: list[dict[str, Any]] = Field(default_factory=list)
    exploit_success: list[dict[str, Any]] = Field(default_factory=list)
    tracks_enrolled: list[str] = Field(default_factory=list)
    track_progress: dict[str, Any] = Field(default_factory=dict)
    bounty_reports: list[dict[str, Any]] = Field(default_factory=list)
    skill_tracker: dict[str, Any] = Field(default_factory=dict)
    emotion_mode: str = Field(default="neutral")
