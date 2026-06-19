"""
🗄️ Database abstraction layer — SQLite / PostgreSQL
Поддерживает оба бэкенда через SQLAlchemy.
"""

import os
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
    create_engine,
    event,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Поддержка обоих переменных: DATABASE_URL (новый) и DB_FILE (старый)
_db_url = os.getenv("DATABASE_URL")
if not _db_url:
    _db_file = os.getenv("DB_FILE", "./memory/chat_history.db")
    _db_url = f"sqlite:///{_db_file}"

DB_URL = _db_url

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Новый стиль Base
class Base(DeclarativeBase):
    pass


# === SQLite-specific tweaks ===
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in DB_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# === Helper ===
def _utc_now_naive():
    """Текущее время UTC без timezone info (для совместимости с SQLite)"""
    return datetime.now(UTC).replace(tzinfo=None)


# === Models ===


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_timestamp", "timestamp"),
        Index("ix_messages_role", "role"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=_utc_now_naive)
    mode = Column(String(30), default="teacher")


class Stat(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    points = Column(Integer, default=0)
    quizzes_passed = Column(Integer, default=0)
    tasks_solved = Column(Integer, default=0)
    last_activity = Column(DateTime, default=_utc_now_naive)


class TopicProgress(Base):
    __tablename__ = "progress"
    topic = Column(String(200), primary_key=True)
    correct = Column(Integer, default=0)
    total = Column(Integer, default=0)
    last_seen = Column(DateTime, default=_utc_now_naive)


class QueryCache(Base):
    __tablename__ = "query_cache"
    query_hash = Column(String(64), primary_key=True)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_utc_now_naive)
    expires_at = Column(DateTime, nullable=True)
    ttl_seconds = Column(Integer, nullable=True)


class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    achievement_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    earned = Column(Boolean, default=False)
    earned_at = Column(DateTime, nullable=True)
    xp_reward = Column(Integer, default=0)


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=0)
    last_practice = Column(DateTime, nullable=True)


class Flag(Base):
    __tablename__ = "flags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    flag_value = Column(String(200), unique=True, nullable=False)
    category = Column(String(50), nullable=True)
    difficulty = Column(String(20), nullable=True)
    captured = Column(Boolean, default=False)
    captured_at = Column(DateTime, nullable=True)


class Writeup(Base):
    __tablename__ = "writeups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_utc_now_naive)
    tags = Column(JSON, nullable=True)


class DailyChallenge(Base):
    __tablename__ = "daily_challenges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), unique=True, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)


class ExploitLog(Base):
    __tablename__ = "exploit_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_id = Column(String(20), nullable=True)
    target = Column(String(200), nullable=True)
    success = Column(Boolean, default=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=_utc_now_naive)


class PurchaseHistory(Base):
    __tablename__ = "purchase_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String(50), nullable=False)
    item_name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    purchased_at = Column(DateTime, default=_utc_now_naive)


class CommandHeatmap(Base):
    __tablename__ = "command_heatmap"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10), nullable=False)
    command = Column(String(50), nullable=False)
    count = Column(Integer, default=0)


class ReviewSchedule(Base):
    __tablename__ = "review_schedule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(200), nullable=False)
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0)
    repetitions = Column(Integer, default=0)
    next_review = Column(DateTime, nullable=False)
    last_review = Column(DateTime, nullable=True)


class SessionSummary(Base):
    __tablename__ = "session_summaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    xp_earned = Column(Integer, default=0)
    quizzes_taken = Column(Integer, default=0)
    labs_started = Column(Integer, default=0)
    commands_used = Column(JSON, nullable=True)


class AppStateRecord(Base):
    """Единая запись состояния приложения для БД (DATA-01)."""

    __tablename__ = "app_state"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), default="default", nullable=False, index=True)
    state_data = Column(JSON, nullable=False)
    version = Column(Integer, default=1)
    updated_at = Column(DateTime, default=_utc_now_naive, onupdate=_utc_now_naive)
    created_at = Column(DateTime, default=_utc_now_naive)


# === Helper functions ===


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    _ensure_default_stats()


def _ensure_default_stats():
    db = SessionLocal()
    try:
        if db.query(Stat).first() is None:
            db.add(Stat(points=0, last_activity=_utc_now_naive()))
            db.commit()
    finally:
        db.close()


def get_session():
    return SessionLocal()


# === AppState persistence (DATA-01) ===


def save_app_state(state_data: dict, user_id: str = "default") -> None:
    """Сохранить состояние приложения в БД."""
    db = SessionLocal()
    try:
        record = db.query(AppStateRecord).filter_by(user_id=user_id).first()
        if record:
            record.state_data = state_data  # type: ignore[assignment]
            record.updated_at = _utc_now_naive()
            record.version += 1  # type: ignore[assignment]
        else:
            record = AppStateRecord(
                user_id=user_id,
                state_data=state_data,
                version=1,
                created_at=_utc_now_naive(),
                updated_at=_utc_now_naive(),
            )
            db.add(record)
        db.commit()
    finally:
        db.close()


def load_app_state(user_id: str = "default") -> dict | None:
    """Загрузить состояние приложения из БД."""
    db = SessionLocal()
    try:
        record = db.query(AppStateRecord).filter_by(user_id=user_id).first()
        if record:
            result: dict | None = record.state_data  # type: ignore[assignment]
            return result
        return None
    finally:
        db.close()


def migrate_json_to_db(json_path: str, user_id: str = "default") -> bool:
    """Мигрировать состояние из JSON-файла в БД."""
    import json

    if not os.path.exists(json_path):
        return False
    with open(json_path, "r", encoding="utf-8") as f:
        state_data = json.load(f)
    save_app_state(state_data, user_id)
    return True
