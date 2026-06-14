# Story Implementation Plan v2 (Lean)

## Философия

Сюжет — это **рамка**, а не второй режим. История оборачивает существующие эпизоды в нарратив, не требуя переписывать их. Механики добавляются только те, что усиливают обучение: последствия действий, таймеры, чистота следов.

**Цель:** заставить ученика хотеть вернуться, а не просто "добавить атмосферы".

---

## Этап 1 — Главы и нарратив (3-4 дня)

Группировка 20 существующих эпизодов в 6 глав. Создание обёртки `story_chapter.py`.

### Фичи:

| # | Что делаем | Файлы | Зачем |
|---|-----------|-------|-------|
| 1 | **6 глав вместо 20 эпизодов** | `story_mode.py` — STORY_EPISODES → CHAPTERS | Эпизоды 1–5 → Ch1, 6–10 → Ch2, 11–15 → Ch3, 16–18 → Ch4, 19–20 → Ch5, missions → Ch6 |
| 2 | **Chapter wrapper (intro/outro)** | `handlers/story_chapter.py` — новый | Каждая глава: intro-текст от учителя, цепочка эпизодов, outro-текст |
| 3 | **CLI + API для глав** | `handlers/story_chapter.py`, `api_server.py` | `/story chapter 1` — начать главу. Флаги в рамках главы |
| 4 | **State поля для глав** | `state.py` | `current_chapter: int`, `chapter_completed: list[int]`, `chapter_progress: dict` |
| 5 | **PWA: Chapter view** | `static/js/tabs/story.js` | Вкладка story: главы вместо эпизодов, прогресс по главам |

### Результат:
- Вместо 20 строк в списке — 6 глав с нарративом
- Каждая глава имеет intro/outro
- Всё старые эпизоды работают, просто сгруппированы

---

## Этап 2 — Риск-механики (4-5 дней)

Механики, которые добавляют вес действиям ученика.

### Фичи:

| # | Что делаем | Файлы | Зачем |
|---|-----------|-------|-------|
| 5 | **Noise Level** | `state.py` (+поле), `handlers/noise.py` (новый), CLI `/noise` | Шкала 0–100. Растёт от брутфорса/сканеров. Влияет на Watchers. Учит opsec |
| 6 | **Trace Timer** | `state.py`, `handlers/trace.py` (новый), API `/api/trace` | Таймер на отдельные лабы. Не успел → лаба заблокирована на N часов |
| 7 | **Dirty Logs** | `handlers/logs.py` (новый), CLI `/wipe_logs`, `/check_logs` | После лаб остаются логи. Надо чистить. Watchers видят грязные логи |
| 8 | **Debt System** | `state.py` (+поле), `handlers/debt.py` (новый), CLI `/debts` | Незакрытые эпизоды/лабы = долг. >5 → учитель «болеет» (меньше подсказок) |
| 9 | **PWA индикаторы** | `static/js/components/noise.js`, `static/js/components/trace.js`, `static/js/tabs/dashboard.js` | Шкала Noise, Progress bar Trace, счётчик Debt |

### Результат:
- Ученик думает: "тихо — чисто — безопасно" vs "громко — быстро — рискованно"
- Незакрытые задания давят морально, а не баллами
- Watchers реагируют на шум

---

## Этап 3 — Фракции и киберпсихоз (3-4 дня)

Выборы, которые влияют на историю, и атмосфера, которая затягивает.

### Фичи:

| # | Что делаем | Файлы | Зачем |
|---|-----------|-------|-------|
| 10 | **Faction Choice (Rick vs Ghost)** | `state.py` (+faction_reputation), `handlers/faction.py` (новый), CLI `/faction` | Выбор личности учителя влияет на стиль подсказок и доступные лабы |
| 11 | **Cyberpsychosis escalation** | `state.py` (risk_level → влияет на UI), event trigger | 3+ CP → глитчи в PWA. 5+ CP → учитель боится ученика |
| 12 | **Teacher Memory** | `handlers/memory.py` (новый), `state.py` (+memorable_events) | Учитель помнит действия ученика. *«Помнишь, как ты мучился с тем хешом?»* |
| 13 | **Echo Messages** | `handlers/echo.py` (новый), event trigger | Рандомные ghost-сообщения от прошлых студентов в чате |
| 14 | **Secret Phrases** | `handlers/secret_language.py` (новый), `handlers/chat.py` (апдейт) | *«Echo, помоги»* → подсказка. *«Rick, будь серьёзнее»* → меняет тон |
| 15 | **Final Choice (3 paths)** | `handlers/story_chapter.py` (апдейт), `api_server.py` | Глава 8: Память / Слияние / Перерождение |

