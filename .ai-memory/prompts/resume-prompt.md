# Resume Prompt

```text
You are continuing work on this software project.
Use the DevMemory AI context below as the source of truth before re-scanning the repository.
Respect privacy rules: do not request or expose secrets, credentials, tokens, certificates, private keys, local databases, or ignored build artifacts.
First, restate the current objective and propose the smallest safe next step.

## Project Summary

CyberTeacher — AI-наставник по кибербезопасности. CLI (Rich) + PWA (22 вкладки) + REST API (88 endpoints) + WebSocket. 1100+ тестов, 0 mypy ошибок. 99% задач выполнено (125/126).

**Стек:** Python, FastAPI, SQLAlchemy (SQLite/PostgreSQL), ChromaDB + BM25 (RAG), Ollama/Groq/OpenRouter (LLM providers). PWA на чистом JS (SPA, lazy tabs, IndexedDB offline, SW).

**Статус:** v5.21, готов к релизу. Осталось: P0 (ротация ключей), P2 (portable build), P3 (mobile/OAuth/2FA).

## Current State

Bullets describing what is working, what is in progress, and known issues after this session.

## Architecture

**Data Flow:** CLI/PWA → handle_extended_commands() / API → handlers/*.py → state.py (AppState singleton) → services/ → db.py (SQLAlchemy)

**LLM Layer:** LazyLoader → ResilientLLM (retry 2 + circuit breaker 3) → fallback chain (ollama→groq→openrouter→hf→mock). MockLLM — offline stub.

**Storage:** JSON files (state) + SQLite/PostgreSQL (messages, cache, achievements) + ChromaDB (RAG)

**Key modules:** context_budget.py (token-aware), personality.py (5 drift axes), cyberpsychosis.py (stress/obsession/recklessness), world_state.py (incidents/factions), episode_memory.py

**PWA:** 22 tabs, lazy-loaded, Service Worker v4, OfflineDB (IndexedDB), WebSocket streaming (/chat_stream, /notifications, /quiz_multiplayer)

## Commands

## Python (проект)
```bash
python main.py              # Запуск CLI
python api_server.py        # Запуск API + PWA
python launcher.py          # GUI-лаунчер
python -m pytest            # Все тесты
python -m pytest tests/ -v  # Конкретный тест
python index_project.py     # Обновить векторный индекс
```

## Docker
```bash
docker-compose up           # PostgreSQL + pgAdmin
docker ps                   # Статус контейнеров
docker stop cyberteacher-*  # Остановка лабы
```

## LLM
```bash
ollama pull qwen2.5:7b      # Локальная модель
ollama serve                # Запуск Ollama сервера
```

## CLI shortcuts
```bash
/menu                       # Цифровое меню (0-72)
/doctor                     # Статус LLM провайдеров
/context stats              # Статус контекста
```

## Next Actions

Bullet list of concrete near-term actions for the next session.
```
