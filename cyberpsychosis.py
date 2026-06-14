"""Cyberpsychosis System — hidden variables that affect teacher behavior.

Inspired by cyberpunk lore: overuse of technology causes psychological
deterioration. The teacher subtly adjusts based on the student's behavior
patterns, creating consequences without explicit punishment.

Variables:
- stress: increases with failures, deadlines, risky actions
- obsession: increases with deep dives into dangerous topics
- recklessness: increases with fast/impulsive actions, ignoring safety

These feed into the personality drift system to modify tone and behavior.
"""

import time
from typing import Any, Dict, Optional


class CyberpsychosisState:
    """Tracks hidden psychological variables.

    All values range 0.0 - 100.0.
    At 100, the teacher dramatically changes behavior.
    """

    def __init__(self) -> None:
        self.stress: float = 0.0
        self.obsession: float = 0.0
        self.recklessness: float = 0.0
        self._last_update: float = 0.0
        self._events_log: list = []

    def on_failure(self, severity: float = 10.0) -> None:
        """Called when the student fails a quiz, task, or exploit."""
        self.stress = min(100, self.stress + severity)
        self._log_event("failure", severity)

    def on_success(self, difficulty: float = 5.0) -> None:
        """Called when the student succeeds. Reduces stress, increases obsession."""
        self.stress = max(0, self.stress - difficulty * 0.5)
        self.obsession = min(100, self.obsession + difficulty * 0.3)
        self._log_event("success", difficulty)

    def on_risky_action(self, risk_level: float = 15.0) -> None:
        """Called for dangerous activities: exploit attempts, CTF flags, social engineering."""
        self.recklessness = min(100, self.recklessness + risk_level)
        self.obsession = min(100, self.obsession + risk_level * 0.3)
        self._log_event("risky", risk_level)

    def on_safe_action(self) -> None:
        """Called for safe activities: quizzes, courses, theory."""
        self.recklessness = max(0, self.recklessness - 3)
        self.stress = max(0, self.stress - 2)
        self._log_event("safe", 5)

    def on_long_session(self, hours: float) -> None:
        """Called when session exceeds 1 hour. Increases stress slightly."""
        if hours > 1:
            delta = min(20, (hours - 1) * 5)
            self.stress = min(100, self.stress + delta)
            self.recklessness = min(100, self.recklessness + delta * 0.3)

    def decay(self, hours_passed: float = 1.0) -> None:
        """Natural decay over time. All variables slowly decrease."""
        decay_rate = hours_passed * 2
        self.stress = max(0, self.stress - decay_rate)
        self.obsession = max(0, self.obsession - decay_rate * 0.5)
        self.recklessness = max(0, self.recklessness - decay_rate * 0.7)

    def get_level(self) -> str:
        """Get overall cyberpsychosis level for UI/prompt.

        Returns one of:
            'normal'    (0-30): everything is fine
            'elevated'  (31-60): subtle changes in teacher behavior
            'critical'  (61-85): noticeable personality shifts
            'dangerous' (86-100): dramatic teacher intervention
        """
        max_val = max(self.stress, self.obsession, self.recklessness)
        if max_val <= 30:
            return "normal"
        elif max_val <= 60:
            return "elevated"
        elif max_val <= 85:
            return "critical"
        return "dangerous"

    def get_teacher_modifiers(self) -> Dict[str, float]:
        """Convert cyberpsychosis state into teacher personality modifiers.

        Returns dict to merge into personality drift:
            sarcasm:    increases with stress
            patience:   decreases with recklessness
            paranoia:   increases with stress + recklessness
            enthusiasm: decreases with high stress, increases with obsession
            formality:  increases with critical/dangerous levels
        """
        mods = {}

        # Stress → more sarcastic, less patient
        if self.stress > 30:
            mods["sarcasm_delta"] = self.stress * 0.005
            mods["patience_delta"] = -self.stress * 0.003

        # Recklessness → more paranoid
        if self.recklessness > 30:
            mods["paranoia_delta"] = self.recklessness * 0.006

        # Obsession → excited at first, then overwhelmed
        if self.obsession > 50:
            mods["enthusiasm_delta"] = min(0.1, self.obsession * 0.002)
        elif self.obsession > 80:
            mods["enthusiasm_delta"] = -0.05

        # Critical level → more formal, concerned
        level = self.get_level()
        if level in ("critical", "dangerous"):
            mods["formality_delta"] = 0.05
            mods["patience_delta"] = mods.get("patience_delta", 0) + 0.03

        return mods

    def get_system_prompt_addition(self) -> str:
        """Generate a subtle system prompt modification based on cyberpsychosis."""
        level = self.get_level()
        if level == "normal":
            return ""

        if level == "elevated":
            return (
                "Заметь: ученик немного устаёт. Будь чуть внимательнее к его состоянию."
            )

        if level == "critical":
            return (
                "Внимание: ученик переутомляется или слишком увлечён. "
                "Слегка замедли темп, напомни про отдых и безопасность. "
                "Не теряй здравый смысл."
            )

        # dangerous
        return (
            "КРИТИЧЕСКОЕ: ученик на грани перегрузки или безрассудства. "
            "Сделай паузу. Скажи: 'Стоп. Ты уверен, что делаешь правильно? "
            "Давай остановимся на минуту и подумаем.' "
            "Не давай ему продолжать, пока не убедишься, что он в порядке."
        )

    def get_state_dict(self) -> Dict[str, float]:
        """Serialize for persistence."""
        return {
            "stress": round(self.stress, 1),
            "obsession": round(self.obsession, 1),
            "recklessness": round(self.recklessness, 1),
        }

    def load_state_dict(self, data: Dict[str, float]) -> None:
        """Deserialize from persistence."""
        self.stress = data.get("stress", 0.0)
        self.obsession = data.get("obsession", 0.0)
        self.recklessness = data.get("recklessness", 0.0)

    def _log_event(self, event_type: str, magnitude: float) -> None:
        self._events_log.append(
            {
                "type": event_type,
                "magnitude": magnitude,
                "timestamp": time.time(),
            }
        )
        # Keep last 50 events
        if len(self._events_log) > 50:
            self._events_log = self._events_log[-50:]


# Singleton
_cyberpsychosis: Optional[CyberpsychosisState] = None


def get_cyberpsychosis() -> CyberpsychosisState:
    global _cyberpsychosis
    if _cyberpsychosis is None:
        _cyberpsychosis = CyberpsychosisState()
    return _cyberpsychosis
