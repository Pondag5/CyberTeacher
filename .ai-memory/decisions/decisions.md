# Decisions

## 2026-06-05
- **NUEMRIC_MENU расширен** до 0-72 (было 1-13). Все цифры из меню работают.
- **OSINT /api/threats** переписан: загрузка из threats/*.json вместо несуществующей APT_GROUPS.
- **.ai-memory/ заполнен** — все 8 файлов с актуальным контекстом.
- **Устаревшие .md документы** помечены.

## 2026-05-29 (Sprint 11-16)
- **ResilientLLM вместо прямого вызова** — fallback chain + retry + circuit breaker
- **Context Budget Manager** — token-aware trimming 4 chars/token
- **Memory Caps** — _trim_unbounded_lists() для всех растущих списков
- **MockLLM** — офлайн-режим без LLM, intent detection
- **Rule-based achievements** — achievement_service без LLM
- **Отвязка LLM от игровой механики** — прогресс/ачивки/очки работают офлайн
- **PWA через IndexedDB** — OfflineDB для кэширования API ответов
## 2026-06-09T21:53:57.536Z

Bullet list of durable decisions (write "None" if no notable decisions were made).

---

