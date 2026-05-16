"""
Real-time hints state management.
"""

from dataclasses import dataclass, field
import time


@dataclass
class HintsState:
    """Real-time hints configuration and state."""
    
    hint_enabled: bool = True  # automatic hints on/off
    hint_credits: int = 3  # available manual hints
    hints_used: int = 0  # used in current session/mission
    last_hint_time: float = 0.0  # timestamp of last hint
    hint_cooldown: int = 30  # seconds between auto-hints