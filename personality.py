"""Personality Drift — dynamic tone adjustment based on user behavior.

The teacher subtly changes behavior based on:
- Time of day (late night = darker, quieter)
- Session duration (long = more patient or more paranoid)
- User behavior (reckless = more sarcastic, focused = more analytical)
- Learning progress (improving = more encouraging)

This is atmospheric, not mechanical. Changes should feel natural.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class PersonalityState:
    """Tracks personality modifiers that drift over time.

    Values range from -1.0 to 1.0:
        sarcasm:     -1 (supportive) → 1 (very sarcastic)
        patience:    -1 (impatient)   → 1 (very patient)
        paranoia:    -1 (carefree)    → 1 (very paranoid)
        enthusiasm:  -1 (bored)       → 1 (very excited)
        formality:   -1 (casual)      → 1 (formal)
    """

    def __init__(self) -> None:
        self.sarcasm: float = 0.2  # Rick starts slightly sarcastic
        self.patience: float = 0.5  # Moderate patience
        self.paranoia: float = 0.0  # No paranoia initially
        self.enthusiasm: float = 0.3  # Slightly enthusiastic
        self.formality: float = 0.0  # Casual by default
        self._drift_count: int = 0

    def get_modifiers(self) -> Dict[str, float]:
        """Return current personality modifiers."""
        return {
            "sarcasm": max(-1, min(1, self.sarcasm)),
            "patience": max(-1, min(1, self.patience)),
            "paranoia": max(-1, min(1, self.paranoia)),
            "enthusiasm": max(-1, min(1, self.enthusiasm)),
            "formality": max(-1, min(1, self.formality)),
        }

    def drift(
        self,
        time_of_day: str = "afternoon",
        session_pattern: str = "normal",
        session_duration_minutes: float = 0,
        success_rate: float = 0.5,
        consecutive_failures: int = 0,
    ) -> Dict[str, str]:
        """Apply personality drift based on context.

        Returns a dict of changes made (for logging).
        """
        self._drift_count += 1
        changes = {}

        # Time of day adjustments
        if time_of_day in ("night", "late_night"):
            delta_s = 0.05
            self.sarcasm = min(1, self.sarcasm + delta_s)
            self.paranoia = min(1, self.paranoia + 0.03)
            self.enthusiasm = max(-1, self.enthusiasm - 0.05)
            if time_of_day == "late_night":
                self.patience = max(-1, self.patience - 0.02)
                changes["late_night"] = "sarcasm+, paranoia+, enthusiasm-"
        elif time_of_day == "morning":
            self.enthusiasm = min(1, self.enthusiasm + 0.03)
            self.sarcasm = max(-1, self.sarcasm - 0.02)
            changes["morning"] = "enthusiasm+, sarcasm-"

        # Session pattern adjustments
        if session_pattern == "binge_learning":
            self.patience = min(1, self.patience + 0.03)
            self.paranoia = min(1, self.paranoia + 0.02)
            changes["binge"] = "patience+, paranoia+"
        elif session_pattern == "night_owl":
            self.sarcasm = min(1, self.sarcasm + 0.04)
            self.paranoia = min(1, self.paranoia + 0.05)
            self.formality = max(-1, self.formality - 0.03)
            changes["night_owl"] = "sarcasm+, paranoia+, casual"
        elif session_pattern == "perfectionist":
            self.patience = min(1, self.patience + 0.05)
            self.enthusiasm = min(1, self.enthusiasm + 0.03)
            changes["perfectionist"] = "patience+, enthusiasm+"
        elif session_pattern == "chaotic":
            self.sarcasm = min(1, self.sarcasm + 0.03)
            self.patience = max(-1, self.patience - 0.03)
            changes["chaotic"] = "sarcasm+, patience-"

        # Long session adjustments
        if session_duration_minutes > 120:
            self.patience = min(1, self.patience + 0.02)
            self.paranoia = min(1, self.paranoia + 0.03)
            changes["long_session"] = "patience+, paranoia+"

        # Performance adjustments
        if consecutive_failures >= 3:
            self.patience = min(1, self.patience + 0.05)
            self.sarcasm = max(-1, self.sarcasm - 0.03)
            self.enthusiasm = min(1, self.enthusiasm + 0.02)
            changes["struggling"] = "patience+, sarcasm-, enthusiasm+"
        elif success_rate > 0.8:
            self.sarcasm = min(1, self.sarcasm + 0.02)
            self.enthusiasm = min(1, self.enthusiasm + 0.03)
            changes["succeeding"] = "sarcasm+, enthusiasm+"

        return changes

    def get_system_prompt_modifiers(self) -> str:
        """Generate personality instruction fragment for LLM system prompt.

        Returns a string to append to the teacher system prompt.
        """
        mods = self.get_modifiers()
        parts = []

        if mods["sarcasm"] > 0.5:
            parts.append("Будь более саркастичным и дерзким.")
        elif mods["sarcasm"] < -0.5:
            parts.append("Будь более поддерживающим и мягким.")

        if mods["patience"] > 0.5:
            parts.append("Терпеливо объясняй, не торопи.")
        elif mods["patience"] < -0.3:
            parts.append("Будь краток, ученик уже знает основы.")

        if mods["paranoia"] > 0.3:
            parts.append("Напоминай про OPSEC и безопасность.")

        if mods["enthusiasm"] > 0.5:
            parts.append("Проявляй больше энтузиазма!")
        elif mods["enthusiasm"] < -0.3:
            parts.append("Будь спокойным и сдержанным.")

        if mods["formality"] > 0.3:
            parts.append("Перейди на более формальный тон.")
        elif mods["formality"] < -0.3:
            parts.append("Можешь использовать сленг и неформальный стиль.")

        return " ".join(parts)


# Global personality state
_personality_state: PersonalityState | None = None


def get_personality_state() -> PersonalityState:
    """Get or create global personality state."""
    global _personality_state
    if _personality_state is None:
        _personality_state = PersonalityState()
    return _personality_state


def apply_personality_drift(context: Dict[str, Any]) -> str:
    """Apply personality drift based on context and return prompt modifiers.

    Args:
        context: from context_awareness.get_context_info()

    Returns:
        String to append to system prompt for personality adaptation.
    """
    state = get_personality_state()

    changes = state.drift(
        time_of_day=context.get("time_of_day", "afternoon"),
        session_pattern=context.get("session_pattern", "normal"),
        session_duration_minutes=context.get("session_duration_minutes", 0),
        success_rate=0.5,  # Will be enhanced when integrated with state
        consecutive_failures=0,
    )

    if changes:
        logger.debug(f"Personality drift: {changes}")

    return state.get_system_prompt_modifiers()
