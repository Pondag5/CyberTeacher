# CyberTeacher — Ideas Status

*Last updated: 2026-09-18*

Единый источник истины для всех идей, фич и планов проекта. Каждая идея отслеживается здесь со статусом и ссылками на код/документы.

---

## Легенда

| Статус | Описание |
|--------|----------|
| ✅ Done | Реализовано и работает |
| ⏳ Partial | Частично реализовано, требует доработки |
| 🔄 In Progress | В работе |
| 📋 Planned | Запланировано, не начато |
| ❌ Cut | Намеренно исключено |
| 🗂️ Deprecated | Устарело, не актуально |

---

## Vision Ideas (`docs/cyberteacher_vision_ideas_masterfile.md`)

| ID | Idea | Status | Where |
|----|------|--------|-------|
| V1 | Personality drift (sarcasm, patience, paranoia, enthusiasm, formality) | ✅ Done | `personality.py`, `handlers/mood.py`, `persona_router.py` |
| V2 | Behavioral archetypes (Analyst, Researcher, Script Kiddie, Engineer, Ghost Operator, Chaotic Hacker) | ✅ Done | `behavior_profile.py` |
| V3 | Cyberpsychosis 4 stages (subtle → major corruption) | ✅ Done | `cyberpsychosis.py`, `static/js/glitch.js` |
| V4 | Fake OS integration (daemon messages, hidden logs) | ⏳ Partial | `handlers/ghost_log.py`, `static/js/notifications_ws.js` |
| V5 | Memory layers (episodic, personality, story) with importance scoring | ⏳ Partial | `handlers/memory.py`, `services/learning_memory_service.py` |
| V6 | Hybrid LLM (local primary 95%, cloud heavy reasoning 5%) | ⏳ Partial | `config.py` ResilientLLM — сейчас cloud-first, local fallback |
| V7 | Local model primary (Qwen2.5 7B via Ollama/LM Studio) | 📋 Planned | Архитектура поддерживает, но default cloud |
| V8 | Context Controller (token budget, retrieval, summarization) | ✅ Done | `context_budget.py` |
| V9 | Dynamic UI mood per persona | ⏳ Partial | `static/js/themes.js`, persona tags в `api_server.py` |
| V10 | Persistent world dashboard (active incidents) | ⏳ Partial | `world_state.py` — дашборд не fully реализован |
| V11 | Late-night hacker mode (3AM, fatigue warnings) | ✅ Done | `static/js/glitch.js` 3AM triggers |
| V12 | Pseudo multi-agent via persona routing | ✅ Done | `persona_router.py` (Rick/Doc/Analyst/Ghost) |
| V13 | Hidden knowledge layer (topics locked behind gates) | ✅ Done | `handlers/secret_room.py`, `handlers/backdoor.py` |
| V14 | Reputation/faction system with persistent state | ✅ Done | `handlers/faction.py` |
| V15 | Echo messages from past students | ✅ Done | `handlers/echo.py` |
| V16 | Teacher memory with personalized references | ✅ Done | `handlers/memory.py`, `services/learning_memory_service.py` |
| V17 | Rewind/timeloop mechanic | ✅ Done | `handlers/rewind.py`, `handlers/timeloop.py` |
| V18 | Spaced Repetition (SM-2) | ✅ Done | `services/spaced_repetition_service.py` |
| V19 | Weak topics auto-tracking | ✅ Done | `services/weak_topics_service.py` |
| V20 | State save throttling (2s debounce) | ✅ Done | `state.py` |

---

## Story Mechanics (`docs/STORY_IMPLEMENTATION_PLAN.md`, `story/CHAPTERS.md`)

| ID | Mechanic | Chapter | Status | Where |
|----|----------|---------|--------|-------|
| S1 | Ghost Log (`/ghost_log`) | 1 | ✅ Done | `handlers/ghost_log.py` |
| S2 | Backdoors (`/backdoor`) | 5 | ✅ Done | `handlers/backdoor.py` |
| S3 | Secret Phrases | 5 | ✅ Done | `handlers/secret_language.py` |
| S4 | Hidden Knowledge unlock | 2-5 | ✅ Done | `handlers/secret_room.py` |
| S5 | Teacher Sleep / 4am | 7 | ✅ Done | `handlers/misc.py` |
| S6 | World Stability (0-100) | 7 | ✅ Done | `state.py`, `world_state.py` |
| S7 | CP-based Glitches | 7 | ✅ Done | `cyberpsychosis.py`, `glitch.js` |
| S8 | Watchers Counterattack | — | ✅ Done | `handlers/watchers.py` |
| S9 | Phantom Labs | — | ✅ Done | `handlers/phantom_lab.py` |
| S10 | Secret Room | — | ✅ Done | `handlers/secret_room.py` |
| S11 | Rewind / Time Machine | — | ✅ Done | `handlers/rewind.py` |
| S12 | Echo Messages | — | ✅ Done | `handlers/echo.py` |
| S13 | Teacher Memory (learning events) | — | ✅ Done | `services/learning_memory_service.py` |
| S14 | Factions + Reputation | — | ✅ Done | `handlers/faction.py` |
| S15 | Final Choice (3 paths) | — | ✅ Done | `story_mode.py` |
| S16 | Debt System | — | ✅ Done | `handlers/debt.py`, `state.py` |
| S17 | Event Engine (14 narrative events) | — | ✅ Done | `handlers/event_engine.py` |
| S18 | Rescue Missions | 6 | ⏳ Partial | `handlers/missions.py` — exists, narrative chain needs verification |
| S19 | `node_key.enc` blinking inventory item | 2 | 📋 Planned | Not fully implemented as described |

