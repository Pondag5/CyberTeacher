"""Persistent World State — incidents, factions, hidden knowledge.

The world evolves based on user actions. Creates a sense of a living,
persistent cyberpunk universe that reacts to the learner's behavior.

Key concepts:
- Active Incidents: security events that appear and resolve
- Factions: organizations the user discovers over time
- Hidden Knowledge: advanced topics locked behind progression
"""

import json
import os
import random
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


WORLD_FILE = "./memory/world_state.json"


# ─── Incident Templates ───
INCIDENT_TEMPLATES = [
    {
        "id": "netwatch_anomaly",
        "title": "NetWatch Anomaly Detected",
        "desc": "Необычная сетевая активность обнаружена в сегменте B7.",
        "severity": "low",
        "category": "network",
        "resolve_condition": "quiz_perfect",
        "xp_reward": 30,
    },
    {
        "id": "rogue_ai_signal",
        "title": "Rogue AI Signal",
        "desc": "Признаки несанкционированного ИИ-процесса в даркнете.",
        "severity": "medium",
        "category": "ai",
        "resolve_condition": "exploit_success",
        "xp_reward": 50,
    },
    {
        "id": "militech_breach",
        "title": "Militech Data Breach",
        "desc": "Утечка данных корпорации Militech. Требуется анализ.",
        "severity": "high",
        "category": "corporate",
        "resolve_condition": "scan_clean",
        "xp_reward": 80,
    },
    {
        "id": "phishing_wave",
        "title": "Phishing Campaign Active",
        "desc": "Волна фишинговых атак на сотрудников компаний.",
        "severity": "low",
        "category": "social",
        "resolve_condition": "social_engineer",
        "xp_reward": 25,
    },
    {
        "id": "zero_day_leak",
        "title": "Zero-Day Exploit Leaked",
        "desc": "Утечка эксплойта нулевого дня. Критическая угроза.",
        "severity": "critical",
        "category": "exploit",
        "resolve_condition": "flag_capture",
        "xp_reward": 120,
    },
    {
        "id": "ransomware_outbreak",
        "title": "Ransomware Outbreak",
        "desc": "Вспышка шифровальщика в корпоративной сети.",
        "severity": "high",
        "category": "malware",
        "resolve_condition": "malware_analysis",
        "xp_reward": 100,
    },
    {
        "id": "dns_poisoning",
        "title": "DNS Poisoning Detected",
        "desc": "Обнаружено отравление DNS-записей.",
        "severity": "medium",
        "category": "network",
        "resolve_condition": "lab_complete",
        "xp_reward": 40,
    },
    {
        "id": "insider_threat",
        "title": "Insider Threat Alert",
        "desc": "Подозрительная активность от внутреннего сотрудника.",
        "severity": "medium",
        "category": "social",
        "resolve_condition": "investigation",
        "xp_reward": 60,
    },
]


# ─── Faction Definitions ───
FACTIONS = [
    {
        "id": "netwatch",
        "name": "NetWatch",
        "desc": "Кибер-полиция, следящая за сетью.",
        "alignment": "lawful",
        "unlock_condition": "quizzes_taken >= 5",
        "lore": "NetWatch — элитное подразделение кибер-полиции. Они защищают сеть от хакеров и корпоративных шпионов.",
    },
    {
        "id": "valkyrie",
        "name": "Valkyrie Corps",
        "desc": "Хакерская группа свободы.",
        "alignment": "chaotic",
        "unlock_condition": "exploit_success >= 3",
        "lore": "Valkyrie Corps — анархисты-хакеры, борющиеся с корпоративным контролем. Их методы радикальны, но цели благородны.",
    },
    {
        "id": "araska",
        "name": "Arasaka Intel",
        "desc": "Корпоративная разведка.",
        "alignment": "corporate",
        "unlock_condition": "apt_groups_viewed >= 10",
        "lore": "Arasaka Intel — теневое крыло корпорации. Они знают всё обо всех. За информацию нужно платить.",
    },
    {
        "id": "ghosts",
        "name": "Digital Ghosts",
        "desc": "Легенды даркнета.",
        "alignment": "neutral",
        "unlock_condition": "stealth_ops >= 5",
        "lore": "Digital Ghosts — мифические хакеры, которые якобы существуют только в сети. Никто не знает их настоящих имён.",
    },
]


