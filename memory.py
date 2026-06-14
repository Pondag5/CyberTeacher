"""
💾 Операции с БД — SQLAlchemy abstraction layer
Поддерживает SQLite и PostgreSQL.
"""

import logging
import os
from datetime import timedelta
from typing import Any

from config import sanitize_log
from db import (
    Message,
    QueryCache,
    SessionLocal,
    Stat,
    TopicProgress,
    _utc_now_naive,
)
from db import (
    init_db as init_db_models,
)

logger = logging.getLogger(__name__)


def init_db() -> Any:
    """Инициализация БД через SQLAlchemy"""
    from settings import get_settings

    mem_dir = str(get_settings().state_file.parent)
    os.makedirs(mem_dir, exist_ok=True)
    init_db_models()
    return SessionLocal()


MAX_MESSAGE_LENGTH = 50000


def save_message(conn: Any, role: str, content: str, mode: str = "teacher") -> None:
    """Сохранить сообщение (обрезка до MAX_MESSAGE_LENGTH символов)"""
    if len(content) > MAX_MESSAGE_LENGTH:
        logger.warning(
            f"Truncating {role} message from {len(content)} to {MAX_MESSAGE_LENGTH}"
        )
        content = content[:MAX_MESSAGE_LENGTH]
    sanitized_content = sanitize_log(content)
    conn.add(
        Message(
            role=role,
            content=sanitized_content,
            timestamp=_utc_now_naive(),
            mode=mode,
        )
    )
    conn.commit()


def get_chat_history(conn: Any, limit: int = 10) -> list[dict[str, str]]:
    """Получить историю чата"""
    rows = conn.query(Message).order_by(Message.id.desc()).limit(limit).all()
    return [
        {"role": r.role, "content": r.content, "mode": r.mode} for r in reversed(rows)
    ]


def clear_chat(conn: Any) -> None:
    """Очистить чат"""
    conn.query(Message).delete()
    conn.commit()


# === ГЕЙМИФИКАЦИЯ ===


def update_stats(conn: Any, points: int, field: str = "points") -> None:
    """Обновить статистику"""
    stat = conn.query(Stat).first()
    if stat:
        stat.points += points
        stat.last_activity = _utc_now_naive()
        if field == "quizzes_passed":
            stat.quizzes_passed += 1
        elif field == "tasks_solved":
            stat.tasks_solved += 1
        conn.commit()


def get_stats(conn: Any) -> dict[str, int]:
    """Получить статистику"""
    stat = conn.query(Stat).first()
    if stat:
        return {
            "points": stat.points,
            "quizzes": stat.quizzes_passed,
            "tasks": stat.tasks_solved,
        }
    return {"points": 0, "quizzes": 0, "tasks": 0}


# === АДАПТИВНОЕ ОБУЧЕНИЕ ===


def update_topic_progress(conn: Any, topic: str, is_correct: bool) -> None:
    """Обновить прогресс по конкретной теме"""
    row = conn.query(TopicProgress).filter_by(topic=topic).first()
    now = _utc_now_naive()
    correct_inc = 1 if is_correct else 0

    if row:
        row.correct += correct_inc
        row.total += 1
        row.last_seen = now
    else:
        conn.add(
            TopicProgress(
                topic=topic,
                correct=correct_inc,
                total=1,
                last_seen=now,
            )
        )
    conn.commit()


def get_weak_topics(conn: Any, limit: int = 3) -> list[dict[str, Any]]:
    """Получить темы с худшим результатом (< 60% успеха)"""
    rows = conn.query(TopicProgress).filter(TopicProgress.total > 0).all()

    weak: list[dict[str, Any]] = [
        {
            "topic": r.topic,
            "correct": r.correct,
            "total": r.total,
            "rate": int(r.correct / r.total * 100) if r.total > 0 else 0,
        }
        for r in rows
        if r.total > 0 and (r.correct / r.total) < 0.6
    ]

    weak.sort(key=lambda x: x["rate"])
    return weak[:limit]


# === КЭШИРОВАНИЕ LLM ОТВЕТОВ ===


def cleanup_expired_cache(conn: Any) -> None:
    """Удалить просроченные записи кэша"""
    now = _utc_now_naive()
    conn.query(QueryCache).filter(
        QueryCache.expires_at.isnot(None),
        QueryCache.expires_at < now,
    ).delete()
    conn.commit()


def get_cached_response(conn: Any, query_hash: str) -> str | None:
    """Получить ответ из кэша если не просрочен"""
    from state import get_state

    row = conn.query(QueryCache).filter_by(query_hash=query_hash).first()
    state = get_state()
    if row:
        now = _utc_now_naive()
        if row.expires_at is None or row.expires_at > now:
            state.cache_hits += 1
            result: str | None = row.response
            return result
        conn.delete(row)
        conn.commit()
    state.cache_misses += 1
    return None


def cache_response(
    conn: Any, query_hash: str, response: str, ttl_seconds: int | None = None
) -> None:
    """Сохранить ответ в кэш с TTL"""
    now = _utc_now_naive()
    expires_at = None
    if ttl_seconds:
        expires_at = now + timedelta(seconds=ttl_seconds)

    existing = conn.query(QueryCache).filter_by(query_hash=query_hash).first()
    if existing:
        existing.response = response
        existing.created_at = now
        existing.expires_at = expires_at
        existing.ttl_seconds = ttl_seconds
    else:
        conn.add(
            QueryCache(
                query_hash=query_hash,
                response=response,
                created_at=now,
                expires_at=expires_at,
                ttl_seconds=ttl_seconds,
            )
        )
    conn.commit()
    total = conn.query(QueryCache).count()
    if total > 1000:
        now2 = _utc_now_naive()
        deleted = (
            conn.query(QueryCache)
            .filter(
                (QueryCache.expires_at.isnot(None)) & (QueryCache.expires_at < now2)
            )
            .delete()
        )
        if not deleted:
            newest = (
                conn.query(QueryCache.id)
                .order_by(QueryCache.created_at.desc())
                .limit(1000)
                .all()
            )
            if newest:
                min_keep = min(r[0] for r in newest)
                conn.query(QueryCache).filter(QueryCache.id < min_keep).delete()
        conn.commit()


def get_cache_stats(conn: Any) -> dict[str, int]:
    """Статистика кэша"""
    now = _utc_now_naive()
    total = conn.query(QueryCache).count()
    valid = (
        conn.query(QueryCache)
        .filter((QueryCache.expires_at.is_(None)) | (QueryCache.expires_at > now))
        .count()
    )
    return {"total": total, "valid": valid, "expired": total - valid}


def cleanup_old_messages(conn: Any, keep_last: int = 500) -> None:
    """
    Удаляет старые сообщения, оставляя только последние `keep_last` записей.
    Вызывать при старте или периодически.
    """
    from db import Message

    oldest_to_keep = (
        conn.query(Message.id).order_by(Message.id.desc()).limit(keep_last).all()
    )
    if not oldest_to_keep:
        return
    min_id_to_keep = min(row[0] for row in oldest_to_keep)
    deleted = conn.query(Message).filter(Message.id < min_id_to_keep).delete()
    if deleted:
        logger.info(f"Очищено старых сообщений: {deleted}")
    conn.commit()
