"""
Application settings: hints, voice, and explanation depth.
"""

import time

from pydantic import BaseModel, Field


class SettingsState(BaseModel):
    """Hints, voice, and explanation configuration."""
    
    # Hints
    hint_enabled: bool = Field(default=True)
    hint_credits: int = Field(default=3, ge=0)
    hints_used: int = Field(default=0, ge=0)
    last_hint_time: float = Field(default_factory=time.time)
    hint_cooldown: int = Field(default=30, gt=0)

    # Voice
    voice_enabled: bool = Field(default=False)
    voice_engine: str = Field(default="pyttsx3")
    voice_rate: int = Field(default=200, gt=0)

    # Explanation
    explanation_depth: str = Field(default="normal")  # beginner, normal, expert

    # Language (i18n)
    language: str = Field(default="ru")  # ru, en

    def set_explanation_depth(self, depth: str) -> str:
        if depth in ("beginner", "normal", "expert"):
            self.explanation_depth = depth
        return self.explanation_depth

    def get_explanation_depth(self) -> str:
        return self.explanation_depth

    model_config = {"validate_assignment": True}