# ─── Hidden Knowledge ───
HIDDEN_KNOWLEDGE = [
    {
        "id": "advanced_sql_injection",
        "title": "Advanced SQL Injection Techniques",
        "desc": "Продвинутые техники SQL-инъекций: blind, time-based, stacked queries.",
        "unlock_condition": "skills.web_security >= 3",
        "category": "web",
    },
    {
        "id": "binary_exploitation",
        "title": "Binary Exploitation & ROP",
        "desc": "Эксплуатация бинарников: buffer overflow, ROP chains, shellcode.",
        "unlock_condition": "skills.binary_analysis >= 3",
        "category": "systems",
    },
    {
        "id": "active_directory",
        "title": "Active Directory Attacks",
        "desc": "Атаки на AD: Kerberoasting, Pass-the-Hash, DCSync.",
        "unlock_condition": "labs_started >= 10",
        "category": "network",
    },
    {
        "id": "reverse_engineering",
        "title": "Reverse Engineering with Ghidra",
        "desc": "Обратный инжиниринг: анализ бинарников, decompilation, patching.",
        "unlock_condition": "skills.reverse_engineering >= 2",
        "category": "systems",
    },
    {
        "id": "c2_frameworks",
        "title": "Command & Control Frameworks",
        "desc": "C2-инфраструктура: Sliver, Cobalt Strike, Mythic.",
        "unlock_condition": "tracks_completed >= 2",
        "category": "offensive",
    },
]