**Cut items (intentionally excluded):**
- ❌ Shadow Teacher
- ❌ Digital Grave
- ❌ Sacrifice / 4th path
- ❌ Doppelganger
- ❌ Metronome
- ❌ Ghost Shop
- ❌ Forced Detox
- ❌ Impostor Syndrome
- ❌ System Sleep Paralysis
- ❌ Lost Episode

---

## New Features (`docs/new_features.md`)

| ID | Feature | Status | Where |
|----|---------|--------|-------|
| NF1 | Debt System | ✅ Done | `handlers/debt.py` |
| NF2 | Phantom Messages | ✅ Done | `handlers/phantom_messages.py`, `handlers/phantom_lab.py` |
| NF3 | Non-linear Story Events | ✅ Done | `handlers/event_engine.py`, `events/narrative_events.json` |
| NF4 | Glitch.js extensions | ⏳ Partial | `static/js/glitch.js` — `fake_camera_request` not implemented |
| NF5 | Push Notifications | ✅ Done | `handlers/push_notifications.py` |
| NF6 | Final Exam Ritual (3 endings) | ✅ Done | `story_mode.py` |

---

## Netbuk Plans (`docs/IDEAS_FOR_NETBUK.md`)

| ID | Plan | Status | Notes |
|----|------|--------|-------|
| NB1 | Docker Labs Host | 📋 Planned | SSH host, docker-compose templates |
| NB2 | LXC Network Sandbox | 📋 Planned | attacker/victim/router |
| NB3 | Red Team Target | 📋 Planned | Vulnerable services |
| NB4 | WiFi Range (hostapd + aircrack-ng) | 📋 Planned | |
| NB5 | SIEM/Log Collector | 📋 Planned | rsyslog + Loki/Grafana |
| NB6 | CTFd Platform | 📋 Planned | API integration |
| NB7 | Gophish Phishing | 📋 Planned | Campaigns, templates |
| NB8 | Anomaly Generator + Honeypot | 📋 Planned | Cowrie/Dionaea + hping3/nmap |

---

## Platform / Long-term (`docs/FEATURES_PLANNED.md`, `docs/ROADMAP.md`, `docs/план релиза.md`)

| ID | Feature | Status | Effort | Dependencies |
|----|---------|--------|--------|--------------|
| P3-1 | Mobile App (React Native / TWA) | 📋 Planned | 2-4 weeks | PWA ready |
| P3-2 | OAuth2 (Google, GitHub) | 📋 Planned | 1-2 weeks | auth.py, JWT |
| P3-3 | 2FA (TOTP) | 📋 Planned | 1 week | auth.py, pyotp |
| P3-4 | Multi-user Auth (Roles) | 📋 Planned | 1 week | auth.py, JWT |
| P3-5 | Admin Panel | 📋 Planned | 1 week | JWT, roles |
| P3-6 | GDPR Export/Import | 📋 Planned | 3 days | |
| P3-7 | SCORM Export | 📋 Planned | 2 days | `course_manager.py` |
| P2-1 | DB Indexes + Connection Pooling | 📋 Planned | 1-2d | SQLAlchemy |
| P2-2 | WebSocket Pooling + Auto-reconnect | 📋 Planned | 2-3d | `api_server.py` |
| P2-3 | LLM Response Caching (SQLite TTL + LRU) | 📋 Planned | 2-3d | `config.py` |
| P2-4 | PWA SW stale-while-revalidate | 📋 Planned | 2-3d | `static/sw.js` |
| P2-5 | Portable .exe build (PyInstaller) | 📋 Planned | 1-2d | PyInstaller |
| P0-1 | API Keys Rotation (manual) | 📋 Planned | 1-2d | `/keys rotate` |
| P0-2 | JWT_SECRET + ENC_KEY hardening | 📋 Planned | 1h | `.env` |
| P0-3 | Rate Limiting token bucket | 📋 Planned | 1-2d | `api_server.py` |

---

## Deprecated / Outdated Documents

| Document | Status | Notes |
|----------|--------|-------|
| `docs/WEB_VERSION.md` | 🗂️ Deprecated | Дата 2026-05-29, описывает PWA как заглушку 132 строки. Реально PWA — 58 табов, ~140 API. Не отражает текущее состояние. |
| `docs/roadmap/` | 🗂️ Empty | Пустая директория, roadmap находится в `docs/ROADMAP.md` |
| `docs/план релиза.md` | ⚠️ Stale | Все этапы 1-11 отмечены ✅, но не отражает текущий бэклог P1/P2/P3 |

---

## Architecture / ADR (`docs/adr/`)

| ADR | Title | Status |
|-----|-------|--------|
| 0001 | LazyLoader for LLM/embeddings | ✅ Implemented |
| 0002 | Hybrid RAG (FAISS + BM25 + RRF) | ✅ Implemented |
| 0003 | LLM Caching (SQLite + TTL) | ✅ Implemented |
| 0004 | Singleton AppState via `get_state()` | ✅ Implemented |
| 0005 | Rate Limiting (sliding window) | ✅ Implemented |

---

## Key Insights

1. **Vision → Code alignment**: 80%+ идей из masterfile реализованы, но часто в другой форме, чем описано
2. **Biggest gap**: Netbuk plans — 0% реализации, но это инфраструктура, а не софт
3. **Biggest opportunity**: Memory layers + importance scoring — если доделать, это УТП проекта
4. **Biggest risk**: Файлы с идеями разрознены и устаревают; этот документ (`IDEAS_STATUS.md`) должен стать единым источником истины
5. **Deprecated docs**: `WEB_VERSION.md` и `docs/roadmap/` путают newcomers; их нужно или обновить, или удалить

---

*This file is the master index for all ideas. Update it when implementing new features or changing plans.*
