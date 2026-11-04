"""
Real-time hints state management.
"""

import time

from pydantic import BaseModel, Field


class HintsState(BaseModel):
    """Real-time hints configuration and state."""

    hint_enabled: bool = Field(default=True)
    hint_credits: int = Field(default=3, ge=0)
    hints_used: int = Field(default=0, ge=0)
    last_hint_time: float = Field(default_factory=time.time)
    hint_cooldown: int = Field(default=30, gt=0)

    model_config = {"validate_assignment": True}