class WorldState:
    """Persistent world that evolves with the user."""

    def __init__(self) -> None:
        self.incidents: List[Dict[str, Any]] = []
        self.resolved_incidents: List[Dict[str, Any]] = []
        self.discovered_factions: List[str] = []
        self.unlocked_knowledge: List[str] = []
        self.world_events: List[Dict[str, Any]] = []
        self.last_incident_check: float = 0.0
        self._load()

    def _load(self) -> None:
        try:
            if os.path.exists(WORLD_FILE):
                with open(WORLD_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.incidents = data.get("incidents", [])
                self.resolved_incidents = data.get("resolved_incidents", [])
                self.discovered_factions = data.get("discovered_factions", [])
                self.unlocked_knowledge = data.get("unlocked_knowledge", [])
                self.world_events = data.get("world_events", [])
                self.last_incident_check = data.get("last_incident_check", 0.0)
        except (OSError, IOError, json.JSONDecodeError):
            pass

    def save(self) -> None:
        os.makedirs(os.path.dirname(WORLD_FILE), exist_ok=True)
        data = {
            "incidents": self.incidents,
            "resolved_incidents": self.resolved_incidents,
            "discovered_factions": self.discovered_factions,
            "unlocked_knowledge": self.unlocked_knowledge,
            "world_events": self.world_events[-100:],  # Cap events
            "last_incident_check": self.last_incident_check,
        }
        with open(WORLD_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def check_spawn_incident(self, state: Any) -> Optional[Dict[str, Any]]:
        """Maybe spawn a new incident based on time and state."""
        now = time.time()
        # Spawn max 1 incident per 30 minutes
        if now - self.last_incident_check < 1800:
            return None
        self.last_incident_check = now

        # Max 3 active incidents
        if len(self.incidents) >= 3:
            return None

        # 30% chance to spawn
        if random.random() > 0.3:
            return None

        # Pick a random incident not already active
        active_ids = {i["id"] for i in self.incidents}
        available = [t for t in INCIDENT_TEMPLATES if t["id"] not in active_ids]
        if not available:
            return None

        template = random.choice(available)
        incident = {
            **template,
            "spawned_at": now,
            "active": True,
        }
        self.incidents.append(incident)
        self._log_event("incident_spawned", str(incident["id"]), str(incident["title"]))
        self.save()
        return incident

    def resolve_incident(self, incident_id: str, xp_awarded: int = 0) -> bool:
        """Resolve an active incident."""
        for i, inc in enumerate(self.incidents):
            if inc["id"] == incident_id:
                resolved = self.incidents.pop(i)
                resolved["resolved_at"] = time.time()
                resolved["xp_awarded"] = xp_awarded
                self.resolved_incidents.append(resolved)
                self._log_event("incident_resolved", incident_id, resolved["title"])
                self.save()
                return True
        return False

    def check_discover_faction(self, state: Any) -> Optional[Dict[str, Any]]:
        """Check if a new faction should be discovered."""
        for faction in FACTIONS:
            if faction["id"] in self.discovered_factions:
                continue
            if self._check_condition(faction["unlock_condition"], state):
                self.discovered_factions.append(faction["id"])
                self._log_event("faction_discovered", faction["id"], faction["name"])
                self.save()
                return faction
        return None

    def check_unlock_knowledge(self, state: Any) -> Optional[Dict[str, Any]]:
        """Check if hidden knowledge should be unlocked."""
        for knowledge in HIDDEN_KNOWLEDGE:
            if knowledge["id"] in self.unlocked_knowledge:
                continue
            if self._check_condition(knowledge["unlock_condition"], state):
                self.unlocked_knowledge.append(knowledge["id"])
                self._log_event(
                    "knowledge_unlocked", knowledge["id"], knowledge["title"]
                )
                self.save()
                return knowledge
        return None

    def _check_condition(self, condition: str, state: Any) -> bool:
        """Evaluate a simple condition string against state.
        Supports dot-notation: 'skills.web_security >= 3'."""
        try:
            import operator

            ops = {
                ">=": operator.ge,
                "<=": operator.le,
                ">": operator.gt,
                "<": operator.lt,
                "==": operator.eq,
            }
            for op_str, op_func in ops.items():
                if op_str in condition:
                    left, right = condition.split(op_str, 1)
                    left = left.strip()
                    right = right.strip()
                    # Handle dot-notation: skills.web_security
                    if "." in left:
                        parts = left.split(".")
                        state_val: Any = state
                        for part in parts:
                            if isinstance(state_val, dict):
                                state_val = state_val.get(part, 0)
                            else:
                                state_val = getattr(state_val, part, 0)
                    else:
                        state_val = getattr(state, left, 0)
                    if isinstance(state_val, (list, dict)):
                        state_val = len(state_val)
                    result: bool = op_func(float(state_val), float(right))
                    return result
        except (ValueError, AttributeError, TypeError):
            pass
        return False

    def get_world_summary(self) -> Dict[str, Any]:
        """Get a summary of the world state for the system prompt."""
        return {
            "active_incidents": len(self.incidents),
            "resolved_incidents": len(self.resolved_incidents),
            "discovered_factions": [
                f["name"] for f in FACTIONS if f["id"] in self.discovered_factions
            ],
            "unlocked_knowledge": [
                k["title"]
                for k in HIDDEN_KNOWLEDGE
                if k["id"] in self.unlocked_knowledge
            ],
            "incidents": [
                {"title": i["title"], "severity": i["severity"], "desc": i["desc"]}
                for i in self.incidents
            ],
        }

    def get_world_prompt(self) -> str:
        """Generate a world state section for the LLM system prompt."""
        summary = self.get_world_summary()
        parts = ["=== PERSISTENT WORLD STATE ==="]

        if summary["active_incidents"] > 0:
            parts.append("Active Incidents:")
            for inc in summary["incidents"]:
                parts.append(
                    f"  [{inc['severity'].upper()}] {inc['title']}: {inc['desc']}"
                )

        if summary["discovered_factions"]:
            parts.append(f"Known Factions: {', '.join(summary['discovered_factions'])}")

        if summary["unlocked_knowledge"]:
            parts.append(
                f"Unlocked Advanced Topics: {', '.join(summary['unlocked_knowledge'])}"
            )

        if summary["resolved_incidents"] > 0:
            parts.append(f"Total incidents resolved: {summary['resolved_incidents']}")

        return "\n".join(parts) if len(parts) > 1 else ""

    def _log_event(self, event_type: str, event_id: str, title: str) -> None:
        self.world_events.append(
            {
                "type": event_type,
                "id": event_id,
                "title": title,
                "timestamp": time.time(),
            }
        )


# Singleton
_world_state: Optional[WorldState] = None


def get_world_state() -> WorldState:
    global _world_state
    if _world_state is None:
        _world_state = WorldState()
    return _world_state
