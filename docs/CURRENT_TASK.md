# Текущая активная задача

Версия: **5.19**
Статус: **✅ Архитектурные фичи завершены / ⏳ Плановые механики (7 шт.)**
Последнее обновление: 2026-06-14

## Завершённые в этой сессии

| Компонент | Файлы | Описание |
|-----------|-------|----------|
| Event Engine | `handlers/event_engine.py`, `events/narrative_events.json` | 14 сюжетных событий, триггеры/условия/эффекты |
| PWA Narrative Events | `static/js/notifications_ws.js` | WebSocket events → purple banners |
| Glitch.js | `static/js/glitch.js` | 3AM Witching Hour + Debt Warning |
| Behavior Profile | `behavior_profile.py` | 6 черт, 6 архетипов, автодетекция |
| Persona Router | `persona_router.py`, `handlers/core.py`, `api_server.py` | 4 персоны, `/persona`, PWA voice tags |
| FAISS Batch Embedding | `knowledge.py` | Нативный батчинг эмбеддингов |
| Backup Rotation | `state.py`, `settings.py` | Ротация по count + age |
| Docs Sync | `docs/STORY_IMPLEMENTATION_PLAN.md` | Статусная таблица, архитектура |
| FAISS Rebuild | `index_project.py` | Исключены cves/, tests/ → 9 мин |

## Тесты
- **1207 passed**, 2 pre-existing failures, 8 skipped

---

## ⏳ Из плана STORY_IMPLEMENTATION_PLAN.md — НЕ СДЕЛАНО (0 механик)

| # | Механика | Глава | Приоритет |
|---|----------|-------|-----------|
| 1 | ✅ **Ghost Log** (`/ghost_log`) | 1 | High |
| 2 | ✅ **Backdoors** (`/backdoor list/remove`) | 5 | High |
| 3 | ✅ **Secret Phrases** integration | 5 | High |
| 4 | ✅ **Hidden Knowledge unlock** | 2-5 | High |
| 5 | ✅ **Teacher Sleep / 4am** | 7 | Medium |
| 6 | ✅ **World Stability** (0-100) | 7 | Medium |
| 7 | ✅ **CP-based Glitches** | 7 | Medium |

---

## P0 — Ручное действие
- [ ] Ротация API ключей (OpenRouter, HuggingFace, Groq)
- [ ] Настроить `CYBERTEACHER_JWT_SECRET` и `CYBERTEACHER_ENC_KEY` в `.env`

## P3 — Долгосрочные
- [ ] Mobile приложение (React Native / TWA)
- [ ] OAuth2 (Google, GitHub)
- [ ] 2FA (TOTP)

## ⏳ Оптимизация (выполнено: FAISS Watcher)

| Область | Статус |
|---------|--------|
| **FAISS Auto-reindex** | ✅ `faiss_watcher.py` + `/faiss_watch [start|status]` (watchdog, debounce 2с) |
| **DB** | Индексы, connection pooling |
| **WebSocket** | Connection pooling, auto-reconnect, message batching |
| **LLM** | Response caching, токен-бюджет |
| **PWA** | Service worker: stale-while-revalidate, offline queue |
| **MCP** | Кэширование поиска, parallel calls |
| **Static** | Brotli/gzip, CSP nonce |
| **CVE** | Фильтрация critical/high, дедуп |
| **Logs** | Structured JSON, rotation, Loki/Grafana |
