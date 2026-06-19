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

import asyncio
import contextlib
import json
import logging
import time
import os
import signal
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from state import get_state

# API logger with 7-day rotation
try:
    from logging_config import setup_logging

    setup_logging()
except ImportError:
    pass

api_log = logging.getLogger("cyberteacher.api")

# Глобальная переменная для хранения PID сервера
_server_process: Optional[subprocess.Popen] = None

# FastAPI опционален
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel

    FASTAPI_AVAILABLE = True
except ImportError:
    FastAPI = None  # type: ignore[misc,assignment]
    HTTPException = Exception  # type: ignore[misc,assignment]
    FileResponse = None  # type: ignore[misc,assignment]
    StaticFiles = None  # type: ignore[misc,assignment]
    BaseModel = object  # type: ignore[misc,assignment]
    FASTAPI_AVAILABLE = False

app: Optional[FastAPI] = (
    FastAPI(title="CyberTeacher API", version="1.0") if FASTAPI_AVAILABLE else None
)

# CORS middleware для веб-фронта (raw ASGI — не блокирует WebSocket)
if FASTAPI_AVAILABLE and app is not None:
    _cors_origins = os.getenv(
        "CORS_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000"
    ).split(",")

    class _CORSMiddleware:
        """Simple CORS that skips WebSocket connections."""

        def __init__(self, app: Any, origins: list) -> None:
            self.app = app
            self.origins = origins

        async def __call__(self, scope: Any, receive: Any, send: Any) -> Any:
            if scope.get("type") != "http":
                return await self.app(scope, receive, send)
            from starlette.datastructures import Headers

            headers = Headers(scope=scope)
            origin = headers.get("origin", "")
            is_cors = origin != ""
            response_headers = {}
            if is_cors and origin in self.origins:
                response_headers["access-control-allow-origin"] = origin
                response_headers["access-control-allow-credentials"] = "true"
                response_headers["access-control-allow-methods"] = "GET, POST, OPTIONS"
                response_headers["access-control-allow-headers"] = "*"
            if scope.get("method") == "OPTIONS":
                from starlette.responses import Response

                resp = Response("", status_code=204, headers=response_headers)
                return await resp(scope, receive, send)

            async def send_wrapper(message: Any) -> None:
                if message.get("type") == "http.response.start" and is_cors:
                    existing = dict(message.get("headers", []))
                    for k, v in response_headers.items():
                        existing[k.encode()] = v.encode()
                    message["headers"] = list(existing.items())
                await send(message)

            return await self.app(scope, receive, send_wrapper)

    app.add_middleware(_CORSMiddleware, origins=_cors_origins)

    # Security headers + cache-control middleware (raw ASGI — no WebSocket blocking)
    class _NoCacheMiddleware:
        def __init__(self, app: Any) -> None:
            self.app = app

        async def __call__(self, scope: Any, receive: Any, send: Any) -> Any:
            if scope.get("type") != "http":
                return await self.app(scope, receive, send)

            async def send_wrapper(message: Any) -> None:
                if message.get("type") == "http.response.start":
                    headers = dict(message.get("headers", []))
                    path = scope.get("path", "")

                    headers[b"x-content-type-options"] = b"nosniff"
                    headers[b"x-frame-options"] = b"DENY"
                    headers[b"x-xss-protection"] = b"1; mode=block"
                    headers[b"referrer-policy"] = b"strict-origin-when-cross-origin"
                    headers[b"permissions-policy"] = (
                        b"camera=(), microphone=(), geolocation=()"
                    )
                    headers[b"strict-transport-security"] = (
                        b"max-age=31536000; includeSubDomains"
                    )
                    headers[b"content-security-policy"] = (
                        b"default-src 'self'; "
                        b"script-src 'self' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                        b"style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                        b"font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
                        b"img-src 'self' data:; "
                        b"connect-src 'self' ws: wss:; "
                        b"frame-ancestors 'none'"
                    )

                    if (
                        path.endswith(".js")
                        or path.endswith(".css")
                        or path == "/sw.js"
                    ):
                        headers[b"cache-control"] = (
                            b"no-cache, no-store, must-revalidate"
                        )
                        headers.pop(b"etag", None)
                        headers.pop(b"last-modified", None)

                    message["headers"] = list(headers.items())
                await send(message)

            return await self.app(scope, receive, send_wrapper)

    app.add_middleware(_NoCacheMiddleware)

    # Legacy API path redirect middleware (skip WebSockets)
    _LEGACY_API_MAP = {
        "/get_progress": "/api/progress",
        "/get_modes": "/api/modes",
        "/get_courses": "/api/courses",
        "/get_labs": "/api/labs",
        "/get_profile": "/api/profile",
        "/get_daily_challenge": "/api/daily",
        "/get_achievements_list": "/api/achievements/list",
        "/get_skills": "/api/skills",
        "/get_shop": "/api/shop",
        "/get_story_episodes": "/api/story",
        "/get_tracks": "/api/tracks",
        "/get_ctf_status": "/api/ctf/status",
        "/get_config": "/api/config",
        "/get_world": "/api/world",
        "/get_episodes": "/api/episodes",
        "/get_cyberpsychosis": "/api/cyberpsychosis",
        "/get_detailed_stats": "/api/stats",
        "/get_heatmap": "/api/heatmap",
        "/get_threats": "/api/threats",
        "/get_news": "/api/news",
        "/get_history": "/api/history",
        "/get_scan_rules": "/api/scan/rules",
        "/get_versus_scenarios": "/api/versus/scenarios",
        "/get_versus_status": "/api/versus/status",
        "/chat_with_llm": "/api/chat",
        "/docker_containers": "/api/docker/containers",
        "/docker_status": "/api/docker/status",
        "/docker_start_lab": "/api/docker/start",
        "/docker_stop_lab": "/api/docker/stop",
        "/start_lab": "/api/labs/start",
        "/stop_lab": "/api/labs/stop",
        "/generate_quiz": "/api/quiz/generate",
        "/submit_quiz_result": "/api/quiz/result",
        "/list_users": "/api/users",
        "/set_role": "/api/users/role",
        "/create_course": "/api/courses/create",
        "/verify_auth": "/api/auth/verify",
        "/login": "/api/auth/login",
        "/register": "/api/auth/register",
        "/set_mode": "/api/modes/set",
        "/select_course": "/api/courses/select",
        "/submit_daily_challenge": "/api/daily/submit",
        "/purchase_item": "/api/shop/purchase",
        "/scan_code": "/api/scan",
        "/start_versus": "/api/versus/start",
        "/versus_move": "/api/versus/move",
        "/start_story_episode": "/api/story/start",
        "/start_track": "/api/tracks/start",
        "/submit_flag": "/api/ctf/flag",
        "/submit_mission_flag": "/api/missions/submit",
        "/get_history_eras": "/api/history/eras",
        "/study_history_era": "/api/history/study",
        "/analyze_malware": "/api/malware",
        "/export_user_data": "/api/gdpr/export",
        "/import_user_data": "/api/gdpr/import",
    }

    class _LegacyRedirectMiddleware:
        def __init__(self, app: Any) -> None:
            self.app = app

        async def __call__(self, scope: Any, receive: Any, send: Any) -> Any:
            if scope.get("type") != "http":
                return await self.app(scope, receive, send)
            path = scope.get("path", "")
            if path in _LEGACY_API_MAP:
                from starlette.responses import RedirectResponse as _RR

                qs = scope.get("query_string", b"").decode()
                new_path = _LEGACY_API_MAP[path]
                url = new_path + (f"?{qs}" if qs else "")
                resp = _RR(url=url, status_code=307)
                return await resp(scope, receive, send)
            return await self.app(scope, receive, send)

    app.add_middleware(_LegacyRedirectMiddleware)

