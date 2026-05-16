"""REST API для отслеживания прогресса (L-16).

FastAPI сервер для внешнего мониторинга и интеграции с LMS.

Endpoints:
    GET  /api/health       — Статус сервера
    GET  /api/progress     — Прогресс пользователя
    GET  /api/stats        — Статистика
    GET  /api/achievements — Достижения
    GET  /api/weak-topics  — Слабые темы
    POST /api/quiz/result  — Отправить результат квиза
"""

import json
import os
from datetime import datetime
from typing import Any, Dict

from state import get_state

# FastAPI опционален
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

app = FastAPI(title="CyberTeacher API", version="1.0") if FASTAPI_AVAILABLE else None


class QuizResult(BaseModel):
    topic: str
    score: float
    total: int


@app.get("/api/health")
def health_check():
    """Проверка статуса API."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/progress")
def get_progress():
    """Получить прогресс пользователя."""
    state = get_state()
    return {
        "xp": getattr(state, "xp", 0),
        "level": getattr(state, "level", 1),
        "reputation": getattr(state, "reputation", 0),
        "current_course": getattr(state, "current_course", None),
        "current_topic": getattr(state, "current_topic", None),
        "streak": getattr(state, "daily_streak", 0),
    }


@app.get("/api/stats")
def get_stats():
    """Получить статистику."""
    state = get_state()
    return {
        "completed_quizzes": getattr(state, "completed_quizzes", []),
        "completed_tasks": getattr(state, "completed_tasks", []),
        "total_quizzes": len(getattr(state, "completed_quizzes", [])),
        "total_tasks": len(getattr(state, "completed_tasks", [])),
    }


@app.get("/api/achievements")
def get_achievements():
    """Получить достижения."""
    state = get_state()
    return {"achievements": getattr(state, "achievements", [])}


@app.get("/api/weak-topics")
def get_weak_topics():
    """Получить слабые темы."""
    state = get_state()
    return {"weak_topics": getattr(state, "weak_topics", [])}


@app.post("/api/quiz/result")
def submit_quiz_result(result: QuizResult):
    """Отправить результат квиза."""
    state = get_state()
    if result.score / result.total < 0.6:
        weak_topics = getattr(state, "weak_topics", [])
        if result.topic not in weak_topics:
            weak_topics.append(result.topic)
            state.weak_topics = weak_topics
    return {"status": "recorded", "topic": result.topic, "score": result.score}


def start_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Запустить API сервер."""
    if not FASTAPI_AVAILABLE:
        print("[API] FastAPI не установлен. Установите: pip install fastapi uvicorn")
        return False

    import uvicorn
    print(f"[API] Запуск сервера на {host}:{port}")
    print(f"[API] Документация: http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port, log_level="info")
    return True
