# Текущая активная задача

Версия: **6.0**
Статус: **✅ Архитектурные фичи завершены / ⏳ Плановые механики (3 шт.)**
Последнее обновление: 2026-09-18

## Завершённые в этой сессии

| Компонент | Файлы | Описание |
|-----------|-------|----------|
| Learning Memory System | `services/learning_memory_service.py`, `db.py`, `handlers/quiz.py`, `api_server.py`, `personality.py` | Долгосрочная память учителя в SQLite (`learning_events`), семантический retrieval по ошибкам, personality insights, запись ошибок из quiz |
| Knowledge Base Optimization | `knowledge.py` | Категоризация книг по названию, richer metadata, BM25 на полном корпусе, RRF fusion, query expansion, source/category фильтры, персистентный BM25 индекс |
| Alembic Migration | `migrations/versions/cb007d8d52d1_add_learning_events_table.py` | Миграция для `learning_events` |
| Personality Drift Extensions | `personality.py` | Параметры `weak_topics_count`, `recent_errors`, `recent_breakthroughs` |
| GitHub Repo Update | README.md, `gh` CLI | Описание, topics, README обновлены |

## Архитектурные фичи (всё завершено)

| Компонент | Файлы | Описание |
|-----------|-------|----------|
| Story Mode | `story_mode.py`, `handlers/event_engine.py` | 8 глав, 20+ эпизодов, финальный выбор 3 путей |
| Risk Mechanics | `handlers/noise.py`, `handlers/trace.py`, `handlers/debt.py`, `handlers/logs.py` | Noise/Trace/Debt/Stealth |
| Factions + Reputation | `handlers/faction.py` | Rick/Ghost/Archive |
| Cyberpsychosis | `cyberpsychosis.py`, `static/js/glitch.js` | 4 уровня, PWA глитчи |
| Echo Messages | `handlers/echo.py` | Ghost-сообщения прошлых студентов |
| Teacher Memory | `handlers/memory.py`, `services/learning_memory_service.py` | Learning events + semantic retrieval |
| Watchers Counterattack | `handlers/watchers.py` | |
| Phantom Labs | `handlers/phantom_lab.py` | |
| Secret Room | `handlers/secret_room.py` | |
| Rewind / Time Machine | `handlers/rewind.py` | |
| Spaced Repetition (SM-2) | `services/spaced_repetition_service.py` | |
| Weak Topics Auto-tracking | `services/weak_topics_service.py` | |
| FAISS + BM25 + Cross-encoder RAG | `knowledge.py`, `index_project.py` | Гибридный поиск |
| State Save Throttling | `state.py` | Debounced save 2s |
| Mood / Persona System | `handlers/mood.py`, `persona_router.py` | 5 режимов, 5 настроений |
| Behavior Profile + Archetypes | `behavior_profile.py` | 6 черт, 6 архетипов |
| Push Notifications (VAPID) | `handlers/push_notifications.py` | |
| Backdoors | `handlers/backdoor.py` | |
| Ghost Log | `handlers/ghost_log.py` | |
| Secret Phrases | `handlers/secret_language.py` | |
| FAISS Auto-Reindex Watcher | `faiss_watcher.py` | |
| Multi-user Auth / Roles / Admin Panel / GDPR / SCORM | `auth.py`, `api_server.py` | |
| Service Worker, OfflineDB, WebSocket | `static/sw.js`, `static/js/offline.js`, `api_server.py` | |
| Launcher (tkinter GUI) | `launcher.py`, `scripts/launcher.py` | |

## Тесты
- **105+ passed** в ключевых модулях (knowledge, quiz, mood, persona, memory, services)
- Полный запуск всего тестового набора требует больше времени из-за импорта моделей

---

## ⏳ STORY_IMPLEMENTATION_PLAN.md — все 15/15 механик завершены

| # | Механика | Глава | Статус |
|---|----------|-------|--------|
| 1 | Ghost Log (`/ghost_log`) | 1 | ✅ |
| 2 | Backdoors (`/backdoor list/remove`) | 5 | ✅ |
| 3 | Secret Phrases integration | 5 | ✅ |
| 4 | Hidden Knowledge unlock | 2-5 | ✅ |
| 5 | Teacher Sleep / 4am | 7 | ✅ |
| 6 | World Stability (0-100) | 7 | ✅ |
| 7 | CP-based Glitches | 7 | ✅ |
| 8 | Watchers Counterattack | — | ✅ |
| 9 | Phantom Labs | — | ✅ |
| 10 | Secret Room | — | ✅ |
| 11 | Rewind / Time Machine | — | ✅ |
| 12 | Echo Messages | — | ✅ |
| 13 | Teacher Memory (learning events) | — | ✅ |
| 14 | Factions + Reputation | — | ✅ |
| 15 | Final Choice (3 paths) | — | ✅ |

---

## P0 — Выполнено
- [x] Ротация API ключей (OpenRouter, HuggingFace, Groq) — `/keys rotate <provider>`
- [x] Настроить `CYBERTEACHER_JWT_SECRET` и `CYBERTEACHER_ENC_KEY` в `.env` — уже заданы
- [x] Rate Limiting → token bucket — `api_server.py`

## P1 — Выполнено
- [x] `handlers/quiz.py` — интерактивный ввод кода + LLM анализ
- [x] `handlers/hints.py` — mission-based hint
- [x] `news_fetcher.py` — XMLParsedAsHTMLWarning исправлен

## P3 — Долгосрочные
- [ ] Mobile приложение (React Native / TWA)
- [ ] OAuth2 (Google, GitHub)
- [ ] 2FA (TOTP)

## ⏳ Оптимизация (в процессе)

| Область | Статус |
|---------|--------|
| **FAISS Auto-reindex** | ✅ `faiss_watcher.py` + `/faiss_watch [start|status]` |
| **DB** | ✅ Индексы, connection pooling |
| **WebSocket** | ✅ Connection pooling, auto-reconnect, broadcast, `/api/ws/stats` |
| **LLM** | ✅ Response caching, токен-бюджет, prompt compression |
| **PWA** | ✅ Service worker: stale-while-revalidate, offline queue |
| **Knowledge Base** | ✅ Категоризация, BM25 full-corpus, RRF, query expansion |
| **Learning Memory** | ✅ SQLite + semantic retrieval, personality drift |
| **CVE** | ✅ Фильтрация critical/high, дедуп |
| **Logs** | ✅ Structured JSON, rotation |
