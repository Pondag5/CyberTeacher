import os
import sqlite3
from datetime import datetime

from config import DB_FILE
from ui import console


def init_db():
    """Инициализация БД с безопасной миграцией"""
    os.makedirs("./memory", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 1. Таблица сообщений
    c.execute("""CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, role TEXT, content TEXT,
                  timestamp TEXT, mode TEXT DEFAULT 'teacher')""")

    # 2. Таблица статистики
    c.execute("""CREATE TABLE IF NOT EXISTS stats
                 (id INTEGER PRIMARY KEY, 
                  points INTEGER DEFAULT 0,
                  quizzes_passed INTEGER DEFAULT 0,
                  tasks_solved INTEGER DEFAULT 0,
                  last_activity TEXT)""")

    # 3. Таблица прогресса (Адаптивное обучение)
    # Проверяем, существует ли таблица
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='progress'")
    table_exists = c.fetchone()

    if not table_exists:
        # Если таблицы нет — создаем новую
        c.execute("""CREATE TABLE progress
                     (topic TEXT PRIMARY KEY, 
                      correct INTEGER DEFAULT 0,
                      total INTEGER DEFAULT 0,
                      last_seen TEXT)""")
        print("База данных: Создана таблица прогресса.")
    else:
        # Если таблица есть — проверяем наличие колонок (МИГРАЦИЯ)
        c.execute("PRAGMA table_info(progress)")
        columns = [info[1] for info in c.fetchall()]

        if "correct" not in columns:
            c.execute("ALTER TABLE progress ADD COLUMN correct INTEGER DEFAULT 0")
            print("База данных: Добавлена колонка 'correct'.")

        if "total" not in columns:
            c.execute("ALTER TABLE progress ADD COLUMN total INTEGER DEFAULT 0")
            print("База данных: Добавлена колонка 'total'.")

        if "last_seen" not in columns:
            c.execute("ALTER TABLE progress ADD COLUMN last_seen TEXT")
            print("База данных: Добавлена колонка 'last_seen'.")

    # 4. Таблица кэша ответов LLM (с TTL)
    c.execute("""CREATE TABLE IF NOT EXISTS query_cache
                 (query_hash TEXT PRIMARY KEY,
                  response TEXT,
                  created_at TEXT,
                  expires_at TEXT,
                  ttl_seconds INTEGER)""")

    # Проверяем, есть ли запись статистики
    c.execute("SELECT count(*) FROM stats")
    if c.fetchone()[0] == 0:
        c.execute(
            "INSERT INTO stats (points, last_activity) VALUES (0, ?)",
            (datetime.now().isoformat(),),
        )

    conn.commit()
    return conn


def save_message(conn, role: str, content: str, mode: str = "teacher"):
    """Сохранить сообщение (с санитизацией)"""
    from config import sanitize_log

    # Санитизируем контент перед сохранением
    sanitized_content = sanitize_log(content)

    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (role, content, timestamp, mode) VALUES (?, ?, ?, ?)",
        (role, sanitized_content, datetime.now().isoformat(), mode),
    )
    conn.commit()


