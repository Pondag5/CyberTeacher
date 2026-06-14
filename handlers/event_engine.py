"""Narrative event engine — evaluates trigger conditions and fires story events."""

import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from state import get_state

EVENTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "events", "narrative_events.json"
)


def _resolve_metric(name: str) -> Any:
    state = get_state()
    metric_map = {
        "xp": lambda: state.xp,
        "level": lambda: state.level,
        "stealth_ops": lambda: state.stealth_ops,
        "digital_debts": lambda: state.digital_debts,
        "dirty_logs": lambda: len(getattr(state, "dirty_logs", [])),
        "flags_captured": lambda: getattr(state, "flags_captured", 0),
        "current_chapter": lambda: state.current_chapter,
        "noise_level": lambda: state.noise_level,
        "achievements_count": lambda: len(getattr(state, "earned_achievements", [])),
        "night_sessions": lambda: getattr(state, "night_sessions", 0),
        "trace": lambda: getattr(state, "trace_count", 0),
        "cp_level": lambda: _get_cp_level(),
    }
    getter = metric_map.get(name)
    if getter is None:
        return 0
    try:
        return getter()
    except (ValueError, KeyError, TypeError, RuntimeError):
        return 0


def _get_cp_level() -> float:
    try:
        from cyberpsychosis import CyberpsychosisState

        st = CyberpsychosisState()
        return round((st.stress + st.obsession + st.recklessness) / 3, 1)
    except (ImportError, RuntimeError):
        return 0.0


def load_events() -> List[Dict[str, Any]]:
    try:
        if not os.path.exists(EVENTS_PATH):
            return []
        with open(EVENTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, IOError, json.JSONDecodeError):
        return []


def get_fired_events() -> List[str]:
    state = get_state()
    return list(getattr(state, "fired_events", []))


def mark_event_fired(event_id: str) -> None:
    state = get_state()
    fired = getattr(state, "fired_events", None)
    if fired is None:
        fired = []
        state.fired_events = fired
    if event_id not in fired:
        fired.append(event_id)


def _check_conditions(
    condition: Dict[str, Any], fired: List[str], current_hour: int
) -> bool:
    if not condition:
        return True

    for eid in condition.get("not_fired", []):
        if eid in fired:
            return False

    for eid in condition.get("fired_before", []):
        if eid not in fired:
            return False

    min_h = condition.get("min_hour")
    if min_h is not None and current_hour < min_h:
        return False
    max_h = condition.get("max_hour")
    if max_h is not None and current_hour > max_h:
        return False

    return True


def _check_trigger(trigger: Dict[str, Any]) -> bool:
    ttype = trigger.get("type", "threshold")

    if ttype == "threshold":
        metric = _resolve_metric(trigger["metric"])
        op = trigger.get("op", ">=")
        value = trigger["value"]
        if op == ">=":
            return metric >= value
        elif op == "<=":
            return metric <= value
        elif op == ">":
            return metric > value
        elif op == "<":
            return metric < value
        elif op == "==":
            return metric == value
        return False

    elif ttype == "and":
        return all(_check_trigger(t) for t in trigger.get("triggers", []))

    elif ttype == "or":
        return any(_check_trigger(t) for t in trigger.get("triggers", []))

    return False


def _apply_effects(effects: Dict[str, Any]) -> List[str]:
    messages = []
    state = get_state()
    if not effects:
        return messages

    if "xp" in effects:
        val = effects["xp"]
        state.xp = max(0, state.xp + val)
        messages.append(f"{'+' if val >= 0 else ''}{val} XP")

    if "noise" in effects:
        val = effects["noise"]
        state.noise_level = max(0, state.noise_level + val)
        messages.append(f"{'+' if val >= 0 else ''}{val} шума")

    if "trace" in effects:
        val = effects["trace"]
        current = getattr(state, "trace_count", 0)
        state.trace_count = max(0, current + val)
        messages.append(f"{'+' if val >= 0 else ''}{val} trace")

    if "hint_block" in effects and effects["hint_block"]:
        state.hint_enabled = False
        messages.append("подсказки отключены")

    if "cp" in effects:
        val = effects["cp"]
        try:
            from cyberpsychosis import get_cyberpsychosis

            cp = get_cyberpsychosis()
            cp.on_risky_action(val)
            messages.append(f"{'+' if val >= 0 else ''}{val} CP")
        except (ImportError, RuntimeError):
            pass

    return messages


def check_events() -> List[Dict[str, Any]]:
    """Evaluate all narrative events and fire those whose triggers pass."""
    events = load_events()
    if not events:
        return []

    fired_ids = get_fired_events()
    now = time.localtime()
    current_hour = now.tm_hour

    results = []
    for event in events:
        eid = event.get("id", "")
        if not eid:
            continue
        if event.get("once") and eid in fired_ids:
            continue

        condition = event.get("condition", {})
        if not _check_conditions(condition, fired_ids, current_hour):
            continue

        trigger = event.get("trigger", {})
        if not trigger:
            continue
        if not _check_trigger(trigger):
            continue

        mark_event_fired(eid)
        fired_ids.append(eid)
        action = event.get("action", {})
        effects = event.get("effects", {})
        effect_msgs = _apply_effects(effects)

        results.append(
            {
                "id": eid,
                "title": event.get("title", ""),
                "message": action.get("message", ""),
                "effects": effect_msgs,
            }
        )

    return results
