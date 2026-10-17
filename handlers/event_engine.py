"""
Event Engine — narrative event system with trigger conditions and effects.
Module-level functions that delegate to EventEngine singleton.
"""
import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

# Module-level singleton
_event_engine = None

# Default events path (patched in tests)
EVENTS_PATH = "./events"


def get_event_engine() -> "EventEngine":
    """Get the singleton EventEngine instance."""
    global _event_engine
    if _event_engine is None:
        _event_engine = EventEngine()
    return _event_engine


# --- Module-level functions (primary API) ---

def load_events(path: Optional[str] = None) -> List[Dict]:
    """Load events from EVENTS_PATH (or given path)."""
    return get_event_engine().load_events(path or EVENTS_PATH)


def load_events_from_file(path: str) -> List[Dict]:
    """Load events from a specific JSON file."""
    return get_event_engine().load_events_from_file(path)


def get_fired_events() -> List[str]:
    """Get list of fired event IDs."""
    return get_event_engine().get_fired_events()


def mark_event_fired(event_id: str) -> None:
    """Mark an event as fired."""
    get_event_engine().mark_event_fired(event_id)


def check_events(state=None) -> List[Dict]:
    """Check for events that should fire given current state."""
    return get_event_engine().check_events(state)


def check_events_in_main_loop():
    """Check and fire events in main loop - for integration with main.py."""
    from state import get_state
    state = get_state()
    engine = get_event_engine()
    fired = engine.check_events(state)
    for event in fired:
        engine.fire_event(event)


# --- Expose internal methods on module for testing ---

def _resolve_metric(metric: str, state=None):
    from state import get_state
    if state is None:
        state = get_state()
    return get_event_engine()._resolve_metric(metric, state)


def _check_trigger(trigger: Dict, state=None):
    from state import get_state
    if state is None:
        state = get_state()
    return get_event_engine()._check_trigger(trigger, state)


def _check_conditions(conditions: Dict, fired_events: List[str], current_hour: int) -> bool:
    return get_event_engine()._check_conditions(conditions, fired_events, current_hour)


def _apply_effects(effects: Dict, state=None):
    from state import get_state
    if state is None:
        state = get_state()
    return get_event_engine()._apply_effects(effects, state)