# Раздача статики (PWA)
if FASTAPI_AVAILABLE and app is not None and os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Mount subdirectories so /css/*, /js/* resolve correctly
    if os.path.isdir("static/css"):
        app.mount("/css", StaticFiles(directory="static/css"), name="css")
    if os.path.isdir("static/js"):
        app.mount("/js", StaticFiles(directory="static/js"), name="js")

    @app.get("/")
    def read_root() -> FileResponse:
        return FileResponse(
            "static/index.html",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )

    @app.get("/index.html")
    def read_index() -> FileResponse:
        return FileResponse(
            "static/index.html",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )

    @app.get("/manifest.json")
    def read_manifest() -> FileResponse:
        return FileResponse(
            "static/manifest.json",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )

    @app.get("/sw.js")
    def read_sw() -> FileResponse:
        return FileResponse(
            "static/sw.js",
            media_type="application/javascript",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )

    @app.get("/favicon.ico")
    def read_favicon() -> FileResponse:
        return FileResponse("static/icon-192.png", media_type="image/png")

    @app.get("/icon-192.png")
    def read_icon_192() -> FileResponse:
        return FileResponse("static/icon-192.png", media_type="image/png")

    @app.get("/icon-512.png")
    def read_icon_512() -> FileResponse:
        return FileResponse("static/icon-512.png", media_type="image/png")


class QuizResult(BaseModel):
    topic: str
    score: float
    total: int


class ChatRequest(BaseModel):
    message: str
    history: list = []


class QuizGenerateRequest(BaseModel):
    topic: str = "general"
    count: int = 5


class PhishingGenerateRequest(BaseModel):
    template_type: str = ""


class SandboxRunRequest(BaseModel):
    code: str
    language: str = "python"
    timeout: int = 10


class DockerGenRequest(BaseModel):
    labs: list[str] = []


# ----------------------------------------------------------------------
# Rate Limiter (in-memory, sliding window)
# ----------------------------------------------------------------------
class _RateLimiter:
    """Simple in-memory sliding-window rate limiter."""

    def __init__(self) -> None:
        self._hits: Dict[str, List[float]] = {}

    def is_limited(self, key: str, max_requests: int, window: int) -> bool:
        now = time.time()
        if key not in self._hits:
            self._hits[key] = []
        self._hits[key] = [t for t in self._hits[key] if now - t < window]
        if len(self._hits[key]) >= max_requests:
            return True
        self._hits[key].append(now)
        return False


_rate_limiter = _RateLimiter()


# ----------------------------------------------------------------------
# Context Budget Manager (global for API endpoints)
# ----------------------------------------------------------------------
try:
    from context_budget import ContextBudgetManager as _CBM

    api_budget_manager = _CBM(max_tokens=8000)
    BUDGET_AVAILABLE = True
except ImportError:
    api_budget_manager = None  # type: ignore[assignment]
    BUDGET_AVAILABLE = False


# ----------------------------------------------------------------------
# Вспомогательная функция для декорирования, если app не None
# ----------------------------------------------------------------------
def _if_app(method: str, path: str):
    def decorator(func):
        if app is not None:
            return getattr(app, method)(path)(func)
        return func

    return decorator


# Register extracted route modules
if FASTAPI_AVAILABLE and app is not None:
    from routes.story import register_story_routes
    from routes.risk import register_risk_routes
    from routes.faction import register_faction_routes
    from routes.phantom import register_phantom_routes
    from routes.rewind import register_rewind_routes

    register_story_routes(app, _if_app, HTTPException, get_state)
    register_risk_routes(app, _if_app, HTTPException, get_state)
    register_faction_routes(app, _if_app, HTTPException, get_state)
    register_phantom_routes(app, _if_app, HTTPException, get_state)
    register_rewind_routes(app, _if_app, HTTPException, get_state)


# ----------------------------------------------------------------------
# API endpoints (все с проверкой app)
# ----------------------------------------------------------------------
@_if_app("get", "/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@_if_app("get", "/api/doctor")
def doctor_status():
    """Return LLM provider status and system info."""
    try:
        from handlers.doctor import get_doctor_status

        return get_doctor_status()
    except Exception as e:
        return {"current_provider": "unknown", "error": str(e), "providers": []}


@_if_app("get", "/api/offline")
def get_offline_status():
    state = get_state()
    return {"offline_mode": state.offline_mode}


@_if_app("post", "/api/offline")
def set_offline_status(action: str = "toggle"):
    state = get_state()
    if action == "on":
        state.offline_mode = True
    elif action == "off":
        state.offline_mode = False
    else:
        state.offline_mode = not state.offline_mode
    return {"offline_mode": state.offline_mode, "action": action}


@_if_app("get", "/api/progress")
def get_progress():
    state = get_state()
    return {
        "xp": getattr(state, "xp", 0),
        "level": getattr(state, "level", 1),
        "reputation": getattr(state, "reputation", 0),
        "current_course": getattr(state, "current_course", None),
        "current_topic": getattr(state, "current_topic", None),
        "streak": getattr(state, "daily_streak", 0),
    }


@_if_app("get", "/api/achievements")
def get_achievements():
    state = get_state()
    return {"achievements": getattr(state, "achievements", [])}


@_if_app("get", "/api/weak-topics")
def get_weak_topics():
    state = get_state()
    return {"weak_topics": getattr(state, "weak_topics", [])}


# ----------------------------------------------------------------------
# Курсы (импортируем COURSES из courses)
# ----------------------------------------------------------------------
@_if_app("get", "/api/courses")
def get_courses():
    try:
        from courses import COURSES

        state = get_state()
        courses_list = []
        for cid, course in COURSES.items():
            total_topics = len(course.get("topics", []))
            progress = 0
            if total_topics > 0:
                current_topic_idx = state.course_progress.get(cid, 0)
                progress = int((current_topic_idx / total_topics) * 100)
            topics_data = []
            for t in course.get("topics", []):
                if hasattr(t, "__dataclass_fields__"):
                    topics_data.append(
                        {
                            "id": t.name.lower().replace(" ", "-"),
                            "name": t.name,
                            "description": t.description,
                            "labs": t.labs if hasattr(t, "labs") else [],
                            "quiz_topics": t.quiz_topics
                            if hasattr(t, "quiz_topics")
                            else [],
                        }
                    )
                elif isinstance(t, dict):
                    topics_data.append(
                        {
                            "id": t.get(
                                "id", t.get("name", "").lower().replace(" ", "-")
                            ),
                            "name": t.get("name", ""),
                            "description": t.get("description", ""),
                            "labs": t.get("labs", []),
                            "quiz_topics": t.get("quiz_topics", []),
                        }
                    )
            courses_list.append(
                {
                    "id": cid,
                    "name": course.get("name", ""),
                    "description": course.get("desc", ""),
                    "icon": course.get("icon", "📚"),
                    "topics_count": total_topics,
                    "topics": topics_data,
                    "duration": f"{total_topics} тем",
                    "level": course.get("level", "beginner"),
                    "progress": progress,
                    "active": state.current_course == cid,
                }
            )
        return {"courses": courses_list}
    except Exception as e:
        return {"courses": [], "error": "Internal error"}


@_if_app("post", "/api/courses/{course_id}/select")
@_if_app("post", "/api/courses/select")
def select_course(course_id: str = "", token: str = ""):
    try:
        from courses import COURSES

        if course_id not in COURSES:
            raise HTTPException(status_code=404, detail="Course not found")
        state = get_state()
        state.current_course = course_id
        state.current_topic = 0
        state.save_to_file()
        return {"status": "selected", "course": course_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("post", "/api/quiz/result")
def submit_quiz_result(result: QuizResult):
    state = get_state()
    if result.score / result.total < 0.6:
        weak_topics = getattr(state, "weak_topics", [])
        if result.topic not in weak_topics:
            weak_topics.append(result.topic)
            state.weak_topics = weak_topics
    try:
        from handlers.skills import guess_skill_from_topic

        skill = guess_skill_from_topic(result.topic)
        if skill:
            success = result.score / result.total >= 0.6
            state.track_skill(skill, success, xp=result.score)
    except (ValueError, RuntimeError):
        pass
    return {"status": "recorded", "topic": result.topic, "score": result.score}


@_if_app("post", "/api/chat")
def chat_with_llm(req: ChatRequest):
    try:
        from config import LazyLoader
        from handlers.mood import get_mood_prompt_modifier
        from pedagogy import TeacherPersona
        from courses import COURSES

        llm = LazyLoader.get_llm()
        if llm is None:
            raise RuntimeError("LLM не загружен")

        state = get_state()
        language = getattr(state, "language", "ru")
        mode = getattr(state, "current_mode", "hybrid")

        # Secret phrase detection
        try:
            from secret_language import detect_secret_phrase
            secret = detect_secret_phrase(req.message)
            if secret:
                # Apply effect and return special response
                if secret["effect"] == "hint":
                    state.hint_credits = min(10, state.hint_credits + 1)
                elif secret["effect"] == "mood_serious":
                    state.current_mood = "serious"
                elif secret["effect"] == "unlock_ghost_log":
                    pass  # Ghost log unlock is informational
                return {
                    "response": f"🔐 **Секретная фраза:** {secret['phrase']}\n\n{secret['response']}",
                    "history": [*req.history, {"role": "user", "content": req.message}, {"role": "assistant", "content": secret["response"]}],
                    "secret_phrase": secret,
                }
        except ImportError:
            pass

        system_prompt = TeacherPersona.get_system_prompt(
            style=mode,
            language=language,
        )

        mood_modifier = get_mood_prompt_modifier()
        if mood_modifier:
            system_prompt += f"\n\nStyle: {mood_modifier}"

        # Behavioral archetype
        try:
            from behavior_profile import get_archetype_prompt_modifier

            archetype_mod = get_archetype_prompt_modifier(state)
            if archetype_mod:
                system_prompt += archetype_mod
        except ImportError:
            pass

        # Persona Router (dynamic)
        try:
            from persona_router import (
                select_persona,
                get_persona_prompt,
                get_persona_info,
            )

            persona_id = select_persona(state, req.message)
            persona_mod = get_persona_prompt(persona_id)
            if persona_mod:
                system_prompt += persona_mod
        except ImportError:
            pass

        # Inject user statistics for context awareness
        study_context = (
            f"\n\n---\nДАННЫЕ УЧЕНИКА:\n"
            f"XP: {getattr(state, 'xp', 0)}, "
            f"Level: {getattr(state, 'level', 1)}, "
            f"Streak: {getattr(state, 'daily_streak', 0)} дн.\n"
            f"Текущий курс: {getattr(state, 'current_course', 'не выбран')}\n"
            f"Слабые темы: {', '.join(getattr(state, 'weak_topics', [])[-5:]) or 'нет'}\n"
            f"---"
        )
        system_prompt += study_context

        # Inject RAG from knowledge base
        try:
            from knowledge import get_relevant_docs

            vectordb = getattr(state, "_vectordb", None)
            if vectordb is None:
                from knowledge import load_knowledge_base

                vectordb = load_knowledge_base()
                state._vectordb = vectordb
            if vectordb:
                docs = (
                    get_relevant_docs(vectordb, req.message, top_k=3)
                    if hasattr(vectordb, "similarity_search")
                    else []
                )
                if docs:
                    docs_context = "\n📖 База знаний:\n" + "\n".join(
                        [f"- {d.page_content[:500]}" for d in docs]
                    )
                    system_prompt += docs_context
        except (ValueError, RuntimeError):
            pass

        messages = [{"role": "system", "content": system_prompt}]

        # Inject summary if available
        if BUDGET_AVAILABLE and api_budget_manager is not None:
            summary = api_budget_manager.extract_summary(req.history)
            if summary:
                messages.append(
                    {"role": "system", "content": f"[Context summary: {summary}]"}
                )

            trimmed, _ = api_budget_manager.prepare_context(
                req.history, max_messages=30, user_input=req.message
            )
            history_slice = trimmed
        else:
            history_slice = req.history[-10:]
        for msg in history_slice:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": req.message})

        response = llm.invoke(messages)
        response_text = (
            response.content if hasattr(response, "content") else str(response)
        )

        # Narrative events
        try:
            from handlers.event_engine import check_events

            fired = check_events()
            if fired:
                event_lines = []
                for evt in fired:
                    msg = f"⚡ {evt['title']}: {evt['message']}"
                    if evt["effects"]:
                        msg += f" ({', '.join(evt['effects'])})"
                    event_lines.append(msg)
                response_text += "\n\n" + "\n".join(event_lines)
        except ImportError:
            pass

        # Persona info for PWA
        try:
            from persona_router import get_persona_info

            persona_info = get_persona_info(persona_id)
        except ImportError:
            persona_info = {"id": "rick", "name": "Rick", "emoji": "🧪"}

        new_history = [
            *req.history,
            {"role": "user", "content": req.message},
            {"role": "assistant", "content": response_text},
        ]

        return {
            "response": response_text,
            "history": new_history,
            "persona": persona_info,
        }
    except (ValueError, RuntimeError, KeyError, OSError):
        import logging

        logging.exception("[API Chat Error]")
        raise HTTPException(status_code=500, detail="LLM error")


# Hardcoded fallback quiz questions (LLM-free game mechanic)
_FALLBACK_QUESTIONS = {
    "general": [
        {
            "question": "Что такое фишинг?",
            "options": [
                "Вид рыбалки",
                "Атака с подделкой писем/сайтов",
                "Тип шифрования",
                "Сетевой протокол",
            ],
            "correct": 1,
            "explanation": "Фишинг — вид социальной инженерии, где злоумышленник подделывает письма/сайты.",
        },
        {
            "question": "Что такое zero-day уязвимость?",
            "options": [
                "Уязвимость нулевого дня",
                "Уязвимость без патча",
                "Неизвестная разработчику уязвимость",
                "Всё вышеперечисленное",
            ],
            "correct": 3,
            "explanation": "Zero-day — уязвимость, о которой разработчик не знает, и патча ещё нет.",
        },
        {
            "question": "Что означает CIA Triad?",
            "options": [
                "Confidentiality, Integrity, Availability",
                "Code, Internet, Access",
                "Central Intelligence Agency",
                "Cryptography, Identity, Authentication",
            ],
            "correct": 0,
            "explanation": "Триада CIA — конфиденциальность, целостность, доступность.",
        },
        {
            "question": "Какой порт использует HTTP?",
            "options": ["443", "80", "22", "8080"],
            "correct": 1,
            "explanation": "HTTP по умолчанию использует порт 80.",
        },
        {
            "question": "Что такое ботнет?",
            "options": [
                "Сеть ботов",
                "Тип вируса",
                "Сеть заражённых устройств под контролем атакующего",
                "Антивирусная программа",
            ],
            "correct": 2,
            "explanation": "Ботнет — сеть заражённых устройств, управляемая злоумышленником.",
        },
    ],
    "networking": [
        {
            "question": "Какой порт использует SSH?",
            "options": ["22", "23", "443", "3389"],
            "correct": 0,
            "explanation": "SSH использует порт 22 для безопасного удалённого доступа.",
        },
        {
            "question": "Что такое DNS?",
            "options": [
                "Система доменных имён",
                "Протокол шифрования",
                "Межсетевой экран",
                "Тип атаки",
            ],
            "correct": 0,
            "explanation": "DNS преобразует доменные имена в IP-адреса.",
        },
        {
            "question": "Какой протокол используется для безопасной веб-передачи?",
            "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
            "correct": 2,
            "explanation": "HTTPS — HTTP поверх SSL/TLS, обеспечивает шифрование.",
        },
        {
            "question": "Что такое NAT?",
            "options": [
                "Трансляция сетевых адресов",
                "Протокол маршрутизации",
                "Тип межсетевого экрана",
                "Алгоритм шифрования",
            ],
            "correct": 0,
            "explanation": "NAT подменяет частные IP-адреса на публичный.",
        },
        {
            "question": "Какой порт использует DNS?",
            "options": ["53", "80", "443", "25"],
            "correct": 0,
            "explanation": "DNS работает на порту 53.",
        },
    ],
    "web": [
        {
            "question": "Что такое XSS?",
            "options": [
                "Cross-Site Scripting",
                "Extra Secure System",
                "XML Style Sheet",
                "Cross-Site Request",
            ],
            "correct": 0,
            "explanation": "XSS — внедрение скриптов на веб-страницу через уязвимость.",
        },
        {
            "question": "Что такое SQL-инъекция?",
            "options": [
                "Внедрение SQL-кода",
                "Тип базы данных",
                "Протокол безопасности",
                "Метод шифрования",
            ],
            "correct": 0,
            "explanation": "SQLi — внедрение вредоносного SQL-кода через пользовательский ввод.",
        },
        {
            "question": "Что такое CSRF?",
            "options": [
                "Cross-Site Request Forgery",
                "Подделка межсайтового запроса",
                "Атака через cookie",
                "Всё вышеперечисленное",
            ],
            "correct": 3,
            "explanation": "CSRF — атака, заставляющая браузер жертвы выполнить нежелательное действие.",
        },
        {
            "question": "Какой заголовок защищает от XSS?",
            "options": [
                "X-XSS-Protection",
                "Content-Security-Policy",
                "X-Content-Type-Options",
                "Все вышеперечисленные",
            ],
            "correct": 3,
            "explanation": "X-XSS-Protection, CSP и X-Content-Type-Options помогают от XSS.",
        },
        {
            "question": "Что такое CORS?",
            "options": [
                "Совместное использование ресурсов между источниками",
                "Протокол шифрования",
                "Тип атаки",
                "Серверная технология",
            ],
            "correct": 0,
            "explanation": "CORS — механизм, разрешающий запросы с других доменов.",
        },
    ],
    "crypto": [
        {
            "question": "Какой алгоритм считается небезопасным для хеширования?",
            "options": ["SHA-256", "MD5", "bcrypt", "Argon2"],
            "correct": 1,
            "explanation": "MD5 устарел и подвержен коллизиям.",
        },
        {
            "question": "Что такое симметричное шифрование?",
            "options": [
                "Один ключ для шифрования и дешифрования",
                "Два разных ключа",
                "Открытый ключ",
                "Хеш-функция",
            ],
            "correct": 0,
            "explanation": "Симметричное шифрование использует один ключ для обеих операций.",
        },
        {
            "question": "Что такое SSL/TLS?",
            "options": [
                "Протокол шифрования канала",
                "Тип сертификата",
                "Алгоритм хеширования",
                "Межсетевой экран",
            ],
            "correct": 0,
            "explanation": "TLS защищает данные при передаче по сети.",
        },
        {
            "question": "Для чего используется цифровая подпись?",
            "options": [
                "Подтверждение авторства",
                "Шифрование данных",
                "Сжатие данных",
                "Аутентификация пользователя",
            ],
            "correct": 0,
            "explanation": "Цифровая подпись подтверждает целостность и авторство.",
        },
        {
            "question": "Что такое AES?",
            "options": [
                "Стандарт шифрования",
                "Протокол аутентификации",
                "Тип атаки",
                "Хеш-функция",
            ],
            "correct": 0,
            "explanation": "AES — Advanced Encryption Standard, симметричное шифрование.",
        },
    ],
    "malware": [
        {
            "question": "Что такое ransomware?",
            "options": [
                "Шифровальщик-вымогатель",
                "Троян удалённого доступа",
                "Сетевой червь",
                "Кейлоггер",
            ],
            "correct": 0,
            "explanation": "Ransomware шифрует файлы и требует выкуп за их расшифровку.",
        },
        {
            "question": "Чем вирус отличается от червя?",
            "options": [
                "Вирусу нужен носитель; червь сам распространяется",
                "Ничем",
                "Червь шифрует файлы",
                "Вирус распространяется по сети",
            ],
            "correct": 0,
            "explanation": "Вирус прикрепляется к файлам; червь автономно распространяется по сети.",
        },
        {
            "question": "Что такое троян?",
            "options": [
                "Вредоносная программа под видом легитимной",
                "Самораспространяющийся вирус",
                "Тип шифровальщика",
                "Программа для взлома",
            ],
            "correct": 0,
            "explanation": "Троян маскируется под полезную программу.",
        },
        {
            "question": "Что такое rootkit?",
            "options": [
                "Набор инструментов для скрытия присутствия в системе",
                "Вирус",
                "Межсетевой экран",
                "Антивирус",
            ],
            "correct": 0,
            "explanation": "Rootkit скрывает активность злоумышленника в системе.",
        },
        {
            "question": "Какой тип анализа малвари использует изолированную среду?",
            "options": [
                "Динамический анализ",
                "Статический анализ",
                "Эвристический анализ",
                "Сигнатурный анализ",
            ],
            "correct": 0,
            "explanation": "Динамический анализ запускает образец в изолированной среде (sandbox).",
        },
    ],
}


@_if_app("post", "/api/quiz/generate")
def generate_quiz(req: QuizGenerateRequest) -> dict[str, Any]:
    try:
        from config import LazyLoader

        llm = LazyLoader.get_llm()

        # If LLM available, try AI-generation first
        if llm is not None:
            topic_map = {
                "general": "общие вопросы кибербезопасности",
                "networking": "сетевая безопасность (порты, протоколы, атаки)",
                "crypto": "криптография (шифрование, хеши, сертификаты)",
                "web": "веб-безопасность (XSS, SQLi, CSRF)",
                "malware": "вредоносное ПО (вирусы, трояны, ransomware)",
            }
            topic_desc = topic_map.get(req.topic, "кибербезопасность")

            prompt = (
                f"Создай {req.count} вопросов с выбором ответа по теме: {topic_desc}. "
                "Формат: JSON массив объектов с полями: question (строка), options (массив из 4 строк), "
                "correct (индекс правильного ответа 0-3), explanation (краткое объяснение). "
                "Только JSON, без markdown."
            )

            response = llm.invoke(prompt)
            response_text = (
                response.content if hasattr(response, "content") else str(response)
            )

            import json
            import re

            json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
            if json_match:
                questions = json.loads(json_match.group())
                return {"questions": questions, "source": "ai"}

        # Fallback: use hardcoded questions (LLM-free)
        topic = req.topic if req.topic in _FALLBACK_QUESTIONS else "general"
        pool = _FALLBACK_QUESTIONS[topic]
        count = min(req.count, len(pool))
        import random

        questions = random.sample(pool, count)
        return {"questions": questions, "source": "local"}
    except HTTPException:
        raise
    except Exception as e:
        # Ultimate fallback: return whatever local questions we have
        topic = req.topic if req.topic in _FALLBACK_QUESTIONS else "general"
        pool = _FALLBACK_QUESTIONS[topic]
        count = min(req.count, len(pool))
        import random

        questions = random.sample(pool, count)
        return {"questions": questions, "source": "local_fallback"}


# ----------------------------------------------------------------------
# Остальные эндпоинты (аналогично, с защитой)
# ----------------------------------------------------------------------
@_if_app("get", "/api/courses-alt")
def get_courses_alt():
    # Дубликат – удаляем, он не нужен, но оставим для совместимости
    return get_courses()


@_if_app("post", "/api/courses-alt/select")
def select_course_alt(course_id: str):
    return select_course(course_id)


@_if_app("get", "/api/labs")
def get_labs():
    try:
        from practice import DOCKER_LABS

        state = get_state()
        running = getattr(state, "running_labs", [])

        result = []
        for lid, lab in DOCKER_LABS.items():
            result.append(
                {
                    "id": lid,
                    "name": lab.get("name", ""),
                    "description": lab.get("desc", ""),
                    "image": lab.get("image", ""),
                    "ports": lab.get("ports", {}),
                    "tags": lab.get("tags", []),
                    "running": lid in running,
                    "difficulty": "beginner"
                    if "beginner" in lab.get("tags", [])
                    else (
                        "intermediate"
                        if "intermediate" in lab.get("tags", [])
                        else "advanced"
                    ),
                }
            )
        return {"labs": result}
    except Exception as e:
        return {"labs": [], "error": "Internal error"}


@_if_app("post", "/api/labs/{lab_id}/start")
@_if_app("post", "/api/labs/start")
def start_lab(lab_id: str = "", token: str = ""):
    if not lab_id:
        raise HTTPException(status_code=400, detail="lab_id required")
    return docker_start_lab(lab_id)


@_if_app("post", "/api/labs/{lab_id}/stop")
@_if_app("post", "/api/labs/stop")
def stop_lab(lab_id: str = "", token: str = ""):
    return docker_stop_lab(lab_id)


@_if_app("get", "/api/docker/status")
def docker_status():
    try:
        import subprocess

        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        available = result.returncode == 0
        return {
            "available": available,
            "message": "Docker доступен"
            if available
            else "Docker не запущен или не установлен",
        }
    except FileNotFoundError:
        return {"available": False, "message": "Docker не установлен"}
    except Exception as e:
        return {"available": False, "message": str(e)}


@_if_app("post", "/api/docker/start")
def docker_start_lab(lab_id: str):
    try:
        from practice import DOCKER_LABS

        if lab_id not in DOCKER_LABS:
            raise HTTPException(status_code=404, detail="Lab not found")

        lab = DOCKER_LABS[lab_id]
        image = lab.get("image", "")
        if not image:
            raise HTTPException(status_code=400, detail="No Docker image specified")

        import subprocess

        ports = lab.get("ports", {})
        port_args = []
        port_list = []
        for host_port, container_port in ports.items():
            port_args.extend(["-p", f"{host_port}:{container_port}"])
            port_list.append(f"http://localhost:{host_port}")

        cmd = [
            "docker",
            "run",
            "-d",
            "--name",
            f"cyberteacher-{lab_id}",
            *port_args,
            image,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, check=False
        )

        if result.returncode != 0:
            if "already in use" in result.stderr:
                start_cmd = ["docker", "start", f"cyberteacher-{lab_id}"]
                start_result = subprocess.run(
                    start_cmd, capture_output=True, text=True, timeout=30, check=False
                )
                if start_result.returncode == 0:
                    state = get_state()
                    running = getattr(state, "running_labs", [])
                    if lab_id not in running:
                        running.append(lab_id)
                        state.running_labs = running
                    post_start = lab.get("post_start", "")
                    if post_start:
                        try:
                            subprocess.run(
                                [
                                    "docker",
                                    "exec",
                                    f"cyberteacher-{lab_id}",
                                    "/bin/bash",
                                    "-c",
                                    post_start,
                                ],
                                capture_output=True,
                                text=True,
                                timeout=30,
                                check=False,
                            )
                        except (subprocess.TimeoutExpired, OSError):
                            pass
                    return {
                        "status": "ok",
                        "lab": lab_id,
                        "ports": port_list,
                        "message": f"Лаборатория {lab.get('name', lab_id)} перезапущена",
                    }
            raise HTTPException(status_code=500, detail=result.stderr)

        container_id = result.stdout.strip()
        state = get_state()
        running = getattr(state, "running_labs", [])
        if lab_id not in running:
            running.append(lab_id)
            state.running_labs = running

        # Post-start hooks (e.g., MySQL init for DVWA)
        post_start = lab.get("post_start", "")
        if post_start:
            try:
                subprocess.run(
                    [
                        "docker",
                        "exec",
                        f"cyberteacher-{lab_id}",
                        "/bin/bash",
                        "-c",
                        post_start,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
            except (subprocess.TimeoutExpired, OSError):
                pass

        return {
            "status": "ok",
            "lab": lab_id,
            "container_id": container_id[:12],
            "ports": port_list,
            "message": f"Лаборатория {lab.get('name', lab_id)} запущена",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("post", "/api/docker/stop")
def docker_stop_lab(lab_id: str):
    try:
        import subprocess

        cmd = ["docker", "stop", f"cyberteacher-{lab_id}"]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, check=False
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        state = get_state()
        running = getattr(state, "running_labs", [])
        if lab_id in running:
            running.remove(lab_id)
            state.running_labs = running

        return {"status": "ok", "lab": lab_id, "message": "Лаборатория остановлена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("get", "/api/docker/containers")
def docker_containers():
    try:
        import subprocess

        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                "name=cyberteacher-",
                "--format",
                "{{.Names}}\t{{.Status}}\t{{.Ports}}",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        containers = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("\t")
                containers.append(
                    {
                        "name": parts[0] if len(parts) > 0 else "",
                        "status": parts[1] if len(parts) > 1 else "",
                        "ports": parts[2] if len(parts) > 2 else "",
                    }
                )
        return {"containers": containers}
    except Exception as e:
        return {"containers": [], "error": "Internal error"}


@_if_app("get", "/api/achievements/list")
def get_achievements_list():
    try:
        state = get_state()
        earned = getattr(state, "earned_achievements", [])

        all_achievements = [
            {
                "id": "first_quiz",
                "name": "Первый квиз",
                "desc": "Пройди свой первый квиз",
                "icon": "📝",
                "xp": 10,
            },
            {
                "id": "first_lab",
                "name": "Первая лаба",
                "desc": "Запусти свою первую лабораторию",
                "icon": "🐳",
                "xp": 20,
            },
            {
                "id": "streak_7",
                "name": "Неделя подряд",
                "desc": "7 дней стрик",
                "icon": "🔥",
                "xp": 50,
            },
            {
                "id": "streak_30",
                "name": "Месяц подряд",
                "desc": "30 дней стрик",
                "icon": "⭐",
                "xp": 100,
            },
            {
                "id": "xp_1000",
                "name": "Тысячник",
                "desc": "Набери 1000 XP",
                "icon": "💎",
                "xp": 0,
            },
            {
                "id": "all_courses",
                "name": "Полиглот",
                "desc": "Пройди все курсы",
                "icon": "🎓",
                "xp": 200,
            },
            {
                "id": "flag_hunter",
                "name": "Охотник за флагами",
                "desc": "Найди 10 флагов",
                "icon": "🚩",
                "xp": 50,
            },
            {
                "id": "code_reviewer",
                "name": "Ревьюер",
                "desc": "Проверь 5 кодов",
                "icon": "🔍",
                "xp": 30,
            },
        ]

        result = []
        for a in all_achievements:
            result.append({**a, "earned": a["id"] in earned, "earned_date": None})

        return {"achievements": result, "total": len(earned)}
    except Exception as e:
        return {"achievements": [], "error": "Internal error"}


@_if_app("get", "/api/stats")
def get_detailed_stats():
    try:
        state = get_state()
        xp = getattr(state, "xp", 0)
        level = getattr(state, "level", 1)
        streak = getattr(state, "daily_streak", 0)
        completed_quizzes = getattr(state, "completed_quizzes", [])
        completed_tasks = getattr(state, "completed_tasks", [])
        weak_topics = getattr(state, "weak_topics", [])

        xp_needed = level * 100
        xp_progress = (xp % xp_needed) / xp_needed * 100 if xp_needed > 0 else 0

        activity = [
            {"day": "Пн", "value": 3},
            {"day": "Вт", "value": 5},
            {"day": "Ср", "value": 2},
            {"day": "Чт", "value": 7},
            {"day": "Пт", "value": 4},
            {"day": "Сб", "value": 1},
            {"day": "Вс", "value": 0},
        ]

        skills = [
            {
                "name": "Web Security",
                "level": min(100, len(completed_quizzes) * 15 + 10),
            },
            {"name": "Network", "level": min(100, len(completed_tasks) * 20 + 5)},
            {"name": "Cryptography", "level": min(100, 25)},
            {"name": "Reverse Engineering", "level": min(100, 10)},
            {"name": "Malware Analysis", "level": min(100, 15)},
        ]

        return {
            "xp": xp,
            "level": level,
            "xp_needed": xp_needed,
            "xp_progress": round(xp_progress, 1),
            "streak": streak,
            "total_quizzes": len(completed_quizzes),
            "total_tasks": len(completed_tasks),
            "weak_topics": weak_topics[:5],
            "activity": activity,
            "skills": skills,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- Versus Mode Endpoints ---
class VersusStartRequest(BaseModel):
    scenario: str


class VersusMoveRequest(BaseModel):
    message: str


@_if_app("get", "/api/versus/scenarios")
def get_versus_scenarios():
    try:
        from handlers.versus import VERSUS_SCENARIOS

        result = []
        for sid, scenario in VERSUS_SCENARIOS.items():
            result.append(
                {
                    "id": sid,
                    "name": scenario["name"],
                    "description": scenario["description"],
                }
            )
        return {"scenarios": result}
    except Exception as e:
        return {"scenarios": [], "error": "Internal error"}


@_if_app("post", "/api/versus/start")
def start_versus(req: VersusStartRequest):
    try:
        from handlers.versus import VERSUS_SCENARIOS

        state = get_state()

        if req.scenario not in VERSUS_SCENARIOS:
            raise HTTPException(status_code=400, detail="Unknown scenario")

        state.versus_active = True
        state.versus_scenario = req.scenario
        state.versus_attempts = 0
        state.versus_history = []

        scenario = VERSUS_SCENARIOS[req.scenario]
        return {
            "status": "ok",
            "scenario": req.scenario,
            "name": scenario["name"],
            "initial_message": scenario["initial_message"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("post", "/api/versus/move")
def versus_move(req: VersusMoveRequest):
    try:
        from config import LazyLoader
        from handlers.versus import get_versus_system_prompt, increment_versus_attempts

        state = get_state()

        if not getattr(state, "versus_active", False):
            raise HTTPException(status_code=400, detail="No active versus game")

        system_prompt = get_versus_system_prompt()
        if not system_prompt:
            raise HTTPException(status_code=500, detail="Invalid scenario")

        history = getattr(state, "versus_history", [])
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": req.message})

        llm = LazyLoader.get_llm()
        if llm is None:
            raise HTTPException(status_code=500, detail="LLM not available")

        response = llm.invoke(messages)
        response_text = (
            response.content if hasattr(response, "content") else str(response)
        )

        history.append({"role": "user", "content": req.message})
        history.append({"role": "assistant", "content": response_text})
        state.versus_history = history

        increment_versus_attempts()

        return {
            "response": response_text,
            "attempts": getattr(state, "versus_attempts", 0),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("get", "/api/versus/status")
def versus_status():
    try:
        state = get_state()
        return {
            "active": getattr(state, "versus_active", False),
            "scenario": getattr(state, "versus_scenario", None),
            "attempts": getattr(state, "versus_attempts", 0),
            "history_length": len(getattr(state, "versus_history", [])),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("post", "/api/versus/stop")
def stop_versus():
    try:
        state = get_state()
        state.versus_active = False
        state.versus_scenario = None
        state.versus_attempts = 0
        state.versus_history = []
        return {"status": "ok", "message": "Versus game ended"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("post", "/api/scan")
def scan_code(payload: dict):
    try:
        from handlers.code_review_v2 import (
            LANGUAGE_EXTENSIONS,
            _count_owasp,
            _count_severities,
            calculate_ci_exit_code,
            generate_sarif,
            scan_file_secrets,
        )

        code = payload.get("code", "")
        language = payload.get("language", "python")
        options = payload.get("options", {})
        use_semgrep = options.get("use_semgrep", True)
        ci_mode = options.get("ci_mode", False)
        sarif_output = options.get("sarif_output", False)

        if not code:
            raise HTTPException(status_code=400, detail="code is required")

        import tempfile

        ext = next((k for k, v in LANGUAGE_EXTENSIONS.items() if v == language), ".py")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=ext, delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            temp_path = f.name

        try:
            findings = []
            findings.extend(scan_file_secrets(temp_path))

            if use_semgrep:
                from handlers.code_review_v2 import run_semgrep

                findings.extend(run_semgrep(temp_path))

            if language == "python":
                from handlers.code_review_v2 import run_bandit

                findings.extend(run_bandit(temp_path))

            results = {
                "language": language,
                "findings": findings,
                "severity_counts": _count_severities(findings),
                "owasp_summary": _count_owasp(findings),
            }

            if sarif_output:
                return {"status": "ok", "sarif": generate_sarif(results)}

            if ci_mode:
                exit_code = calculate_ci_exit_code(results, fail_on="high")
                results["ci_pass"] = exit_code == 0

            return {"status": "ok", "results": results}
        finally:
            import os

            with contextlib.suppress(Exception):
                os.unlink(temp_path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("get", "/api/scan/rules")
def get_scan_rules():
    try:
        import os
        from handlers.code_review_v2 import OWASP_CATEGORIES, RULES_DIR

        rules = []
        if os.path.isdir(RULES_DIR):
            for fname in os.listdir(RULES_DIR):
                if fname.endswith(".yaml") and fname != "owasp-top10.yaml":
                    rules.append(fname.replace(".yaml", ""))

        return {
            "rules": rules,
            "owasp_categories": OWASP_CATEGORIES,
            "rules_dir": RULES_DIR,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- Modes Endpoints ---
MODES = {
    "teacher": {
        "name": "Учитель",
        "icon": "👨‍🏫",
        "desc": "Объяснения, аналогии, Socratic метод",
    },
    "expert": {"name": "Эксперт", "icon": "🔧", "desc": "Краткие технические ответы"},
    "ctf": {"name": "CTF", "icon": "🚩", "desc": "Флаги, соревнования, риск-трекинг"},
    "review": {
        "name": "Code Review",
        "icon": "🔍",
        "desc": "Анализ кода на уязвимости",
    },
    "hybrid": {"name": "Hybrid", "icon": "🎭", "desc": "Адаптивный стиль обучения"},
    "offline": {"name": "Offline", "icon": "📴", "desc": "Работа без LLM"},
}


@_if_app("get", "/api/modes")
def get_modes():
    state = get_state()
    current_mode = getattr(state, "current_mode", "teacher")
    result = []
    for mid, m in MODES.items():
        result.append({**m, "id": mid, "active": mid == current_mode})
    return {"modes": result, "current": current_mode}


@_if_app("post", "/api/modes/set")
def set_mode(mode_id: str):
    if mode_id not in MODES:
        raise HTTPException(status_code=400, detail=f"Unknown mode: {mode_id}")
    state = get_state()
    state.current_mode = mode_id
    return {"status": "ok", "mode": mode_id, "name": MODES[mode_id]["name"]}


# --- Profile Endpoints ---
class ProfileUpdate(BaseModel):
    name: str = ""
    avatar: str = ""


@_if_app("get", "/api/profile")
def get_profile():
    state = get_state()
    return {
        "name": getattr(state, "username", "Аноним"),
        "avatar": getattr(state, "avatar", ""),
        "xp": getattr(state, "xp", 0),
        "level": getattr(state, "level", 1),
        "streak": getattr(state, "daily_streak", 0),
        "reputation": getattr(state, "reputation", 0),
        "points": getattr(state, "points", 0),
        "flags_captured": getattr(state, "flags_captured", 0),
        "quizzes_taken": len(getattr(state, "completed_quizzes", [])),
        "labs_started": len(getattr(state, "running_labs", [])),
    }


@_if_app("post", "/api/profile/update")
def update_profile(req: ProfileUpdate):
    state = get_state()
    if req.name:
        state.username = req.name
    if req.avatar:
        state.avatar = req.avatar
    return {"status": "ok"}


@_if_app("get", "/api/behavior-profile")
def get_behavior_profile():
    state = get_state()
    try:
        from behavior_profile import get_profile_summary

        return get_profile_summary(state)
    except ImportError:
        return {
            "archetype": {"id": "engineer", "name": "Инженер"},
            "traits": {},
            "total_actions": 0,
        }


# --- Daily Challenge Endpoints ---
DAILY_CHALLENGES = [
    {
        "id": 1,
        "question": "Какой порт использует SSH?",
        "answer": "22",
        "category": "networking",
        "difficulty": "easy",
    },
    {
        "id": 2,
        "question": "Что означает XSS?",
        "answer": "Cross-Site Scripting",
        "category": "web",
        "difficulty": "easy",
    },
    {
        "id": 3,
        "question": "Какой протокол использует порт 443?",
        "answer": "HTTPS",
        "category": "networking",
        "difficulty": "easy",
    },
    {
        "id": 4,
        "question": "Что такое SQL-инъекция?",
        "answer": "Внедрение malicious SQL-кода",
        "category": "web",
        "difficulty": "medium",
    },
    {
        "id": 5,
        "question": "Какой инструмент используется для сканирования портов?",
        "answer": "Nmap",
        "category": "tools",
        "difficulty": "easy",
    },
    {
        "id": 6,
        "question": "Что такое CSRF?",
        "answer": "Cross-Site Request Forgery",
        "category": "web",
        "difficulty": "medium",
    },
    {
        "id": 7,
        "question": "Какой хеш-алгоритм считается небезопасным?",
        "answer": "MD5",
        "category": "crypto",
        "difficulty": "medium",
    },
    {
        "id": 8,
        "question": "Что такое zero-day?",
        "answer": "Уязвимость без патча",
        "category": "general",
        "difficulty": "medium",
    },
    {
        "id": 9,
        "question": "Какой порт использует DNS?",
        "answer": "53",
        "category": "networking",
        "difficulty": "easy",
    },
    {
        "id": 10,
        "question": "Что такое ransomware?",
        "answer": "Шифровальщик",
        "category": "malware",
        "difficulty": "easy",
    },
]


@_if_app("get", "/api/daily")
def get_daily_challenge():
    from datetime import datetime

    state = get_state()
    today = datetime.now().strftime("%Y-%m-%d")
    last_daily = getattr(state, "last_daily_date", "")

    if last_daily != today:
        idx = hash(today) % len(DAILY_CHALLENGES)
        state.last_daily_date = today
        state.last_daily_idx = idx

    idx = getattr(state, "last_daily_idx", 0)
    challenge = DAILY_CHALLENGES[idx % len(DAILY_CHALLENGES)]
    completed = getattr(state, "daily_completed", False)

    return {
        **challenge,
        "completed": completed,
        "date": today,
        "streak": getattr(state, "daily_streak", 0),
    }


@_if_app("post", "/api/daily/submit")
def submit_daily_challenge(answer: str):
    state = get_state()
    idx = getattr(state, "last_daily_idx", 0)
    challenge = DAILY_CHALLENGES[idx % len(DAILY_CHALLENGES)]

    answer_val: str = str(challenge.get("answer", ""))
    correct = answer.strip().lower() == answer_val.lower()

    if correct and not getattr(state, "daily_completed", False):
        state.daily_completed = True
        state.daily_streak = getattr(state, "daily_streak", 0) + 1
        state.xp = getattr(state, "xp", 0) + 50
        state.points = getattr(state, "points", 0) + 50

    return {
        "correct": correct,
        "answer": challenge["answer"],
        "explanation": f"Правильный ответ: {challenge['answer']}",
        "xp_earned": 50 if correct else 0,
    }


# --- Skills API ---
@_if_app("get", "/api/skills")
def get_skills():
    state = get_state()
    skills = getattr(state, "skills", {})
    result = []
    for sid, sdata in skills.items():
        if isinstance(sdata, dict):
            result.append(
                {
                    "id": sid,
                    "name": sdata.get("name", sid),
                    "xp": sdata.get("xp", 0),
                    "level": sdata.get("level", 0),
                }
            )
        else:
            result.append({"id": sid, "xp": sdata, "level": 0})
    return {"skills": result}


# --- Shop API ---
@_if_app("get", "/api/shop")
def get_shop():
    try:
        import json, os as _os

        shop_path = _os.path.join(_os.path.dirname(__file__), "data", "shop_items.json")
        with open(shop_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        items = items.get("items", items) if isinstance(items, dict) else items
        state = get_state()
        rep = getattr(state, "reputation", 0)
        discount = (
            0.1 if rep >= 100 else (0.15 if rep >= 200 else (0.25 if rep >= 500 else 0))
        )
        result = []
        for item in items:
            price = item.get("cost", item.get("price", 0))
            discounted = int(price * (1 - discount))
            result.append(
                {
                    **item,
                    "price": discounted,
                    "original_price": price if discount > 0 else None,
                }
            )
        return {"items": result, "discount": int(discount * 100)}
    except Exception as e:
        return {"items": [], "error": f"Internal: {str(e)[:100]}"}


@_if_app("post", "/api/shop/purchase")
def purchase_item(item_id: str):
    try:
        import json, os as _os

        shop_path = _os.path.join(_os.path.dirname(__file__), "data", "shop_items.json")
        with open(shop_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        items = items.get("items", items) if isinstance(items, dict) else items
        item = next((i for i in items if i["id"] == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        state = get_state()
        points = getattr(state, "points", 0)
        rep = getattr(state, "reputation", 0)
        discount = (
            0.1 if rep >= 100 else (0.15 if rep >= 200 else (0.25 if rep >= 500 else 0))
        )
        price = int(item.get("cost", item.get("price", 0)) * (1 - discount))
        if points < price:
            raise HTTPException(status_code=400, detail="Not enough points")
        state.points = points - price
        return {"status": "ok", "item": item_id, "price": price}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- Heatmap API ---
@_if_app("get", "/api/heatmap")
def get_heatmap():
    state = get_state()
    daily_counts = getattr(state, "daily_command_counts", {})
    result = []
    for date, counts in sorted(daily_counts.items())[-28:]:
        total = sum(counts.values()) if isinstance(counts, dict) else counts
        result.append({"date": date, "count": total})
    return {"heatmap": result}


# --- History API ---
@_if_app("get", "/api/history")
def get_history(limit: int = 50):
    try:
        from memory import get_chat_history, init_db

        conn = init_db()
        history = get_chat_history(conn, limit=limit)
        return {"history": history}
    except Exception as e:
        return {"history": [], "error": "Internal error"}


@_if_app("get", "/api/history/eras")
def get_history_eras():
    try:
        from handlers.history import ERAS

        state = get_state()
        completed = getattr(state, "timeline_completed", [])
        result = []
        for era in ERAS:
            result.append(
                {
                    "name": era["name"],
                    "period": era["period"],
                    "description": era["description"],
                    "xp": era.get("xp", 20),
                    "completed": era["name"] in completed,
                    "events": era.get("events", []),
                    "tools": ", ".join(era.get("tools", [])),
                    "vulnerabilities": ", ".join(era.get("vulnerabilities", [])),
                }
            )
        return {"eras": result}
    except Exception as e:
        return {"eras": [], "error": "Internal error"}


@_if_app("post", "/api/history/study")
def study_history_era(era: str):
    try:
        from handlers.history import ERAS

        era_data = next((e for e in ERAS if e["name"] == era), None)
        if not era_data:
            raise HTTPException(status_code=404, detail="Era not found")
        state = get_state()
        completed = getattr(state, "timeline_completed", [])
        if era not in completed:
            completed.append(era)
            state.timeline_completed = completed
            xp = era_data.get("xp", 20)
            state.xp = getattr(state, "xp", 0) + xp
        return {
            "status": "ok",
            "era": era,
            "events": era_data.get("events", []),
            "tools": ", ".join(era_data.get("tools", [])),
            "vulnerabilities": ", ".join(era_data.get("vulnerabilities", [])),
            "xp_earned": era_data.get("xp", 20),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("get", "/api/history/progress")
def get_history_progress():
    state = get_state()
    return {
        "completed_eras": getattr(state, "timeline_completed", []),
        "xp": getattr(state, "xp", 0),
    }


# --- Config API ---
@_if_app("get", "/api/config")
def get_config():
    import config

    state = get_state()
    return {
        "llm_provider": config.LLM_PROVIDER,
        "model": config.get_model_name(),
        "language": getattr(state, "language", "ru"),
        "theme": getattr(state, "current_theme", "dark"),
        "depth": getattr(state, "explanation_depth", "normal"),
        "offline_mode": getattr(state, "offline_mode", False),
        "feature_flags": getattr(state, "feature_flags", {}),
    }


# --- Writeups API ---
@_if_app("get", "/api/writeups")
def get_writeups():
    import os

    writeups = []
    if os.path.exists("writeups"):
        for f in os.listdir("writeups"):
            if f.endswith(".md"):
                writeups.append(
                    {
                        "name": f.replace(".md", ""),
                        "date": os.path.getmtime(os.path.join("writeups", f)),
                    }
                )
    return {"writeups": sorted(writeups, key=lambda x: x["date"], reverse=True)}


@_if_app("get", "/api/writeups/{name}")
def get_writeup_content(name: str):
    import os

    safe_name = os.path.basename(name).replace("..", "")
    filepath = os.path.join("writeups", safe_name)
    if not filepath.endswith(".md"):
        filepath += ".md"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Writeup not found")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return {"name": safe_name, "content": content}


# --- Settings / Config API ---
@_if_app("post", "/api/provider/set")
def set_provider(provider: str = ""):
    """Switch the active LLM provider."""
    if not provider:
        raise HTTPException(status_code=400, detail="provider required")
    import config as _cfg

    valid = _cfg.FALLBACK_ORDER + ["mock", "lmstudio"]
    if provider not in valid:
        raise HTTPException(
            status_code=400, detail=f"Unknown provider. Valid: {', '.join(valid)}"
        )
    _cfg.LLM_PROVIDER = provider
    _cfg.LazyLoader.invalidate()
    return {"status": "ok", "provider": provider}


@_if_app("post", "/api/provider/key")
def set_provider_key(provider: str = "", key: str = ""):
    """Set API key for a cloud provider."""
    import os

    key_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "groq": "GROQ_API_KEY",
        "huggingface": "HUGGINGFACE_API_KEY",
    }
    env_var = key_map.get(provider)
    if not env_var:
        raise HTTPException(
            status_code=400, detail=f"Provider {provider} does not use API keys"
        )
    if not key:
        raise HTTPException(status_code=400, detail="key required")
    os.environ[env_var] = key
    import config as _cfg

    setattr(_cfg, env_var, key)
    _cfg.LazyLoader.invalidate()
    return {"status": "ok", "provider": provider}


# --- Provider info / LM Studio check ---
@_if_app("get", "/api/providers")
def list_providers():
    import config as _cfg

    available = _cfg.FALLBACK_ORDER + ["mock", "lmstudio"]
    current = _cfg.LLM_PROVIDER
    lmstudio_ok = False
    try:
        import urllib.request

        req = urllib.request.Request("http://localhost:1234/v1/models", method="GET")
        with urllib.request.urlopen(req, timeout=2) as r:
            lmstudio_ok = r.status == 200
    except (OSError, ValueError):
        pass
    providers = []
    for p in available:
        status = "active" if p == current else "available"
        if p == "lmstudio":
            status = "running" if lmstudio_ok else "not_found"
        providers.append({"name": p, "status": status, "current": p == current})
    return {"providers": providers, "current": current, "lmstudio_running": lmstudio_ok}


@_if_app("get", "/api/provider/lmstudio/check")
def check_lmstudio():
    try:
        import urllib.request

        req = urllib.request.Request("http://localhost:1234/v1/models", method="GET")
        with urllib.request.urlopen(req, timeout=2) as r:
            if r.status != 200:
                return {"running": False, "error": f"HTTP {r.status}"}
            import json

            data = json.loads(r.read().decode())
            models = [m.get("id", "unknown") for m in data.get("data", [])]
            return {"running": True, "models": models}
    except Exception as e:
        return {"running": False, "error": str(e)}


@_if_app("post", "/api/provider/set_url")
def set_provider_url(provider: str = "", url: str = ""):
    import os

    url_map = {
        "ollama": "OLLAMA_BASE_URL",
        "lmstudio": "LMSTUDIO_BASE_URL",
        "openrouter": "OPENROUTER_BASE_URL",
    }
    env_var = url_map.get(provider)
    if not env_var:
        raise HTTPException(
            status_code=400, detail=f"Provider {provider} does not support custom URL"
        )
    if not url:
        raise HTTPException(status_code=400, detail="url required")
    os.environ[env_var] = url
    import config as _cfg

    setattr(_cfg, env_var, url)
    _cfg.LazyLoader.invalidate()
    return {"status": "ok", "provider": provider, "url": url}


@_if_app("post", "/api/features/toggle")
def toggle_feature(feature: str = ""):
    """Toggle a feature flag on/off."""
    if not feature:
        raise HTTPException(status_code=400, detail="feature required")
    state = get_state()
    flags = getattr(state, "feature_flags", {})
    current = flags.get(feature, True)
    flags[feature] = not current
    state.feature_flags = flags
    return {"status": "ok", "feature": feature, "enabled": not current}


@_if_app("post", "/api/settings/lang")
def set_language(lang: str = ""):
    """Set interface language."""
    if lang not in ("ru", "en"):
        raise HTTPException(status_code=400, detail="Supported languages: ru, en")
    state = get_state()
    state.language = lang
    return {"status": "ok", "language": lang}


# --- Context Budget Endpoints ---
@_if_app("get", "/api/context/budget")
def get_context_budget() -> dict[str, Any]:
    """Get context budget manager stats and configuration."""
    if not BUDGET_AVAILABLE or api_budget_manager is None:
        return {"available": False, "error": "ContextBudgetManager not available"}
    return {"available": True, "stats": api_budget_manager.get_stats()}


class BudgetConfigRequest(BaseModel):
    max_tokens: int = 8000
    system_prompt_tokens: int = 1500
    rag_context_tokens: int = 2000
    response_reserve: int = 1024


@_if_app("post", "/api/context/budget")
def set_context_budget(req: BudgetConfigRequest) -> dict[str, Any]:
    """Configure context budget manager."""
    if not BUDGET_AVAILABLE or api_budget_manager is None:
        return {"available": False, "error": "ContextBudgetManager not available"}
    api_budget_manager.max_tokens = req.max_tokens
    api_budget_manager.system_prompt_tokens = req.system_prompt_tokens
    api_budget_manager.rag_context_tokens = req.rag_context_tokens
    api_budget_manager.response_reserve = req.response_reserve
    return {"status": "ok", "config": api_budget_manager.get_stats()}


@_if_app("get", "/api/context/history")
def get_api_history(limit: int = 10) -> dict[str, Any]:
    """Get recent chat history from DB."""
    try:
        from memory import get_chat_history, init_db

        conn = init_db()
        history = get_chat_history(conn, limit=min(limit, 100))

        # Estimate budget usage
        stats = {}
        if BUDGET_AVAILABLE and api_budget_manager is not None:
            trimmed, warn = api_budget_manager.prepare_context(
                history, max_messages=limit, user_input=""
            )
            stats = {
                "total_messages": len(history),
                "trimmed_to": len(trimmed),
                "warning": warn,
            }

        return {"history": history, "budget": stats}
    except Exception as e:
        return {"history": [], "budget": {}, "error": str(e)[:100]}


# --- Story Mode Endpoints ---
# --- Tracks Endpoints ---
@_if_app("get", "/api/tracks")
def get_tracks():
    try:
        import glob, os, yaml

        tracks = []
        for path in glob.glob("tracks/*.yaml"):
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            state = get_state()
            track_progress = getattr(state, "track_progress", {})
            track_id = data.get("id", os.path.basename(path).replace(".yaml", ""))
            prog = track_progress.get(track_id, {})
            if isinstance(prog, dict):
                completed_topics = prog.get("completed_topics", [])
                total = len(data.get("topics", []))
                progress_pct = (
                    round(len(completed_topics) / total * 100) if total > 0 else 0
                )
            elif isinstance(prog, (int, float)):
                progress_pct = int(prog)
            else:
                progress_pct = 0

            tracks.append(
                {
                    "id": track_id,
                    "name": data.get("name", ""),
                    "description": data.get("description", ""),
                    "level": data.get("level", "beginner"),
                    "estimated_hours": data.get("estimated_hours", 0),
                    "topics_count": len(data.get("topics", [])),
                    "topics": data.get("topics", []),
                    "progress": progress_pct,
                    "prerequisites": data.get("prerequisites", []),
                }
            )
        return {"tracks": tracks}
    except Exception as e:
        return {"tracks": [], "error": "Internal error"}


@_if_app("post", "/api/tracks/start")
def start_track(track_id: str):
    state = get_state()
    state.current_track = track_id
    return {"status": "ok", "track": track_id}


@_if_app("post", "/api/tracks/progress")
def update_track_progress(track_id: str, progress: int):
    state = get_state()
    track_progress = getattr(state, "track_progress", {})
    track_progress[track_id] = progress
    state.track_progress = track_progress
    return {"status": "ok", "track": track_id, "progress": progress}


# --- CTF Endpoints ---
@_if_app("get", "/api/ctf/status")
def get_ctf_status():
    state = get_state()
    return {
        "flags_captured": getattr(state, "flags_captured", 0),
        "risk_level": getattr(state, "risk_level", 0),
        "ctf_active": getattr(state, "ctf_active", False),
    }


@_if_app("post", "/api/ctf/flag")
def submit_flag(flag_value: str):
    try:
        from story_mode import STORY_EPISODES

        state = get_state()
        all_flags = [ep.get("flag", "") for ep in STORY_EPISODES if ep.get("flag")]
        found = any(f.lower() == flag_value.strip().lower() for f in all_flags)

        if found:
            state.flags_captured = getattr(state, "flags_captured", 0) + 1
            state.xp = getattr(state, "xp", 0) + 50
            return {"correct": True, "xp_earned": 50, "message": "Флаг найден! 🚩"}
        else:
            return {"correct": False, "message": "Неверный флаг"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("get", "/api/missions")
def get_missions():
    try:
        from handlers.missions import _list_missions_api

        return {"missions": _list_missions_api()}
    except Exception as e:
        return {"missions": [], "error": "Internal error"}


@_if_app("post", "/api/missions/start")
def start_mission(mission_id: str):
    try:
        from handlers.missions import _load_mission

        mission_data = _load_mission(mission_id)
        if mission_data is None:
            raise HTTPException(status_code=404, detail="Mission not found")
        state = get_state()
        completed = set(getattr(state, "missions_completed", []))
        prereqs = mission_data.get("prerequisites", [])
        missing = [p for p in prereqs if p not in completed]
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Requires missions: {', '.join(missing)}",
            )
        if mission_id in completed:
            raise HTTPException(status_code=400, detail="Mission already completed")
        state.current_mission = mission_id
        return {"status": "ok", "mission": mission_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@_if_app("post", "/api/missions/submit")
def submit_mission_flag(mission_id: str, flag: str):
    try:
        from handlers.missions import _load_mission

        mission_data = _load_mission(mission_id)
        if mission_data is None:
            raise HTTPException(status_code=404, detail="Mission not found")
        state = get_state()
        completed = getattr(state, "missions_completed", [])
        if mission_id in completed:
            return {"correct": False, "message": "Mission already completed"}
        steps = mission_data.get("steps", [])
        for step in steps:
            expected = step.get("flag", "")
            if expected and expected.lower() in flag.lower():
                if mission_id not in completed:
                    completed.append(mission_id)
                    state.missions_completed = completed
                    xp = mission_data.get("xp_reward", 0)
                    state.xp = getattr(state, "xp", 0) + xp
                return {
                    "correct": True,
                    "xp_earned": xp,
                    "step": step.get("order", 1),
                    "message": f"Step {step.get('order', 1)} completed!",
                }
        return {"correct": False, "message": "Invalid flag for this mission"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- OSINT / Threats Endpoints ---
@_if_app("get", "/api/threats")
def get_threats():
    try:
        import glob, json, os as _os

        threats_dir = _os.path.join(_os.path.dirname(__file__), "threats")
        result = []
        for path in sorted(glob.glob(_os.path.join(threats_dir, "*.json"))):
            with open(path, "r", encoding="utf-8") as f:
                g = json.load(f)
            result.append(
                {
                    "id": _os.path.splitext(_os.path.basename(path))[0],
                    "name": g.get("name", ""),
                    "country": g.get("country", ""),
                    "targets": ", ".join(g.get("targets", [])),
                    "description": g.get("description", ""),
                    "aliases": g.get("aliases", []),
                    "tactics": g.get("tactics", []),
                    "tools": g.get("tools", []),
                    "first_seen": g.get("first_seen", ""),
                    "recent_activity": g.get("recent_activity", ""),
                }
            )
        return {"threats": result}
    except Exception as e:
        return {"threats": [], "error": "Internal error"}


@_if_app("get", "/api/cve/{cve_id}")
def get_cve(cve_id: str):
    try:
        from handlers.cve import CVE_CACHE

        cached = CVE_CACHE.get(cve_id.upper())
        cve_data: dict[str, Any] | None = None
        if cached:
            cve_data = cached[1]
        else:
            from handlers.cve import _fetch_cve

            cve_data = _fetch_cve(cve_id.upper())
            if not cve_data:
                raise HTTPException(status_code=404, detail="CVE not found")
        return {"cve": cve_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- External APIs: Shodan ---
@_if_app("get", "/api/shodan")
def shodan_search(query: str = ""):
    from handlers.shodan_censys import _simulate_shodan_search

    if not query:
        return {"results": [], "error": "query required"}
    results = _simulate_shodan_search(query)
    return {"results": results, "total": len(results)}


@_if_app("get", "/api/shodan/host")
def shodan_host(ip: str = ""):
    from handlers.shodan_censys import _simulate_shodan_host

    if not ip:
        raise HTTPException(status_code=400, detail="ip required")
    data = _simulate_shodan_host(ip)
    return {"host": data}


# --- External APIs: Censys ---
@_if_app("get", "/api/censys")
def censys_search(query: str = ""):
    from handlers.shodan_censys import _simulate_censys_search

    if not query:
        return {"results": [], "error": "query required"}
    results = _simulate_censys_search(query)
    return {"results": results, "total": len(results)}


# --- External APIs: HackTheBox ---
@_if_app("get", "/api/htb/machines")
def htb_machines(machine_type: str = "all"):
    try:
        from handlers.htb import _fetch_htb_machines

        machines = _fetch_htb_machines(machine_type)
        return {"machines": machines[:50], "total": len(machines)}
    except Exception as e:
        return {"machines": [], "error": str(e)}


@_if_app("get", "/api/htb/machine/{machine_id}")
def htb_machine(machine_id: int):
    try:
        from handlers.htb import _fetch_htb_machine_detail

        machine = _fetch_htb_machine_detail(machine_id)
        if not machine:
            raise HTTPException(status_code=404, detail="Machine not found")
        return {"machine": machine}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_if_app("get", "/api/htb/status")
def htb_status():
    try:
        from handlers.htb import handle_htb_status

        handle_htb_status("")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# --- External APIs: TryHackMe ---
@_if_app("get", "/api/thm/rooms")
def thm_rooms(room_type: str = "all"):
    try:
        from handlers.tryhackme import _thm_request

        data = _thm_request("/v2/rooms")
        rooms = data.get("data", []) if data else []
        if room_type != "all":
            rooms = [r for r in rooms if r.get("type", "").lower() == room_type.lower()]
        return {"rooms": rooms[:50], "total": len(rooms)}
    except Exception as e:
        return {"rooms": [], "error": str(e)}


@_if_app("get", "/api/thm/room/{room_id}")
def thm_room(room_id: str):
    try:
        from handlers.tryhackme import _thm_request

        data = _thm_request(f"/v2/rooms/{room_id}")
        if not data or not data.get("success"):
            raise HTTPException(status_code=404, detail="Room not found")
        return {"room": data.get("data", {})}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_if_app("get", "/api/thm/status")
def thm_status():
    try:
        from handlers.tryhackme import _thm_request

        data = _thm_request("/v2/user/info")
        if not data or not data.get("success"):
            return {"status": "error", "error": "Not authenticated"}
        user = data.get("data", {})
        profile = user.get("publicProfile", {})
        return {
            "username": user.get("username"),
            "rank": profile.get("rank"),
            "level": profile.get("level"),
            "streak": profile.get("streak", 0),
            "points": profile.get("points", 0),
            "badges": len(profile.get("badges", [])),
            "rooms_completed": profile.get("completedRooms", 0),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@_if_app("get", "/api/news")
def get_news():
    try:
        from news_fetcher import NewsFetcher

        nf = NewsFetcher()
        news = nf.get_formatted_news()
        return {"news": news if isinstance(news, list) else []}
    except ImportError:
        return {"news": []}


# --- Scanner Endpoints ---
@_if_app("post", "/api/scanv2")
def scan_code_simple(code: str, language: str = "python") -> dict[str, Any]:
    try:
        import tempfile
        from handlers.code_review_v2 import (
            LANGUAGE_EXTENSIONS,
            _count_severities,
            scan_file_secrets,
        )

        ext = next((k for k, v in LANGUAGE_EXTENSIONS.items() if v == language), ".py")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=ext, delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            temp_path = f.name

        try:
            findings = scan_file_secrets(temp_path)
            return {
                "findings": findings,
                "severity_counts": _count_severities(findings),
            }
        finally:
            import os

            with contextlib.suppress(Exception):
                os.unlink(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- Malware Analysis Endpoints ---
@_if_app("post", "/api/malware")
def analyze_malware(file_hash: str = "", behavior: str = "") -> dict[str, Any]:
    try:
        from handlers.malware_analysis import MALWARE_FAMILIES

        result: dict[str, Any] = {}
        if file_hash:
            if file_hash in MALWARE_FAMILIES:
                result = {
                    "hash": file_hash,
                    "family": file_hash,
                    "analysis": f"Known malware family: {file_hash}",
                }
            else:
                result = {
                    "hash": file_hash,
                    "unknown": True,
                    "analysis": "Sample not in database",
                }
        elif behavior:
            result = {
                "behavior": behavior,
                "analysis": f"Behavioral analysis of: {behavior}",
            }
        else:
            result = {"message": "Provide file_hash or behavior parameter"}
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# --- SCORM Export Endpoints ---


@_if_app("get", "/api/scorm/courses")
def scorm_list_courses():
    """List courses available for SCORM export."""
    from scorm_export import list_exportable_courses

    return {"courses": list_exportable_courses()}


@_if_app("post", "/api/scorm/export")
def scorm_export(course_id: str = "", token: str = ""):
    """Export a course as SCORM 1.2 .zip package."""
    if not course_id:
        raise HTTPException(status_code=400, detail="course_id required")
    import io
    from scorm_export import export_scorm_package_bytes

    try:
        zip_bytes = export_scorm_package_bytes(course_id)
        from fastapi.responses import StreamingResponse

        return StreamingResponse(
            io.BytesIO(zip_bytes),
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="scorm_{course_id}.zip"'
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (OSError, IOError):
        raise HTTPException(status_code=500, detail="SCORM export failed")


# --- Auth Endpoints ---

LOGIN_RATE_LIMIT = int(os.getenv("AUTH_RATE_LIMIT", "10"))


@_if_app("post", "/api/auth/register")
def register(username: str = "", password: str = "", display_name: str = ""):
    """Register a new user. Rate limited: 5 requests per minute."""
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    client_ip = "register"
    if _rate_limiter.is_limited(client_ip, 5, 60):
        raise HTTPException(
            status_code=429, detail="Too many requests. Try again later."
        )
    from auth import create_user

    result = create_user(username, password, display_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@_if_app("post", "/api/auth/login")
def login(username: str = "", password: str = ""):
    """Login and get JWT token. Rate limited."""
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")
    client_ip = f"login:{username}"
    if _rate_limiter.is_limited(client_ip, LOGIN_RATE_LIMIT, 60):
        raise HTTPException(
            status_code=429, detail="Too many login attempts. Try again later."
        )
    from auth import authenticate

    result = authenticate(username, password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result


@_if_app("get", "/api/auth/verify")
def verify_auth(token: str = ""):
    """Verify JWT token and return user info."""
    if not token:
        raise HTTPException(status_code=400, detail="token required")
    from auth import verify_token, get_user

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user(payload["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"valid": True, "user": user}


@_if_app("get", "/api/users")
def list_users(token: str = ""):
    """List all users (admin only)."""
    from auth import has_permission, list_users as _list_users

    if not has_permission(token, "manage_users"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return {"users": _list_users()}


@_if_app("post", "/api/users/role")
def set_role(token: str = "", target_user: str = "", role: str = ""):
    """Set user role (admin only)."""
    from auth import has_permission, set_role as _set_role

    if not has_permission(token, "manage_users"):
        raise HTTPException(status_code=403, detail="Admin access required")
    if not target_user or not role:
        raise HTTPException(status_code=400, detail="target_user and role required")
    from auth import list_users as _list_users

    users = _list_users()
    target = next((u for u in users if u["username"] == target_user), None)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    success = _set_role(target["user_id"], role)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid role")
    return {"status": "ok", "user": target_user, "role": role}


@_if_app("get", "/api/report")
def export_report(token: str = ""):
    """Generate and return HTML training report."""
    if not token:
        raise HTTPException(status_code=400, detail="token required")
    from auth import verify_token

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    state = get_state()
    from report_generator import generate_report_html
    from fastapi.responses import HTMLResponse

    html = generate_report_html(state)
    return HTMLResponse(content=html)


@_if_app("post", "/api/feedback")
def submit_feedback(name: str = "", message: str = ""):
    """Save user feedback to a JSON file."""
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    feedback_dir = os.path.join(os.path.dirname(__file__), "feedback")
    os.makedirs(feedback_dir, exist_ok=True)
    entry = {
        "name": name or "Anonymous",
        "message": message,
        "timestamp": datetime.now().isoformat(),
    }
    path = os.path.join(feedback_dir, f"feedback_{int(time.time())}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)
    return {
        "status": "ok",
        "detail": "\u0421\u043f\u0430\u0441\u0438\u0431\u043e! \u0412\u0430\u0448\u0430 \u043e\u0431\u0440\u0430\u0442\u043d\u0430\u044f \u0441\u0432\u044f\u0437\u044c \u043f\u0440\u0438\u043d\u044f\u0442\u0430.",
    }


# --- Course Management (teacher/admin) ---


@_if_app("post", "/api/courses/create")
def create_course(
    token: str = "", name: str = "", description: str = "", difficulty: str = "beginner"
):
    """Create a new course (teacher/admin only)."""
    from auth import has_permission

    if not has_permission(token, "manage_courses"):
        raise HTTPException(status_code=403, detail="Teacher access required")
    if not name:
        raise HTTPException(status_code=400, detail="Course name required")
    from course_manager import create_course as _create_course
    from auth import verify_token

    payload = verify_token(token)
    creator = payload.get("username", "teacher") if payload else "teacher"
    result = _create_course(
        name, description, difficulty=difficulty, created_by=creator
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@_if_app("post", "/api/courses/update")
def update_course(
    token: str = "", course_id: str = "", name: str = "", description: str = ""
):
    """Update a course (teacher/admin only)."""
    from auth import has_permission

    if not has_permission(token, "manage_courses"):
        raise HTTPException(status_code=403, detail="Teacher access required")
    if not course_id:
        raise HTTPException(status_code=400, detail="course_id required")
    from course_manager import update_course as _update_course

    kwargs: dict = {}
    if name:
        kwargs["name"] = name
    if description:
        kwargs["description"] = description
    result = _update_course(course_id, **kwargs)
    if not result:
        raise HTTPException(status_code=404, detail="Course not found")
    return result


@_if_app("post", "/api/courses/delete")
def delete_course(token: str = "", course_id: str = ""):
    """Delete a course (admin only, non-default only)."""
    from auth import has_permission

    if not has_permission(token, "manage_courses"):
        raise HTTPException(status_code=403, detail="Admin access required")
    if not course_id:
        raise HTTPException(status_code=400, detail="course_id required")
    from course_manager import delete_course as _delete_course

    if not _delete_course(course_id):
        raise HTTPException(
            status_code=400, detail="Cannot delete (not found or built-in)"
        )
    return {"status": "deleted", "course_id": course_id}


@_if_app("post", "/api/courses/topic")
def add_topic(token: str = "", course_id: str = "", topic: str = ""):
    """Add a topic to a course (teacher/admin only)."""
    from auth import has_permission

    if not has_permission(token, "manage_courses"):
        raise HTTPException(status_code=403, detail="Teacher access required")
    from course_manager import add_topic as _add_topic

    if not _add_topic(course_id, topic):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"status": "ok", "course_id": course_id, "topic": topic}


# --- GDPR Export/Import ---


@_if_app("get", "/api/gdpr/export")
def export_user_data(token: str = ""):
    """Export all user data (GDPR compliance)."""
    if not token:
        raise HTTPException(status_code=400, detail="token required")
    from auth import verify_token, get_user, list_users

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("user_id", "")
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    state = get_state()
    return {
        "user": user,
        "state": {
            "xp": state.xp,
            "level": state.level,
            "points": state.points,
            "reputation": state.reputation,
            "quizzes_taken": state.quizzes_taken,
            "labs_started": state.labs_started,
            "skills": state.skills,
            "weak_topics": state.weak_topics,
            "earned_achievements": state.earned_achievements,
            "course_progress": state.course_progress,
        },
        "exported_at": time.time(),
        "version": "5.8",
    }


@_if_app("post", "/api/gdpr/import")
def import_user_data(token: str = "", data: dict = {}):
    """Import user data (admin only)."""
    from auth import has_permission, verify_token

    if not has_permission(token, "manage_users"):
        raise HTTPException(status_code=403, detail="Admin access required")
    if not data:
        raise HTTPException(status_code=400, detail="data required")
    user = data.get("user", {})
    state_data = data.get("state", {})
    if not user.get("user_id"):
        raise HTTPException(status_code=400, detail="user.user_id required")

    # Restore state fields
    state = get_state()
    for field in [
        "xp",
        "level",
        "points",
        "reputation",
        "quizzes_taken",
        "labs_started",
        "skills",
        "weak_topics",
        "earned_achievements",
        "course_progress",
    ]:
        if field in state_data:
            setattr(state, field, state_data[field])

    return {"status": "ok", "imported_fields": list(state_data.keys())}


# --- Atmosphere & Personality Endpoints ---


@_if_app("get", "/api/personality")
def get_personality():
    """Текущие personality modifiers (sarcasm, patience, paranoia, etc.)."""
    try:
        from personality import get_personality_state

        state = get_personality_state()
        return {"modifiers": state.get_modifiers()}
    except ImportError:
        return {
            "modifiers": {
                "sarcasm": 0.2,
                "patience": 0.5,
                "paranoia": 0.0,
                "enthusiasm": 0.3,
                "formality": 0.0,
            }
        }


@_if_app("get", "/api/context")
def get_context():
    """Текущий контекст: время суток, паттерн сессии."""
    try:
        from context_awareness import get_context_info

        state = get_state()
        return get_context_info(
            session_start=state.metrics.get("start_time", 0),
            messages_this_session=state.messages_sent,
        )
    except ImportError:
        return {"time_of_day": "afternoon", "session_pattern": "normal"}


@_if_app("get", "/api/world")
def get_world():
    """Persistent world state: incidents, factions, hidden knowledge."""
    try:
        from world_state import get_world_state

        world = get_world_state()
        return world.get_world_summary()
    except ImportError:
        return {
            "active_incidents": 0,
            "resolved_incidents": 0,
            "discovered_factions": [],
            "unlocked_knowledge": [],
        }


@_if_app("get", "/api/episodes")
def get_episodes():
    """Episode memory: important learning events."""
    try:
        from episode_memory import get_episode_memory

        mem = get_episode_memory()
        return {"episodes": mem.get_recent(20), "stats": mem.get_stats()}
    except ImportError:
        return {"episodes": [], "stats": {"total_episodes": 0, "by_category": {}}}


@_if_app("get", "/api/cyberpsychosis")
def get_cyberpsychosis():
    """Cyberpsychosis status: stress, obsession, recklessness."""
    try:
        from cyberpsychosis import get_cyberpsychosis

        cp = get_cyberpsychosis()
        return {"level": cp.get_level(), "state": cp.get_state_dict()}
    except ImportError:
        return {
            "level": "normal",
            "state": {"stress": 0, "obsession": 0, "recklessness": 0},
        }


# --- Social Engineering API ---
@_if_app("get", "/api/social/scenarios")
def social_scenarios():
    from handlers.social import SCENARIOS

    return {
        "scenarios": {
            k: {"name": v["name"], "goal": v["goal"]} for k, v in SCENARIOS.items()
        }
    }


# --- Phishing API ---
@_if_app("get", "/api/phishing/templates")
def phishing_templates():
    from handlers.phishing import PHISHING_TEMPLATES

    return {
        "templates": {
            k: {"name": v["name"], "scenario": v["scenario"], "elements": v["elements"]}
            for k, v in PHISHING_TEMPLATES.items()
        }
    }


@_if_app("post", "/api/phishing/generate")
def phishing_generate(req: PhishingGenerateRequest):
    from handlers.phishing import PHISHING_TEMPLATES
    import random
    from config import LazyLoader

    tt = req.template_type
    if tt and tt not in PHISHING_TEMPLATES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown template. Available: {', '.join(PHISHING_TEMPLATES.keys())}",
        )
    if not tt:
        tt = random.choice(list(PHISHING_TEMPLATES.keys()))

    template = PHISHING_TEMPLATES[tt]
    llm = LazyLoader.get_llm()
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM not available")

    prompt = f"""Ты — эксперт по социальной инженерии (в образовательных целях).
Создай пример фишингового письма для обучения кибербезопасности.

Тип: {template["name"]}
Сценарий: {template["scenario"]}
Ключевые элементы: {", ".join(template["elements"])}

Создай:
1. Subject (тема письма)
2. Sender (отправитель)
3. Body (тело письма)
4. Объясни, какие техники социальной инженерии использованы
5. Покажи, как распознать этот фишинг

ВАЖНО: Это образовательный пример. Не используй реальные данные компаний."""

    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)

    ctx = get_context()
    state = ctx.state
    state.phishing_generated = getattr(state, "phishing_generated", 0) + 1

    return {
        "content": content,
        "template": tt,
        "template_name": template["name"],
    }


# --- Sandbox API ---
@_if_app("post", "/api/sandbox/run")
def sandbox_run(req: SandboxRunRequest):
    from handlers.sandbox import run_code_in_sandbox

    result = run_code_in_sandbox(req.code, req.language, req.timeout)
    return result


# --- Network / Docker Status API ---
@_if_app("get", "/api/network/status")
def network_status():
    try:
        from practice import DOCKER_LABS
        from handlers.network import get_container_status

        labs = {}
        running = 0
        for key, lab in DOCKER_LABS.items():
            container_name = f"{key}-web"
            status = get_container_status(container_name)
            is_running = status.get("running", False)
            if is_running:
                running += 1
            labs[key] = {
                "name": lab.get("name", key),
                "ports": lab.get("ports", []),
                "running": is_running,
            }
        return {"labs": labs, "running": running, "total": len(DOCKER_LABS)}
    except Exception as e:
        return {"labs": {}, "running": 0, "total": 0, "error": str(e)}


# --- Mood API ---
@_if_app("get", "/api/mood")
def get_mood():
    from handlers.mood import MOODS
    from di import get_context

    state = get_context().state
    current = getattr(state, "mood", "normal")
    return {"moods": MOODS, "current": current}


@_if_app("post", "/api/mood/set")
def set_mood(mood: str = "normal"):
    from handlers.mood import MOODS

    if mood not in MOODS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown mood. Available: {', '.join(MOODS.keys())}",
        )
    from di import get_context

    state = get_context().state
    state.mood = mood
    return {"mood": mood, "name": MOODS[mood]["name"]}


# --- Emotions API ---
@_if_app("get", "/api/emotions")
def get_emotions():
    from handlers.emotions import EMOTION_STATES, get_emotion_status

    return {"states": EMOTION_STATES, "current": get_emotion_status()}


# --- Summary API ---
@_if_app("post", "/api/summary")
def get_summary(topic: str = ""):
    from config import LazyLoader
    from knowledge import get_current_vectordb, get_relevant_docs

    if not topic:
        raise HTTPException(status_code=400, detail="topic required")
    vectordb = get_current_vectordb()
    if not vectordb:
        raise HTTPException(status_code=503, detail="Knowledge base not available")
    docs = get_relevant_docs(vectordb, topic, top_k=5)
    context = (
        "\n\n".join(
            [
                f"Источник {i + 1}:\n{doc.page_content[:2000]}"
                for i, doc in enumerate(docs[:5])
            ]
        )
        if docs
        else "No context available."
    )
    llm = LazyLoader.get_llm()
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM not available")
    prompt = f"""Ты — эксперт по кибербезопасности. Создай структурированный конспект в Markdown по теме: "{topic}".

Контекст из учебных материалов:

{context}

Конспект должен включать:
1. Определение — кратко что это такое
2. Ключевые концепции — основные идеи, механизмы
3. Примеры — реальные или гипотетические примеры
4. Техники/Инструменты — если применимо
5. Ссылки на источники — укажи, какие источники использовались (из контекста)

Формат: Markdown с заголовками, списками, код-блоками где уместно.
Не добавляй введение или заключение — сразу приступай к делу."""
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return {"topic": topic, "content": content}


# --- Docker Gen API ---
DOCKER_IMAGES = [
    {
        "id": "dvwa",
        "name": "DVWA",
        "desc": "Damn Vulnerable Web Application",
        "ports": ["80:80"],
    },
    {
        "id": "metasploitable",
        "name": "Metasploitable",
        "desc": "Vulnerable Linux VM",
        "ports": [],
    },
    {"id": "vulnhub", "name": "VulnHub", "desc": "CTF-style challenges", "ports": []},
    {
        "id": "juice-shop",
        "name": "Juice Shop",
        "desc": "OWASP Juice Shop",
        "ports": ["3000:3000"],
    },
    {
        "id": "wordpress",
        "name": "WordPress",
        "desc": "Vulnerable WordPress",
        "ports": ["8080:80"],
    },
]


@_if_app("get", "/api/dockergen/images")
def dockergen_images():
    return {"images": DOCKER_IMAGES}


@_if_app("post", "/api/dockergen/generate")
def dockergen_generate(req: DockerGenRequest):
    import yaml
    from handlers.docker_gen import LAB_IMAGES

    services = {}
    for lab_name in req.labs:
        lab = LAB_IMAGES.get(lab_name)
        if not lab:
            continue
        service = {
            "image": lab["image"],
            "container_name": f"ct_{lab_name}",
            "restart": "unless-stopped",
            "networks": ["ct_lab_net"],
        }
        ports = lab.get("ports")
        if ports:
            service["ports"] = [f"{host}:{cont}" for host, cont in ports.items()]
        services[lab_name] = service
    if not services:
        raise HTTPException(status_code=400, detail="No valid labs selected")
    compose = {
        "version": "3.8",
        "services": services,
        "networks": {"ct_lab_net": {"driver": "bridge"}},
    }
    yaml_str = yaml.dump(compose, default_flow_style=False, allow_unicode=True)
    return {"compose": yaml_str, "services": len(services)}


# --- Equipment API ---
@_if_app("get", "/api/equipment")
def get_equipment():
    from tools_ram import TOOL_RAM_COSTS, MAX_RAM
    from di import get_context

    state = get_context().state
    selected = set(getattr(state, "selected_tools", []))
    tools = []
    for tool, cost in sorted(TOOL_RAM_COSTS.items()):
        tools.append({"name": tool, "cost": cost, "selected": tool in selected})
    used = sum(TOOL_RAM_COSTS.get(t, 0) for t in selected)
    return {"tools": tools, "used_ram": used, "max_ram": MAX_RAM}


@_if_app("post", "/api/equipment/toggle")
def toggle_equipment(tool: str = ""):
    from tools_ram import TOOL_RAM_COSTS, MAX_RAM
    from di import get_context

    if not tool or tool not in TOOL_RAM_COSTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown tool. Available: {', '.join(sorted(TOOL_RAM_COSTS.keys()))}",
        )
    ctx = get_context()
    state = ctx.state
    selected = set(getattr(state, "selected_tools", []))
    if tool in selected:
        state.selected_tools.remove(tool)
        result = False
    else:
        new_total = (
            sum(TOOL_RAM_COSTS.get(t, 0) for t in selected) + TOOL_RAM_COSTS[tool]
        )
        if new_total > MAX_RAM:
            raise HTTPException(status_code=400, detail="Not enough RAM")
        state.selected_tools.append(tool)
        result = True
    ctx.save_state()
    return {"tool": tool, "selected": result}


# --- Timeloop API ---
@_if_app("get", "/api/timeloop")
def get_timeloop():
    from handlers.timeloop import STORY_NODES
    from di import get_context

    state = get_context().state
    current = getattr(state, "timeloop_node", "start")
    history = getattr(state, "timeloop_history", [])
    return {
        "current_node": current,
        "node_data": STORY_NODES.get(current, {}),
        "history": history,
        "started": bool(getattr(state, "timeloop_started", False)),
    }


@_if_app("post", "/api/timeloop/start")
def start_timeloop():
    from di import get_context

    state = get_context().state
    state.timeloop_node = "start"
    state.timeloop_started = True
    state.timeloop_history = []
    return {"status": "ok", "node": "start"}


@_if_app("post", "/api/timeloop/choice")
def timeloop_choice(choice: str = ""):
    from handlers.timeloop import STORY_NODES
    from di import get_context

    if not choice:
        raise HTTPException(status_code=400, detail="choice required")
    ctx = get_context()
    state = ctx.state
    current = getattr(state, "timeloop_node", "start")
    node = STORY_NODES.get(current)
    if not node or choice not in node.get("choices", {}):
        raise HTTPException(status_code=400, detail="Invalid choice")
    next_node = node["choices"][choice]["next"]
    history = getattr(state, "timeloop_history", [])
    history.append(
        {"from": current, "choice": choice, "label": node["choices"][choice]["text"]}
    )
    state.timeloop_node = next_node
    state.timeloop_history = history
    ctx.save_state()
    return {
        "status": "ok",
        "node": next_node,
        "node_data": STORY_NODES.get(next_node, {}),
        "history": history,
    }


# --- Sync API ---
@_if_app("get", "/api/sync/id")
def get_sync_id():
    from handlers.sync import _generate_user_id

    return {"sync_id": _generate_user_id()}


@_if_app("get", "/api/sync/export")
def export_sync(filepath: str = ""):
    from handlers.sync import _export_progress

    success = _export_progress(filepath if filepath else None)
    if not success:
        raise HTTPException(status_code=500, detail="Export failed")
    return {"status": "ok", "filepath": filepath or "auto"}


# --- Exploit Trainer API ---
@_if_app("get", "/api/exploit/challenges")
def exploit_challenges():
    from handlers.exploit_trainer import EXPLOIT_CHALLENGES

    challenges = []
    for cid, c in EXPLOIT_CHALLENGES.items():
        challenges.append(
            {
                "id": cid,
                "name": c.get("title", cid),
                "difficulty": c.get("difficulty", "medium"),
                "category": c.get("category", ""),
                "description": c.get("description", "")[:200],
            }
        )
    return {"challenges": challenges}


# --- Analytics API ---
@_if_app("get", "/api/analytics")
def get_analytics():
    from handlers.analytics import _compute_learning_metrics
    from di import get_context

    state = get_context().state
    metrics = _compute_learning_metrics(state)
    return {"metrics": metrics}


# --- Mermaid Diagram API ---
@_if_app("get", "/api/mermaid/generate")
def mermaid_generate(topic: str = ""):
    from config import LazyLoader

    if not topic:
        raise HTTPException(status_code=400, detail="topic required")
    llm = LazyLoader.get_llm()
    if llm is None:
        raise HTTPException(status_code=503, detail="LLM not available")
    prompt = f"""Create a Mermaid diagram for cybersecurity topic: {topic}
Rules:
1. Use only valid Mermaid syntax
2. Type: flowchart, graph, sequence, or mindmap
3. Start with type declaration (e.g. flowchart TD)
4. Return ONLY Mermaid code, no explanations"""
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return {"topic": topic, "diagram": content}


# --- Bug Bounty API ---
BOUNTY_SCENARIOS = [
    {
        "id": "xss_discovery",
        "name": "XSS Vulnerability",
        "difficulty": "easy",
        "reward": 500,
    },
    {
        "id": "sqli_extraction",
        "name": "SQL Injection Data Extraction",
        "difficulty": "medium",
        "reward": 1500,
    },
    {
        "id": "idor_escalation",
        "name": "IDOR Privilege Escalation",
        "difficulty": "medium",
        "reward": 2000,
    },
    {
        "id": "ssrf_internal",
        "name": "SSRF to Internal Network",
        "difficulty": "hard",
        "reward": 5000,
    },
    {
        "id": "rce_chain",
        "name": "RCE via Deserialization",
        "difficulty": "hard",
        "reward": 10000,
    },
]


@_if_app("get", "/api/bounty/scenarios")
def bounty_scenarios():
    return {"scenarios": BOUNTY_SCENARIOS}


# --- Media API ---
MEDIA_RESOURCES = [
    {
        "id": "intro_network",
        "title": "Network Security Intro",
        "type": "video",
        "duration": "15:30",
    },
    {
        "id": "web_attacks",
        "title": "Web Attack Vectors",
        "type": "video",
        "duration": "22:00",
    },
    {"id": "crypto_basics", "title": "Cryptography Basics", "type": "pdf", "pages": 45},
    {
        "id": "malware_101",
        "title": "Malware Analysis 101",
        "type": "video",
        "duration": "30:00",
    },
    {"id": "osint_tools", "title": "OSINT Tools Guide", "type": "pdf", "pages": 30},
    {
        "id": "forensics_cheatsheet",
        "title": "Forensics Cheatsheet",
        "type": "pdf",
        "pages": 12,
    },
]


@_if_app("get", "/api/media")
def get_media():
    return {"resources": MEDIA_RESOURCES}


# --- Walkthroughs / Exploit Search API ---
@_if_app("get", "/api/walkthroughs")
def get_walkthroughs():
    import os, glob as _glob

    wts = []
    for path in _glob.glob("writeups/*.md"):
        name = os.path.splitext(os.path.basename(path))[0]
        wts.append({"name": name, "path": path, "date": os.path.getmtime(path)})
    return {"walkthroughs": sorted(wts, key=lambda x: x["date"], reverse=True)}


# --- WebSocket Auth Helper ---


def _ws_verify_token(websocket: Any) -> Optional[Dict[str, Any]]:
    """Extract and verify JWT from WebSocket query params. Returns payload or None."""
    token = websocket.query_params.get("token", "")
    if not token:
        return None
    from auth import verify_token

    return verify_token(token)


# --- WebSocket Streaming ---

if FASTAPI_AVAILABLE and app is not None:

    @app.websocket("/chat_stream")
    async def websocket_chat_stream(websocket: Any) -> None:
        from starlette.websockets import WebSocketDisconnect

        await websocket.accept()
        try:
            payload = _ws_verify_token(websocket)
            user_context = ""
            if payload:
                from auth import get_user

                user = get_user(payload.get("user_id", ""))
                if user:
                    user_context = f"\n[User: {user.get('display_name', user['username'])}, Role: {user.get('role', 'student')}]"

            params = websocket.query_params
            message = params.get("message", "")
            mode = params.get("mode", "teacher")
            if not message:
                await websocket.send_json({"error": "No message provided"})
                await websocket.close()
                return

            state = get_state()
            state.set_persona(mode)

            # Secret phrase detection
            try:
                from secret_language import detect_secret_phrase
                secret = detect_secret_phrase(message)
                if secret:
                    # Apply effect
                    if secret["effect"] == "hint":
                        state.hint_credits = min(10, state.hint_credits + 1)
                    elif secret["effect"] == "mood_serious":
                        state.current_mood = "serious"
                    elif secret["effect"] == "unlock_ghost_log":
                        pass

                    await websocket.send_json({
                        "secret_phrase": secret,
                        "response": f"🔐 **Секретная фраза:** {secret['phrase']}\n\n{secret['response']}",
                    })
                    await websocket.send_json({"done": True, "full_response": secret["response"]})
                    return
            except ImportError:
                pass

            from config import LazyLoader as _LazyLoader

            llm = _LazyLoader.get_llm()
            if llm is None:
                await websocket.send_json(
                    {"chunk": "[MockLLM] ИИ-провайдер недоступен. Настройте /doctor."}
                )
                await websocket.send_json(
                    {
                        "done": True,
                        "full_response": "[MockLLM] ИИ-провайдер недоступен.",
                    }
                )
                await websocket.close()
                return

            # Build system prompt
            from main import get_mode_prompt

            system_prompt = get_mode_prompt(mode, "", "", "")
            if user_context:
                system_prompt += user_context

            try:
                from context_awareness import get_context_info, get_atmosphere_hint
                from personality import apply_personality_drift

                ctx_info = get_context_info(
                    session_start=state.metrics.get("start_time", 0),
                    messages_this_session=state.messages_sent,
                )
                atm = get_atmosphere_hint(ctx_info)
                pmod = apply_personality_drift(ctx_info)
                if atm:
                    system_prompt += f"\n\n{atm}"
                if pmod:
                    system_prompt += f"\n\n{pmod}"
            except ImportError:
                pass

            # Persona Router (dynamic)
            try:
                from persona_router import (
                    select_persona,
                    get_persona_prompt,
                    get_persona_info,
                )

                persona_id = select_persona(state, message)
                persona_mod = get_persona_prompt(persona_id)
                if persona_mod:
                    system_prompt += persona_mod
                # Send persona info at start
                persona_info = get_persona_info(persona_id)
                await websocket.send_json({"persona": persona_info})
            except ImportError:
                pass

            from memory import get_chat_history, init_db

            conn = init_db()
            raw_history = get_chat_history(conn, limit=100)

            # Inject summary if available
            if BUDGET_AVAILABLE and api_budget_manager is not None:
                summary_text = api_budget_manager.extract_summary(raw_history)
                if summary_text:
                    system_prompt += f"\n\n[Context summary: {summary_text}]"

                trimmed_hist, _ = api_budget_manager.prepare_context(
                    raw_history, max_messages=30, user_input=message
                )
                history = trimmed_hist
            else:
                history = raw_history[-10:]
            context_str = "\n".join([f"{m['role']}: {m['content']}" for m in history])

            full_prompt = (
                f"{system_prompt}\n\n---\n{context_str}\n\nУченик: {message}\nУчитель:"
            )

            full_response = ""
            try:
                for chunk in llm.stream(full_prompt):
                    text = chunk.content if hasattr(chunk, "content") else str(chunk)
                    full_response += text
                    await websocket.send_json({"chunk": text})
            except (ValueError, RuntimeError) as e:
                if not full_response:
                    await websocket.send_json({"chunk": f"[Ошибка: {e}]"})
                    full_response = f"[Ошибка: {e}]"

            # Narrative events
            try:
                from handlers.event_engine import check_events

                fired = check_events()
                if fired:
                    event_block = []
                    for evt in fired:
                        msg = f"\n\n⚡ {evt['title']}: {evt['message']}"
                        if evt["effects"]:
                            msg += f" ({', '.join(evt['effects'])})"
                        event_block.append(msg)
                    full_response += "".join(event_block)
                    await websocket.send_json({"events": fired})
            except ImportError:
                pass

            await websocket.send_json({"done": True, "full_response": full_response})

            # Save to DB
            from memory import save_message, update_stats

            save_message(conn, "user", message, mode)
            save_message(conn, "assistant", full_response, mode)
            update_stats(conn, 1)
            state.messages_sent += 1

        except WebSocketDisconnect:
            pass
        except (ValueError, RuntimeError, ConnectionError) as e:
            try:
                await websocket.send_json({"error": "Internal error"})
                await websocket.close()
            except (ConnectionError, RuntimeError):
                pass

    @app.websocket("/notifications")
    async def websocket_notifications(websocket: Any) -> None:
        """WebSocket endpoint for real-time notifications. Public (no auth required)."""
        from starlette.websockets import WebSocketDisconnect

        await websocket.accept()
        try:
            last_check: float = 0.0
            while True:
                # Wait for messages or timeout
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_json(), timeout=30.0
                    )
                    if data.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                        continue
                except asyncio.TimeoutError:
                    pass

                # Push world state updates
                now = time.time()
                if now - last_check > 30:
                    last_check = now
                    try:
                        from world_state import get_world_state
                        from cyberpsychosis import get_cyberpsychosis

                        world = get_world_state()
                        if world.incidents:
                            for inc in world.incidents:
                                await websocket.send_json(
                                    {
                                        "type": "incident",
                                        "data": {
                                            "title": inc.get("title", ""),
                                            "severity": inc.get("severity", "low"),
                                        },
                                    }
                                )

                        cp = get_cyberpsychosis()
                        if cp.get_level() in ("critical", "dangerous"):
                            await websocket.send_json(
                                {
                                    "type": "cyberpsychosis",
                                    "data": {"level": cp.get_level()},
                                }
                            )
                    except ImportError:
                        pass

        except WebSocketDisconnect:
            pass
        except (ConnectionError, RuntimeError):
            try:
                await websocket.send_json({"error": "Closed"})
                await websocket.close()
            except (ConnectionError, RuntimeError):
                pass
        except (ConnectionError, RuntimeError, asyncio.TimeoutError, OSError):
            try:
                await websocket.close()
            except (ConnectionError, RuntimeError):
                pass

    @app.websocket("/quiz_multiplayer")
    async def websocket_quiz_multiplayer(websocket: Any) -> None:
        """WebSocket for multiplayer quizzes. Optional auth."""
        from starlette.websockets import WebSocketDisconnect

        await websocket.accept()
        try:
            payload = _ws_verify_token(websocket)
            player_name = "Player"
            if payload:
                from auth import get_user

                user = get_user(payload.get("user_id", ""))
                if user:
                    player_name = user.get("display_name", user["username"])
            room = None

            while True:
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_json(), timeout=60.0
                    )
                except asyncio.TimeoutError:
                    continue

                action = data.get("action", "")

                if action == "create":
                    from quiz_multiplayer import create_room

                    room_id = data.get("room", str(int(time.time())))
                    player_name = data.get("name", "Host")
                    room = create_room(room_id, player_name)
                    room.add_player(player_name, websocket)
                    await websocket.send_json(
                        {"type": "room_created", "room_id": room_id}
                    )
                    await websocket.send_json(
                        {"type": "state", "data": room.get_state()}
                    )

                elif action == "join":
                    from quiz_multiplayer import get_room

                    room_id = data.get("room", "")
                    player_name = data.get("name", "Player")
                    room = get_room(room_id)
                    if not room:
                        await websocket.send_json(
                            {"type": "error", "message": "Room not found"}
                        )
                        continue
                    room.add_player(player_name, websocket)
                    await websocket.send_json({"type": "joined", "room_id": room_id})
                    state = room.get_state()
                    await websocket.send_json({"type": "state", "data": state})
                    # Notify others
                    for pname, pdata in room.players.items():
                        if pname != player_name and pdata.get("ws"):
                            try:
                                await pdata["ws"].send_json(
                                    {
                                        "type": "player_joined",
                                        "name": player_name,
                                        "players": len(room.players),
                                    }
                                )
                            except (ConnectionError, RuntimeError):
                                pass

                elif action == "answer" and room:
                    answer_idx = data.get("answer", 0)
                    result = room.submit_answer(player_name, answer_idx)
                    await websocket.send_json({"type": "answer_result", "data": result})
                    # Send updated leaderboard to all
                    for pname, pdata in room.players.items():
                        try:
                            await pdata["ws"].send_json(
                                {
                                    "type": "leaderboard",
                                    "data": room.get_leaderboard(),
                                }
                            )
                        except (ConnectionError, RuntimeError):
                            pass

                elif action == "start" and room:
                    # Generate quiz questions
                    try:
                        from quiz_generator import generate_quiz_question

                        topic = data.get("topic", "general")
                        count = min(data.get("count", 5), 10)
                        questions = []
                        for _ in range(count):
                            q = await asyncio.get_event_loop().run_in_executor(
                                None, generate_quiz_question, topic
                            )
                            if q:
                                questions.append(q)
                        if questions:
                            room.set_questions(questions)
                            room.started = True
                            room.current_question = 0
                    except (ImportError, ValueError, RuntimeError):
                        # Fallback: use predefined questions
                        room.set_questions(
                            [
                                {
                                    "question": "What port does HTTPS use?",
                                    "options": ["80", "443", "8080"],
                                    "correct": 1,
                                },
                                {
                                    "question": "What is XSS?",
                                    "options": [
                                        "Cross-Site Scripting",
                                        "Extra Secure System",
                                        "XML Style Sheet",
                                    ],
                                    "correct": 0,
                                },
                                {
                                    "question": "What does a firewall do?",
                                    "options": [
                                        "Encrypts data",
                                        "Filters traffic",
                                        "Deletes viruses",
                                    ],
                                    "correct": 1,
                                },
                            ]
                        )
                        room.started = True
                        room.current_question = 0

                    # Send first question to all
                    state = room.get_state()
                    for pname, pdata in room.players.items():
                        try:
                            await pdata["ws"].send_json(
                                {"type": "question", "data": state["question"]}
                            )
                            await pdata["ws"].send_json(
                                {"type": "state", "data": state}
                            )
                        except (ConnectionError, RuntimeError):
                            pass

                elif action == "next" and room:
                    room.current_question += 1
                    room.answers = {}
                    if room.current_question >= len(room.questions):
                        room.finished = True
                    state = room.get_state()
                    for pname, pdata in room.players.items():
                        try:
                            if room.finished:
                                await pdata["ws"].send_json(
                                    {
                                        "type": "finished",
                                        "leaderboard": room.get_leaderboard(),
                                    }
                                )
                            else:
                                await pdata["ws"].send_json(
                                    {"type": "question", "data": state["question"]}
                                )
                            await pdata["ws"].send_json(
                                {"type": "state", "data": state}
                            )
                        except (ConnectionError, RuntimeError):
                            pass

                elif action == "state" and room:
                    await websocket.send_json(
                        {"type": "state", "data": room.get_state()}
                    )

        except WebSocketDisconnect:
            pass
        except (ConnectionError, RuntimeError, asyncio.TimeoutError):
            pass
        finally:
            if room and player_name:
                room.remove_player(player_name)
                if not room.players:
                    from quiz_multiplayer import delete_room

                    delete_room(room.room_id)


# ----------------------------------------------------------------------
# PWA state save endpoint
# ----------------------------------------------------------------------
@_if_app("post", "/api/save")
def pwa_save_state():
    """Save state on-demand (called by PWA beforeunload / periodic timer)."""
    from state import get_state
    from settings import get_settings

    try:
        state = get_state()
        state.save_to_file(str(get_settings().state_file))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# ----------------------------------------------------------------------
# Управление сервером
# ----------------------------------------------------------------------
def start_api_server(host: str = "0.0.0.0", port: int = 8000) -> bool:
    global _server_process
    if not FASTAPI_AVAILABLE:
        print("[API] FastAPI не установлен. Установите: pip install fastapi uvicorn")
        return False

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "api_server:app",
        "--host",
        host,
        "--port",
        str(port),
        "--log-level",
        "info",
    ]

    print(f"[API] Запуск сервера на {host}:{port}")
    print(f"[API] Документация: http://{host}:{port}/docs")

    try:
        _server_process = subprocess.Popen(cmd)
        return True
    except Exception as e:
        print(f"[API] Ошибка запуска: {e}")
        return False


def stop_api_server() -> bool:
    global _server_process
    if _server_process is None:
        print("[API] Сервер не запущен.")
        return False

    try:
        if sys.platform == "win32":
            _server_process.terminate()
        else:
            _server_process.send_signal(signal.SIGTERM)

        _server_process.wait(timeout=5)
        print("[API] Сервер остановлен.")
        _server_process = None
        return True
    except subprocess.TimeoutExpired:
        if _server_process is not None:
            _server_process.kill()
        _server_process = None
        print("[API] Сервер принудительно остановлен.")
        return True
    except Exception as e:
        print(f"[API] Ошибка остановки: {e}")
        return False


def is_server_running() -> bool:
    global _server_process
    if _server_process is None:
        return False
    return _server_process.poll() is None