### Результат:
- История реагирует на выборы ученика
- Чем глубже — тем страннее система
- Финал, который хочется пройти ещё раз

---

## Итого

| Этап | Фичи | Хендлеры | API | PWA | Время |
|------|------|----------|-----|-----|-------|
| 1. Главы | 4 | 1 новый | 2-3 | 1 апдейт | 3-4 дня |
| 2. Риск | 5 | 4 новых | 4-5 | 3 новых | 4-5 дней |
| 3. Фракции+CP | 6 | 4 новых | 3-4 | 1 апдейт | 3-4 дня |
| **Всего** | **15** | **9 новых** | **~10** | **~5** | **~10-14 дней** |

## Статус реализации (актуально на текущую сессию)

### ✅ ВЫПОЛНЕНО (за рамками оригинального плана)

| Компонент | Файлы | Описание |
|-----------|-------|----------|
| **Event Engine** | `handlers/event_engine.py`, `events/narrative_events.json` | 14 сюжетных событий с триггерами/условиями/эффектами |
| **PWA Narrative Events** | `static/js/notifications_ws.js` | WebSocket обработка events, фиолетовые баннеры |
| **Glitch.js** | `static/js/glitch.js` | 3AM Witching Hour + Debt Warning (депозиты ≥5) |
| **Behavior Profile** | `behavior_profile.py` | 6 скрытых черт, 6 архетипов, авто-детекция |
| **Persona Router** | `persona_router.py`, `handlers/core.py` | 4 персоны (Rick/Doc/Analyst/Ghost), авто-маршрутизация, `/persona` |
| **PWA Persona Voice Tags** | `api_server.py`, `static/js/tabs/chat.js` | REST/WebSocket возвращают persona info, индикатор в UI |
| **FAISS Batch Embedding** | `knowledge.py` | Оптимизация: нативный батчинг вместо per-document |
| **Backup Rotation** | `state.py`, `settings.py` | Ротация по количеству и возрасту бэкапов |

### ⏳ ИЗ ПЛАНА — ВЫПОЛНЕНО

| # | Фича | Статус |
|---|------|--------|
| 1 | 6 глав вместо 20 эпизодов | ✅ `story_mode.py` CHAPTERS + intro/outro |
| 2 | Chapter wrapper (intro/outro) | ✅ `routes/story.py` + `static/js/tabs/story.js` |
| 3 | CLI + API для глав | ✅ `/api/chapters`, `/api/chapter/start` |
| 4 | State поля для глав | ✅ `current_chapter`, `chapter_completed`, `chapter_progress` |
| 5 | PWA: Chapter view | ✅ вкладка story с прогрессом |
| 6 | Noise Level | ✅ `handlers/noise.py`, `/api/noise`, CLI `/noise` |
| 7 | Trace Timer | ✅ `handlers/trace.py`, `/api/trace` |
| 8 | Dirty Logs | ✅ `handlers/logs.py`, `/wipe_logs`, `/check_logs` |
| 9 | Debt System | ✅ `handlers/debt.py`, CLI `/debts`, блокировка подсказок при >5 |
| 10 | PWA Risk Indicators | ✅ `static/js/components/risk_indicators.js` (Noise, Trace, Debt) |
| 11 | Faction Choice | ✅ `handlers/faction.py`, репутация, влияет на подсказки/лабы |
| 12 | Cyberpsychosis | ✅ `cyberpsychosis.py`, 3 уровня, влияет на учителя |
| 13 | Teacher Memory | ✅ `handlers/memory.py`, `memorable_events` в state |
| 14 | Echo Messages | ✅ `handlers/echo.py`, рандомные ghost-сообщения |
| 15 | Final Choice (3 paths) | ✅ `story_mode.py` final_choice, 3 пути |

### ✅ ИЗ ПЛАНА — ВСЁ ВЫПОЛНЕНО

