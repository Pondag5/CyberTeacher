"""
Weak topics tracking service.
"""

from typing import Any


def update_weak_topic(
    weak_topics: list[dict[str, Any]],
    topic: str,
    score: float,
    max_score: float = 10.0,
) -> None:
    """Обновить статистику по слабой теме."""
    for entry in weak_topics:
        if entry["topic"] == topic:
            entry["attempts"] += 1
            entry["total_score"] += score
            entry["max_score"] += max_score
            entry["success_rate"] = (
                (entry["total_score"] / entry["max_score"]) * 100
                if entry["max_score"] > 0
                else 0
            )
            return

    weak_topics.append({
        "topic": topic,
        "attempts": 1,
        "total_score": score,
        "max_score": max_score,
        "success_rate": (score / max_score) * 100 if max_score > 0 else 0,
    })


def get_weak_topics(
    weak_topics: list[dict[str, Any]],
    threshold: float = 70.0,
) -> list[dict[str, Any]]:
    """Получить список тем с успешностью ниже threshold%."""
    weak = [t for t in weak_topics if t["success_rate"] < threshold]
    return sorted(weak, key=lambda x: x["success_rate"])


def get_next_weak_topic(
    weak_topics: list[dict[str, Any]],
    threshold: float = 70.0,
) -> str | None:
    """Получить следующую тему для фокуса (самую слабую)."""
    weak = get_weak_topics(weak_topics, threshold)
    return weak[0]["topic"] if weak else None