def get_chat_history(conn, limit: int = 10):
    """Получить историю чата"""
    c = conn.cursor()
    c.execute(
        "SELECT role, content, mode FROM messages ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = c.fetchall()
    return [
        {"role": row[0], "content": row[1], "mode": row[2]} for row in reversed(rows)
    ]


def clear_chat(conn):
    """Очистить чат"""
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()


# === ГЕЙМИФИКАЦИЯ ===
def update_stats(conn, points: int, field: str = "points"):
    """Обновить статистику"""
    c = conn.cursor()
    now = datetime.now().isoformat()

    # ✅ Безопасное обновление - все поля параметризованы
    quizzes_inc = 1 if field == "quizzes_passed" else 0
    tasks_inc = 1 if field == "tasks_solved" else 0

    c.execute(
        "UPDATE stats SET points = points + ?, quizzes_passed = quizzes_passed + ?, tasks_solved = tasks_solved + ?, last_activity = ?",
        (points, quizzes_inc, tasks_inc, now),
    )
    conn.commit()


def get_stats(conn):
    """Получить статистику"""
    c = conn.cursor()
    c.execute("SELECT points, quizzes_passed, tasks_solved FROM stats LIMIT 1")
    row = c.fetchone()
    if row:
        return {"points": row[0], "quizzes": row[1], "tasks": row[2]}
    return {"points": 0, "quizzes": 0, "tasks": 0}


# === АДАПТИВНОЕ ОБУЧЕНИЕ ===
def update_topic_progress(conn, topic: str, is_correct: bool):
    """Обновить прогресс по конкретной теме"""
    c = conn.cursor()
    c.execute("SELECT correct, total FROM progress WHERE topic = ?", (topic,))
    row = c.fetchone()

    now = datetime.now().isoformat()
    correct_inc = 1 if is_correct else 0

    if row:
        new_correct = row[0] + correct_inc
        new_total = row[1] + 1
        c.execute(
            "UPDATE progress SET correct = ?, total = ?, last_seen = ? WHERE topic = ?",
            (new_correct, new_total, now, topic),
        )
    else:
        c.execute(
            "INSERT INTO progress (topic, correct, total, last_seen) VALUES (?, ?, ?, ?)",
            (topic, correct_inc, 1, now),
        )
    conn.commit()


def get_weak_topics(conn, limit=3):
    """Получить темы с худшим результатом (< 60% успеха)"""
    c = conn.cursor()
    c.execute(
        """
        SELECT topic, correct, total FROM progress 
        WHERE total > 0 AND (CAST(correct AS FLOAT) / total) < 0.6
        ORDER BY (CAST(correct AS FLOAT) / total) ASC
        LIMIT ?
    """,
        (limit,),
    )

    rows = c.fetchall()
    return [
        {
            "topic": r[0],
            "correct": r[1],
            "total": r[2],
            "rate": int(r[1] / r[2] * 100) if r[2] > 0 else 0,
        }
        for r in rows
    ]


# === КЭШИРОВАНИЕ LLM ОТВЕТОВ (SQLite + TTL) ===


def cleanup_expired_cache(conn):
    """Удалить просроченные записи кэша"""
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute(
        "DELETE FROM query_cache WHERE expires_at IS NOT NULL AND expires_at < ?",
        (now,),
    )
    conn.commit()


def get_cached_response(conn, query_hash: str):
    """Получить ответ из кэша если не просрочен"""
    c = conn.cursor()
    c.execute(
        "SELECT response, expires_at FROM query_cache WHERE query_hash = ?",
        (query_hash,),
    )
    row = c.fetchone()
    if row:
        response, expires_at = row
        if expires_at is None or expires_at > datetime.now().isoformat():
            return response
        # Просрочен — удаляем
        c.execute("DELETE FROM query_cache WHERE query_hash = ?", (query_hash,))
        conn.commit()
    return None


def cache_response(conn, query_hash: str, response: str, ttl_seconds: int = None):
    """Сохранить ответ в кэш с TTL"""
    c = conn.cursor()
    created_at = datetime.now().isoformat()
    expires_at = None
    if ttl_seconds:
        from datetime import timedelta

        expires = datetime.now() + timedelta(seconds=ttl_seconds)
        expires_at = expires.isoformat()

    c.execute(
        """
        INSERT OR REPLACE INTO query_cache (query_hash, response, created_at, expires_at, ttl_seconds)
        VALUES (?, ?, ?, ?, ?)
    """,
        (query_hash, response, created_at, expires_at, ttl_seconds),
    )
    conn.commit()


def get_cache_stats(conn):
    """Статистика кэша"""
    c = conn.cursor()
    c.execute("SELECT count(*) FROM query_cache")
    total = c.fetchone()[0]
    c.execute(
        "SELECT count(*) FROM query_cache WHERE expires_at IS NULL OR expires_at > ?",
        (datetime.now().isoformat(),),
    )
    valid = c.fetchone()[0]
    return {"total": total, "valid": valid, "expired": total - valid}
