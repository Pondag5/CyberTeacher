# Архитектура CyberTeacher

## Обзор
CyberTeacher — AI-наставник по кибербезопасности. CLI + PWA + REST API. Гибридная локальная/облачная LLM-архитектура с полным fallback до офлайн-режима.

## Компоненты

```
main.py (CLI)          api_server.py (FastAPI, ~140 endpoints)    launcher.py (tkinter GUI)
       \                       |                                        /
    handlers/ (79 .py)    static/js/tabs/ (58 .js)              панель управления
       |                       |                                    6 секций, 34 кнопки
    config.py ←── .env     app.js (53-58 tabs registered)
    db.py (16 SQLAlchemy моделей)
    resilient_llm.py / mock_llm.py
```

### 1. Backend Core
| Файл | Назначение |
|------|-----------|
| `main.py` | CLI точка входа, CachedLLM, main loop |
| `api_server.py` | FastAPI: 3981 стр., REST + 3 WebSocket |
| `config.py` | LazyLoader, get_llm(), провайдеры, .env |
| `di.py` | AppContext container (state, db, llm) |
| `db.py` | SQLAlchemy ORM, 16 моделей |
| `state.py` | AppState singleton, 150+ атрибутов |

### 2. Handlers (79 .py)
Каждый обработчик возвращает `HandlerResult(success, data, error, continue_session)`
- Registry pattern для точного/префиксного matching
- Полное покрытие тестами: 40 новых тестов (июнь 2026)

### 3. LLM Providers
| Provider | Тип | Конфиг |
|----------|-----|--------|
| Ollama | Локальный | `http://localhost:11434` |
| LM Studio | Локальный (OpenAI API) | `http://localhost:1234/v1` |
| Groq | Облачный (бесплатный) | API key |
| OpenRouter | Облачный (100+ моделей) | API key |
| HuggingFace | Облачный | API key |
| Mock | Офлайн-заглушка | Всегда доступен |

**Fallback цепочка:** `ollama → groq → openrouter → huggingface → lmstudio → mock`
**Circuit breaker:** 3 ошибки → пропуск провайдера на 60с
**Retry:** 2 попытки на провайдер

### 4. PWA Frontend (58 табов)
- Vanilla JS SPA с lazy-load табами
- WebSocket чат (`/chat_stream`) с ResilientLLM fallback
- Service Worker (Network First + cache fallback)
- IndexedDB OfflineDB для кеширования
- Cyberpunk тема: неон, глитч, canvas particles

### 5. Launcher (tkinter GUI)
6 секций, 34 кнопки, 4 индикатора (API/Postgres/Docker/MCP):
- **SERVER:** Start/Stop/Restart API, MCP, CLI
- **DATABASE:** PostgreSQL, pgAdmin, Migrations, SQLite
- **DOCKER:** Labs, Prune, Info
- **PWA LINKS:** Open PWA, Dashboard, CTF, Labs, Writeups, Recon
- **TOOLS:** Tests, KB, Logs, System Info, Env Config, Provider Settings
- **SERVICES:** MCP Test, Dependencies, Memory Cleanup

### 6. Базы данных
- **SQLite** (дефолт) — `./memory/chat_history.db`
- **PostgreSQL** (через Docker) — альтернатива
- **FAISS** — векторный поиск (126 МБ)
- **Alembic** — миграции (2 версии)

## Потоки данных
1. Пользователь → CLI/PWA → Registry → Handler → логика
2. Handler → DI (LLM, knowledge, state) → результат
3. LLM запросы → ResilientLLM (fallback chain) → кэш (SQLite TTL)
4. Изменения → JSON в `memory/` + опционально PostgreSQL

## Безопасность
- JWT аутентификация (HMAC-SHA256)
- bcrypt для паролей
- CSP, HSTS, rate limiting (10 req/min)
- Content Security Policy заголовки
