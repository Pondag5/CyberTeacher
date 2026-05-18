"""
Real-time hints state management.
"""

import time

from pydantic import BaseModel, Field


class HintsState(BaseModel):
    """Real-time hints configuration and state."""

    hint_enabled: bool = Field(default=True)  # automatic hints on/off
    hint_credits: int = Field(default=3, ge=0)  # available manual hints
    hints_used: int = Field(default=0, ge=0)  # used in current session/mission
    last_hint_time: float = Field(default_factory=time.time)  # timestamp of last hint
    hint_cooldown: int = Field(default=30, gt=0)  # seconds between auto-hints

    model_config = {"validate_assignment": True}
