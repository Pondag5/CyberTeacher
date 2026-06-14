# Краткая долговременная память (MEMORY_SUMMARY.md)

Последнее обновление: 2026-05-29

## Обзор
Долговременная память CyberTeacher хранит ключевые факты о проекте, архитектурные решения и историю разработки.

## Архитектурные решения (ADR)
1. **Lazy Loader** — ленивая загрузка LLM/embeddings для быстрого старта
2. **Hybrid RAG** — ChromaDB + BM25 + cross-encoder reranking
3. **LLM Caching** — SQLite + TTL для кэширования ответов
4. **Singleton State** — `get_state()` синглтон AppState
5. **Rate Limiting** — sliding window 10 req/min

## Новые паттерны (2026-05-29)
6. **ResilientLLM** — provider fallback chain (retry 2 + circuit breaker 3)
7. **Context Budget** — token-aware context trimming (4 chars/token ratio)
8. **Memory Caps** — `_trim_unbounded_lists()` prevents JSON state growth
9. **Log Rotation** — RotatingFileHandler 5MB × 3
10. **MockLLM** — offline stub (intent detection: quiz/hint/explain/default)
11. **/doctor onboarding** — provider health check + setup wizard
12. **Context Awareness** — time-of-day, session pattern, atmosphere hints
13. **Personality Drift** — sarcasm/patience/paranoia/enthusiasm/formality drift

## Структура проекта (ключевые файлы)
- `main.py` — точка входа, CachedLLM, ContextBudgetManager, main loop
- `state.py` — AppState singleton (150+ атрибутов, 4 Pydantic-модуля, _trim_unbounded_lists)
- `config.py` — get_llm(), LazyLoader (с ResilientLLM fallback), provider config
- `resilient_llm.py` — ResilientLLM с retry + circuit breaker + fallback chain
- `context_budget.py` — ContextBudgetManager (token-aware, budget allocation)
- `di.py` — AppContext container (state, db_conn, llm)
- `db.py` — SQLAlchemy (Message, QueryCache, AppStateRecord)
- `memory.py` — save_message(), get_chat_history(), cache_response() (capped at 1000)
- `handlers/` — 60+ обработчиков с registry pattern
- `handlers/context.py` — /context stats, /context clear
- `handlers/doctor.py` — /doctor onboarding (status + setup wizard)
- `mock_llm.py` — MockLLM offline stub (intent detection)
- `context_awareness.py` — время суток, паттерны сессии, атмосферные подсказки
- `personality.py` — PersonalityState (5 drift axes), apply_personality_drift()
- `services/` — achievement_service (включён в state.check_achievements)
- `knowledge.py` — FAISS vector store (~126 МБ)

## Паттерны возврата обработчиков
Все обработчики возвращают: `tuple[bool, Any | None, Any | None, bool]`
- success, output_data, state_update, continue_loop

## Ключевые метрики (2026-05-29)
- mypy ошибок: **0** (было 106)
- Тестов: 985
- CLI команд: 96+ (+ /context)
- PWA вкладок: 18
- API endpoints: 40+

## История спринтов
- Спринт 1-5: Quick Wins, Analytics, Skills, Content, PWA — ✅ Done
- Спринт 6: Infrastructure (SQLAlchemy, PostgreSQL, Alembic) — ✅ Done
- Спринт 7: Code Polish (Ruff 0 errors) — ✅ Done
- Спринт 8: File Organization (cleanup 25 files, move 14 state files) — ✅ Done
- Спринт 9: State Migration (AppStateRecord, DB persistence) — ✅ Done
- Спринт 10: Type Hints (mypy 0 ошибок) — ✅ Done
- Спринт 11: Стабильность + Гибридная LLM-архитектура — ✅ Done (8/8 задач)
- Спринт 12: Атмосфера и UX (Context Awareness, Personality Drift, LLM stats, Backup/Log rotation) — ✅ Done (6/6)
- Спринт 13: Persistent World + Episode Memory + Cyberpsychosis — ✅ Done
- Спринт 13.5: Cyberpsychosis hooks + API endpoints + CORS + Documentation cleanup — ✅ Done
- Спринт 14: Web UI restructure + WebSocket streaming + Sound effects + SVG Heatmap — ✅ Done
- Спринт 15: Multi-user auth + World tab + Radar chart — ✅ Done
- Спринт 16: Canvas animations + IndexedDB offline + Labs drag-and-drop — ✅ Done
- Спринт 17: Enhanced PWA (SW v3, offline page) + Notifications + /api list — ✅ Done
- Спринт 18: Multi-user roles (admin/teacher/student) + Analytics dashboard + TWA — ✅ Done
- Спринт 19: Course management (teacher CRUD) + GDPR export/import + 18 auth tests — ✅ Done
- Спринт 20: Admin panel + WebSocket notifications + SCORM manifest — ✅ Done
