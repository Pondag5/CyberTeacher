"""Episode Memory — persists important learning events.

Unlike chat history (which is ephemeral), episode memory stores
meaningful moments: breakthroughs, failures, discoveries, milestones.

Used by the teacher to reference past experiences:
"Помнишь, когда ты в первый раз взломал SQL-инъекцию?.."
"""

import json
import os
import time
from typing import Any, Dict, List, Optional


def _episodes_file() -> str:
    try:
        from settings import get_settings

        return str(get_settings().episode_memory_file)
    except ImportError:
        return "./memory/episode_memory.json"


EPISODES_FILE = _episodes_file()
MAX_EPISODES = 500


# ─── Episode Categories ───
CATEGORY_ICONS = {
    "breakthrough": "🎯",
    "failure": "💥",
    "discovery": "🔍",
    "milestone": "🏆",
    "session": "📝",
    "social": "👥",
    "explore": "🗺️",
}

CATEGORY_LABELS = {
    "breakthrough": "Прорыв",
    "failure": "Неудача",
    "discovery": "Открытие",
    "milestone": "Веха",
    "session": "Сессия",
    "social": "Социальное",
    "explore": "Исследование",
}


class EpisodeMemory:
    """Stores and retrieves important learning episodes."""

    def __init__(self) -> None:
        self.episodes: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        try:
            if os.path.exists(EPISODES_FILE):
                with open(EPISODES_FILE, "r", encoding="utf-8") as f:
                    self.episodes = json.load(f)
        except (OSError, IOError, json.JSONDecodeError):
            self.episodes = []

    def save(self) -> None:
        os.makedirs(os.path.dirname(EPISODES_FILE), exist_ok=True)
        # Keep only most recent
        self.episodes = self.episodes[-MAX_EPISODES:]
        with open(EPISODES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.episodes, f, ensure_ascii=False, indent=2)

    def record(
        self,
        category: str,
        title: str,
        description: str = "",
        importance: int = 5,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record an important episode.

        Args:
            category: One of breakthrough/failure/discovery/milestone/session/social/explore
            title: Short title of the event
            description: Longer description
            importance: 1-10 (used for retrieval priority)
            context: Optional metadata (skill, topic, score, etc.)
        """
        episode = {
            "category": category,
            "title": title,
            "description": description,
            "importance": max(1, min(10, importance)),
            "timestamp": time.time(),
            "context": context or {},
        }
        self.episodes.append(episode)
        self.save()
        return episode

    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get N most recent episodes."""
        return self.episodes[-n:]

    def get_by_category(self, category: str, n: int = 10) -> List[Dict[str, Any]]:
        """Get N most recent episodes of a category."""
        filtered = [e for e in self.episodes if e["category"] == category]
        return filtered[-n:]

    def get_important(
        self, min_importance: int = 7, n: int = 10
    ) -> List[Dict[str, Any]]:
        """Get important episodes (high importance score)."""
        important = [e for e in self.episodes if e["importance"] >= min_importance]
        return important[-n:]

    def get_memory_prompt(self, n: int = 5) -> str:
        """Generate a memory section for the LLM system prompt.

        Includes the N most important/recent episodes to give the teacher
        context about the student's journey.
        """
        if not self.episodes:
            return ""

        # Mix: 2 most important + 3 most recent
        important = sorted(self.episodes, key=lambda e: e["importance"], reverse=True)[
            :2
        ]
        recent = self.episodes[-3:]
        # Deduplicate
        seen = set()
        selected = []
        for ep in important + recent:
            key = ep["title"]
            if key not in seen:
                seen.add(key)
                selected.append(ep)

        if not selected:
            return ""

        parts = ["=== EPISODE MEMORY (важные моменты ученика) ==="]
        for ep in selected:
            icon = CATEGORY_ICONS.get(ep["category"], "📌")
            ts = time.strftime("%Y-%m-%d", time.localtime(ep["timestamp"]))
            parts.append(f"  {icon} [{ts}] {ep['title']}")
            if ep["description"]:
                parts.append(f"     {ep['description'][:100]}")

        return "\n".join(parts)

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        cats: dict[str, int] = {}
        for ep in self.episodes:
            cat = ep["category"]
            cats[cat] = cats.get(cat, 0) + 1
        return {
            "total_episodes": len(self.episodes),
            "by_category": cats,
        }


# ─── Auto-recorder helpers ───


def record_breakthrough(
    memory: EpisodeMemory, title: str, detail: str = "", skill: str = ""
) -> None:
    """Record a breakthrough moment."""
    memory.record(
        "breakthrough",
        title,
        detail,
        importance=8,
        context={"skill": skill} if skill else {},
    )


def record_failure(
    memory: EpisodeMemory, title: str, detail: str = "", topic: str = ""
) -> None:
    """Record a failure (important for learning)."""
    memory.record(
        "failure",
        title,
        detail,
        importance=6,
        context={"topic": topic} if topic else {},
    )


def record_milestone(memory: EpisodeMemory, title: str, detail: str = "") -> None:
    """Record a milestone (level up, achievement, etc.)."""
    memory.record("milestone", title, detail, importance=9)


def record_discovery(memory: EpisodeMemory, title: str, detail: str = "") -> None:
    """Record a discovery (new faction, hidden knowledge, etc.)."""
    memory.record("discovery", title, detail, importance=7)


# Singleton
_episode_memory: Optional[EpisodeMemory] = None


def get_episode_memory() -> EpisodeMemory:
    global _episode_memory
    if _episode_memory is None:
        _episode_memory = EpisodeMemory()
    return _episode_memory