class EventEngine:
    """Narrative event engine: loads events, evaluates triggers/conditions, applies effects."""

    def __init__(self):
        self._events_cache: List[Dict] = []
        self._events_path: str = EVENTS_PATH
        self._last_load_time: float = 0
        self._lock = __import__("threading").Lock()

    # --- Loading ---

    def load_events(self, path: Optional[str] = None) -> List[Dict]:
        """Load events from JSON file or directory."""
        if path is not None:
            self._events_path = path
        # If path is a file, load from file; otherwise load from directory
        if os.path.isfile(self._events_path):
            events = self._load_from_file(self._events_path)
        else:
            events = self._load_from_dir(self._events_path)

        self._events_cache = events
        self._last_load_time = time.time()
        return events

    def load_events_from_file(self, path: str) -> List[Dict]:
        """Load events from a single JSON file."""
        return self._load_from_file(path)

    def _load_from_dir(self, path: str) -> List[Dict]:
        events = []
        if not os.path.isdir(path):
            return events
        for fname in sorted(os.listdir(path)):
            if fname.endswith(".json"):
                fpath = os.path.join(path, fname)
                events.extend(self._load_from_file(fpath))
        self._events_cache = events
        self._last_load_time = time.time()
        return events

    def _load_from_file(self, path: str) -> List[Dict]:
        if not os.path.isfile(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "events" in data:
                return data["events"]
            return []
        except (json.JSONDecodeError, OSError):
            return []

    # --- Fired events tracking ---

    def get_fired_events(self) -> List[str]:
        from state import get_state
        state = get_state()
        return list(getattr(state, "fired_events", []))

    def mark_event_fired(self, event_id: str) -> None:
        from state import get_state
        state = get_state()
        if not hasattr(state, "fired_events"):
            state.fired_events = []
        if event_id not in state.fired_events:
            state.fired_events.append(event_id)

    # --- Metric resolution ---

    def _resolve_metric(self, metric: str, state) -> float:
        """Resolve a metric name to a numeric value from state."""
        if metric == "xp":
            return getattr(state, "xp", 0)
        if metric == "stealth_ops":
            return getattr(state, "stealth_ops", 0)
        if metric == "digital_debts":
            return getattr(state, "digital_debts", 0)
        if metric == "dirty_logs":
            dirty_logs = getattr(state, "dirty_logs", [])
            return len(dirty_logs) if isinstance(dirty_logs, list) else 0
        if metric == "flags_captured":
            return getattr(state, "flags_captured", 0)
        if metric == "current_chapter":
            return getattr(state, "current_chapter", 1)
        if metric == "noise_level":
            return getattr(state, "noise_level", 0)
        if metric == "achievements_count":
            achievements = getattr(state, "earned_achievements", [])
            return len(achievements) if isinstance(achievements, list) else 0
        if metric == "night_sessions":
            return getattr(state, "night_sessions", 0)
        if metric == "trace":
            return getattr(state, "trace_count", getattr(state, "trace", 0))
        return 0

    # --- Trigger evaluation ---

    def _check_trigger(self, trigger: Dict, state) -> bool:
        """Evaluate a trigger condition against state."""
        if not trigger or not isinstance(trigger, dict):
            return False

        ttype = trigger.get("type")

        if ttype == "threshold":
            metric = trigger.get("metric")
            op = trigger.get("op", ">=")
            value = trigger.get("value", 0)
            current = self._resolve_metric(metric, state)
            if op == ">=":
                return current >= value
            if op == "<=":
                return current <= value
            if op == ">":
                return current > value
            if op == "<":
                return current < value
            if op == "==":
                return current == value
            if op == "!=":
                return current != value
            return False

        if ttype == "and":
            triggers = trigger.get("triggers", [])
            return all(self._check_trigger(t, state) for t in triggers)

        if ttype == "or":
            triggers = trigger.get("triggers", [])
            return any(self._check_trigger(t, state) for t in triggers)

        return False

    # --- Condition evaluation ---

    def _check_conditions(self, conditions: Dict, fired_events: List[str], current_hour: int) -> bool:
        """Evaluate event conditions."""
        if not conditions:
            return True

        # not_fired: event must NOT have fired before
        if "not_fired" in conditions:
            for ev in conditions["not_fired"]:
                if ev in fired_events:
                    return False

        # fired_before: event MUST have fired before
        if "fired_before" in conditions:
            for ev in conditions["fired_before"]:
                if ev not in fired_events:
                    return False

        # min_hour / max_hour: time window
        if "min_hour" in conditions:
            if current_hour < conditions["min_hour"]:
                return False
        if "max_hour" in conditions:
            if current_hour > conditions["max_hour"]:
                return False

        return True

    # --- Effect application ---

    def _apply_effects(self, effects: Dict, state) -> List[str]:
        """Apply effects to state, return list of message strings."""
        messages = []
        if not effects:
            return messages

        if "xp" in effects:
            delta = effects["xp"]
            state.xp = getattr(state, "xp", 0) + delta
            if delta >= 0:
                messages.append(f"+{delta} XP")
            else:
                messages.append(f"{delta} XP")

        if "noise" in effects:
            delta = effects["noise"]
            state.noise_level = getattr(state, "noise_level", 0) + delta
            if delta >= 0:
                messages.append(f"+{delta} Noise")
            else:
                messages.append(f"{delta} Noise")

        if "trace" in effects:
            delta = effects["trace"]
            state.trace_count = getattr(state, "trace_count", 0) + delta
            if delta >= 0:
                messages.append(f"+{delta} Trace")
            else:
                messages.append(f"{delta} Trace")

        if "hint_block" in effects and effects["hint_block"]:
            state.hint_enabled = False
            messages.append("Hints disabled")

        return messages

    # --- Event checking ---

    def check_events(self, state=None) -> List[Dict]:
        """Check all events against state, return list of events that should fire."""
        from state import get_state

        if state is None:
            state = get_state()

        # Auto-load events if not already loaded
        if not self._events_cache:
            self.load_events()

        fired_events = self.get_fired_events()
        current_hour = datetime.now().hour
        results = []

        for event in self._events_cache:
            if not isinstance(event, dict):
                continue
            event_id = event.get("id")
            if not event_id:
                continue
            if event_id in fired_events:
                continue

            trigger = event.get("trigger")
            if not trigger or not self._check_trigger(trigger, state):
                continue

            conditions = event.get("condition", {})
            if not self._check_conditions(conditions, fired_events, current_hour):
                continue

            # Event fires!
            effects = event.get("effects", {})
            msgs = self._apply_effects(effects, state)

            result = {
                "id": event_id,
                "title": event.get("title", event_id),
                "message": event.get("action", {}).get("message", ""),
                "effects": msgs,
            }
            if event.get("once", True):
                self.mark_event_fired(event_id)

            results.append(result)

        return results

    def fire_event(self, event: Dict) -> None:
        """Manually fire an event (apply effects, mark fired)."""
        from state import get_state
        state = get_state()
        event_id = event.get("id")
        if event_id:
            self.mark_event_fired(event_id)
        effects = event.get("effects", {})
        self._apply_effects(effects, state)