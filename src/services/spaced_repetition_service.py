"""
Spaced repetition (SM-2) service.
"""

import time
from typing import Any


def compute_next_review(interval_days: int) -> float:
    """Вычислить timestamp следующего повторения."""
    return time.time() + interval_days * 86400


def schedule_review(
    review_schedule: dict[str, Any],
    topic: str,
    grade: float,
    max_grade: float = 10.0,
) -> None:
    """Запланировать повторение для темы (SM-2 algorithm simplified)."""
    quality = (grade / max_grade) * 5

    if topic not in review_schedule:
        review_schedule[topic] = {
            "repetitions": 0,
            "interval": 1,
            "next_review": compute_next_review(1),
            "last_grade": grade,
            "ef": 2.5,
        }
    else:
        entry = review_schedule[topic]
        repetitions = entry.get("repetitions", 0)
        interval = entry.get("interval", 1)
        ef = entry.get("ef", 2.5)

        if quality < 3:
            repetitions = 0
            interval = 1
            ef = 2.5
            entry["repetitions"] = repetitions
            entry["interval"] = interval
            entry["ef"] = ef
        else:
            repetitions += 1
            if repetitions == 1:
                interval = 1
            elif repetitions == 2:
                interval = 3
            else:
                new_ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
                new_ef = max(1.3, new_ef)
                entry["ef"] = new_ef
                interval = max(1, int(interval * new_ef))
            entry["repetitions"] = repetitions
            entry["interval"] = interval

        entry["next_review"] = compute_next_review(interval)
        entry["last_grade"] = grade


def get_due_reviews(review_schedule: dict[str, Any]) -> list[dict[str, Any]]:
    """Получить темы, готовые к повторению."""
    now = time.time()
    due = []
    for topic, entry in review_schedule.items():
        if entry.get("next_review", 0) <= now:
            due.append(
                {
                    "topic": topic,
                    "interval": entry.get("interval", 0),
                    "repetitions": entry.get("repetitions", 0),
                }
            )
    due.sort(key=lambda x: review_schedule[x["topic"]]["next_review"])
    return due