| # | Фича | Глава | Статус |
|---|------|-------|--------|
| 1 | **Ghost Log** (`/ghost_log`) | 1 | ✅ `handlers/ghost_log.py` + `handlers/misc.py`, 14 записей |
| 2 | **Backdoors** (`/backdoor list/remove`) | 5 | ✅ `handlers/backdoor.py`, 8 бэкдоров, деактивация |
| 3 | **Secret Phrases** интеграция | 5 | ✅ `handlers/secret_language.py` в CLI/REST/WS, 6 фраз |
| 4 | **Hidden Knowledge unlock** | 2-5 | ✅ `world_state.check_unlock_knowledge` в main loop, 5 знаний |
| 5 | **Teacher Sleep / 4am** | 7 | ✅ `state.py` + `handlers/misc.py`, `/teacher_sleep`, `/logs secret` |
| 6 | **World Stability** (0-100) | 7 | ✅ `state.world_stability`, авто-адаптация, `/stability` |
| 7 | **CP-based Glitches** | 7 | ✅ `glitch.js` + `/api/cyberpsychosis`, уровни 2-4 |

## Что НЕ делаем (вырезано)

| Из оригинального плана | Почему |
|------------------------|--------|
| Shadow Teacher | Одноразовый ивент, не стоит реализации |
| Digital Grave / Resurrection | 30 дней отсутствия — слишком нишево |
| Sacrifice (сброс профиля) | Слишком жестоко, оттолкнёт пользователей |
| Doppelganger | Архитектурно сложно, мало impact |
| Metronome / Audio | CLI не поддерживает звук, PWA — оверкилл |
| Ghost Shop | Микроменеджмент, раздражает |
| Forced Detox | Учит плохому — раздражает, а не воспитывает |
| Impostor Syndrome | Нечитаемо в русскоязычном контексте |
| System Sleep Paralysis | Раздражает, не вовлекает |
| Lost Episode | FOMO — вредно для образовательного продукта |

## Архитектура (реальная)

```
handlers/
  story_chapter.py      — 6 глав + intro/outro (в story_mode.py)
  noise.py              — уровень шумности + CLI /noise + /api/noise
  trace.py              — таймер трассировки + API /api/trace
  logs.py               — dirty logs + /wipe_logs, /check_logs
  debt.py               — цифровые долги + CLI /debts, блокировка hints
  faction.py            — репутация Rick/Ghost/Archive, влияет на hints/лабы
  memory.py             — персонализированная память учителя (memorable_events)
  echo.py               — ghost-сообщения от прошлых студентов
  secret_language.py    — тайные фразы (интегрирован в main.py + api_server.py, 6 фраз, CLI/REST/WS)
  event_engine.py       — сюжетные события (14 events, triggers/conditions/effects)
  ghost_log.py          — Ghost Log (14 записей, CLI `/ghost_log`, условия разблокировки по chapter/noise/debts/faction/CP/trace/stealth/memory)
  backdoor.py           — Backdoors (8 записей, CLI `/backdoor [list|info|remove|random]`, деактивация: Noise -5 + флаги, персистентность: cron/JWT/SSH/SQL trigger/systemd/FTP/MongoDB)
  persona_router.py     — динамические персоны (Rick/Doc/Analyst/Ghost)
  behavior_profile.py   — скрытые черты + архетипы
  cyberpsychosis.py     — CP escalation (stress/obsession/recklessness)
  mood.py               — 5 стилей общения
  watchers.py           — Watchers counterattack

state.py — ключевые поля:
  current_chapter, chapter_completed, chapter_progress
  noise_level, stealth_mode, stealth_mode_until
  trace_active, trace_deadline, trace_target
  digital_debts, debt_details, hint_enabled
  faction_chosen, faction_reputation
  memorable_events, earned_achievements
  behavior_profile (curiosity/recklessness/discipline/creativity/opsec/stress)
  preferred_persona, cp_level, risk_level
  secret_room_unlocked, secret_room_expires, truth_artifact

static/js/
  components/risk_indicators.js  — Noise bar, Trace progress, Debt counter
  glitch.js                       — 3AM Witching Hour + Debt Warning
  notifications_ws.js             — WebSocket: events + persona updates
  tabs/chat.js                    — Chat с persona indicator
```

## Связанные файлы

- `story/CHAPTERS.md` — краткое описание глав и механик
- `story/NARRATIVE.md` — полное сюжетное описание
- `story/archive/` — оригинальные lore-файлы (сохранены)
