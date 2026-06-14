# CyberTeacher — Полное описание для веб-реализации

*Версия: 5.2 | Дата: 2026-05-29*

---

## 1. Обзор проекта

CyberTeacher — AI-наставник по кибербезопасности. Работает как CLI (Rich + prompt_toolkit), PWA-компаньон, REST API (FastAPI). **100+ CLI-команд**, **57 API-эндпоинтов**, **150+ функций**.

**Цель веб-реализации:** Полноценный SPA, заменяющий CLI и текущий PWA-заглушку, с подключением к существующему backend API.

---

## 2. Архитектура

```
┌─────────────────────────────────────────────────┐
│                   Frontend (SPA)                │
│  React/Vue/Svelte + TypeScript                 │
│  18 вкладок · 3 темы · i18n ru/en              │
├─────────────────────────────────────────────────┤
│               REST API (FastAPI)                │
│  57 эндпоинтов · CORS · без auth               │
├─────────────────────────────────────────────────┤
│              Backend Services                   │
│  State (Pydantic) · LLM (ResilientLLM)         │
│  RAG (Chroma+BM25) · Memory (SQLite)           │
│  Context Budget · Personality Drift             │
├─────────────────────────────────────────────────┤
│              Data Layer                         │
│  SQLite/PostgreSQL · FAISS · JSON state         │
└─────────────────────────────────────────────────┘
```

---

## 3. API Endpoints (полная таблица)

### 3.1 GET Endpoints (31)

| # | Path | Response | Описание |
|---|------|----------|----------|
| 1 | `/health_check` | `{status, timestamp}` | Health status |
| 2 | `/get_progress` | `{xp, level, reputation, current_course, current_topic, streak}` | Прогресс |
| 3 | `/get_achievements` | `{achievements: [...]}` | Достижения пользователя |
| 4 | `/get_achievements_list` | `{achievements: [...], total}` | Каталог всех достижений (29) |
| 5 | `/get_weak_topics` | `{weak_topics: [...]}` | Слабые темы |
| 6 | `/get_courses` | `{courses: [{id, name, desc, icon, topics_count, duration, progress, active}]}` | Список курсов (6) |
| 7 | `/get_labs` | `{labs: [{id, name, desc, image, ports, tags, running, difficulty}]}` | Docker-лабы (21) |
| 8 | `/docker_status` | `{available, message}` | Статус Docker |
| 9 | `/docker_containers` | `{containers: [{name, status, ports}]}` | Запущенные контейнеры |
| 10 | `/get_detailed_stats` | `{xp, level, xp_needed, xp_progress, streak, total_quizzes, total_tasks, weak_topics, activity, skills}` | Детальная статистика |
| 11 | `/get_versus_scenarios` | `{scenarios: [{id, name, desc}]}` | Сценарии дуэли (4) |
| 12 | `/versus_status` | `{active, scenario, attempts, history_length}` | Статус дуэли |
| 13 | `/get_scan_rules` | `{rules, owasp_categories, rules_dir}` | Правила сканирования |
| 14 | `/get_modes` | `{modes: [{name, icon, desc, id, active}], current}` | Режимы обучения (6) |
| 15 | `/get_profile` | `{name, avatar, xp, level, streak, reputation, points, flags_captured, quizzes_taken, labs_started}` | Профиль |
| 16 | `/get_daily_challenge` | `{id, question, answer, category, difficulty, completed, date, streak}` | Дейли-челлендж |
| 17 | `/get_skills` | `{skills: [{id, name, xp, level}]}` | Навыки |
| 18 | `/get_shop` | `{items: [...], discount}` | Магазин (17 товаров) |
| 19 | `/get_heatmap` | `{heatmap: [{date, count}]}` | Тепловая карта (28 дней) |
| 20 | `/get_history?limit=50` | `{history: [...]}` | История чата |
| 21 | `/get_config` | `{llm_provider, model, language, theme, depth, offline_mode}` | Конфигурация |
| 22 | `/get_writeups` | `{writeups: [{name, date}]}` | Writeup'ы |
| 23 | `/get_story_episodes` | `{episodes: [{id, title, desc, category, difficulty, xp, completed}]}` | Story mode (21 эпизод) |
| 24 | `/get_tracks` | `{tracks: [{id, name, desc, level, estimated_hours, topics_count, topics, progress, prerequisites}]}` | Учебные треки (4) |
| 25 | `/get_ctf_status` | `{flags_captured, risk_level, ctf_active}` | CTF статус |
| 26 | `/get_missions` | `{missions: [{id, name, desc, difficulty, completed}]}` | Миссии |
| 27 | `/get_threats` | `{threats: [{id, name, country, targets, desc}]}` | APT группировки (27) |
| 28 | `/get_cve?cve_id=CVE-XXX` | `{cve: {...}}` | CVE lookup |
| 29 | `/get_news` | `{news: [...]}` | Новости кибербезопасности |
| 30 | `/get_offline_status` | `{offline_mode}` | Оффлайн-режим |
| 31 | `/get_scan_rules` | `{rules, owasp_categories}` | Правила сканирования |

### 3.2 POST Endpoints (26)

| # | Path | Request Body | Response | Описание |
|---|------|-------------|----------|----------|
| 32 | `/set_offline_status?action=toggle` | — | `{offline_mode, action}` | Переключить оффлайн |
| 33 | `/select_course?course_id=X` | — | `{status, course}` | Выбрать курс |
| 34 | `/submit_quiz_result` | `{topic, score, total}` | `{status, topic, score}` | Результат квиза |
| 35 | `/chat_with_llm` | `{message, history: []}` | `{response, history}` | Чат с LLM |
| 36 | `/generate_quiz` | `{topic, count}` | `{questions: [{question, options, correct, explanation}]}` | Генерация квиза |
| 37 | `/start_lab?lab_id=X` | — | `{status, lab, container_id, ports, message}` | Запуск лабы |
| 38 | `/stop_lab?lab_id=X` | — | `{status, lab, message}` | Остановка лабы |
| 39 | `/docker_start_lab?lab_id=X` | — | `{status, lab, container_id, ports, message}` | Docker запуск |
| 40 | `/docker_stop_lab?lab_id=X` | — | `{status, lab, message}` | Docker остановка |
| 41 | `/start_versus` | `{scenario}` | `{status, scenario, name, initial_message}` | Начать дуэль |
| 42 | `/versus_move` | `{message}` | `{response, attempts}` | Ход в дуэли |
| 43 | `/stop_versus` | — | `{status, message}` | Завершить дуэль |
| 44 | `/scan_code` | `{code, language, options: {use_semgrep, ci_mode}}` | `{status, results: {language, findings, severity_counts, owasp_summary}}` | Сканирование кода |
| 45 | `/set_mode?mode_id=X` | — | `{status, mode, name}` | Сменить режим |
| 46 | `/update_profile` | `{name, avatar}` | `{status}` | Обновить профиль |
| 47 | `/submit_daily_challenge?answer=X` | — | `{correct, answer, explanation, xp_earned}` | Ответ на дейли |
| 48 | `/purchase_item?item_id=X` | — | `{status, item, price}` | Купить товар |
| 49 | `/start_story_episode?episode_id=X` | — | `{status, episode, prompt}` | Начать эпизод |
| 50 | `/submit_story_answer?answer=X` | — | `{correct, xp_earned, hint}` | Ответ story |
| 51 | `/start_track?track_id=X` | — | `{status, track}` | Начать трек |
| 52 | `/update_track_progress?track_id=X&progress=N` | — | `{status, track, progress}` | Прогресс трека |
| 53 | `/submit_flag?flag_value=X` | — | `{correct, xp_earned, message}` | Отправить флаг |
| 54 | `/start_mission?mission_id=X` | — | `{status, mission}` | Начать миссию |
| 55 | `/scan_code_simple?code=X&language=python` | `{findings, severity_counts}` | Простое сканирование |
| 56 | `/analyze_malware?file_hash=X` | — | `{analysis}` | Анализ малвари |

---

## 4. Состояние пользователя (AppState — 80+ полей)

### 4.1 Прогресс и достижения

| Поле | Тип | Описание |
|------|-----|----------|
| `xp` | `float` | Очки опыта |
| `level` | `int` | Уровень |
| `points` | `float` | Общие баллы |
| `total_flags_collected` | `int` | Собранные флаги |
| `assignments_completed` | `int` | Выполненные задания |
| `labs_started` | `int` | Запущенные лабы |
| `quizzes_taken` | `int` | Пройденные квизы |
| `news_checked` | `int` | Прочитанные новости |
| `messages_sent` | `int` | Отправленные сообщения |
| `social_success` | `int` | Успешные соц.инженерии |
| `apt_groups_viewed` | `int` | Просмотренные APT |
| `stealth_ops` | `int` | Stealth операции |
| `threat_exposures` | `int` | Столкновения с угрозами |
| `earned_achievements` | `List[str]` | ID заработанных ачивок |
| `reputation` | `int` | Репутация |
| `handle` | `str` | Ранг (Новичок→Фантом) |

### 4.2 Курсы и обучение

| Поле | Тип | Описание |
|------|-----|----------|
| `current_course` | `Optional[str]` | Активный курс |
| `current_topic` | `int` | Индекс текущей темы |
| `course_progress` | `Dict[str, int]` | Прогресс по курсам |
| `current_track` | `Optional[str]` | Активный трек |
| `tracks_enrolled` | `List[str]` | Записанные треки |
| `track_progress` | `Dict[str, Any]` | Прогресс треков |

### 4.3 Навыки и слабые темы

| Поле | Тип | Описание |
|------|-----|----------|
| `skills` | `Dict[str, Any]` | `{skill_id: {xp, level, attempts, successes}}` |
| `weak_topics` | `List[Dict]` | `[{topic, attempts, total_score, max_score, success_rate}]` |

### 4.4 Магазин и кастомизация

| Поле | Тип | Описание |
|------|-----|----------|
| `owned_themes` | `List[str]` | Купленные темы |
| `current_theme` | `str` | Активная тема |
| `unlocked_topics` | `List[str]` | Разблокированные темы |
| `selected_tools` | `List[str]` | Выбранные инструменты |
| `purchase_history` | `List[Dict]` | История покупок (cap 100) |

### 4.5 CTF, миссии, эксплойты

| Поле | Тип | Описание |
|------|-----|----------|
| `risk_level` | `int` | Уровень риска (0-100) |
| `missions_completed` | `List[str]` | Завершённые миссии |
| `active_mission` | `Optional[str]` | Текущая миссия |
| `exploit_success` | `List[Dict]` | Успешные эксплойты (cap 200) |
| `ctf_flags_generated` | `int` | Сгенерированные флаги |
| `active_assignment` | `Optional[Dict]` | Текущее задание |

### 4.6 Story mode

| Поле | Тип | Описание |
|------|-----|----------|
| `story_completed` | `List[int]` | Завершённые эпизоды |
| `current_story_episode` | `Optional[int]` | Текущий эпизод |

### 4.7 Интеграции (HTB/THM)

| Поле | Тип | Описание |
|------|-----|----------|
| `htb_token` | `Optional[str]` | HTB API токен |
| `htb_completed` | `List[int]` | Завершённые HTB (cap 100) |
| `thm_username` | `Optional[str]` | THM имя пользователя |
| `thm_completed` | `List[Dict]` | Завершённые THM комнаты (cap 100) |
| `thm_points` | `int` | THM баллы |
| `thm_level` | `int` | THM уровень |

### 4.8 LLM и аналитика

| Поле | Тип | Описание |
|------|-----|----------|
| `llm_call_count` | `int` | Количество LLM вызовов |
| `llm_total_tokens` | `int` | Потраченные токены |
| `cache_hits` | `int` | Попадания кэша |
| `cache_misses` | `int` | Промахи кэша |
| `command_usage` | `Dict[str, int]` | Статистика команд (cap 50) |
| `request_timestamps` | `List[float]` | Rate limiting |

### 4.9 Lичность и атмосфера

| Поле | Тип | Описание |
|------|-----|----------|
| `_current_mode` | `str` | Режим: teacher/expert/ctf/review/hybrid |
| `_current_persona` | `str` | Персона |
| `communication_mood` | `str` | Стиль общения |
| `emotion_mode` | `str` | Эмоции: neutral/happy/angry/sarcastic |
| `language` | `str` | Язык: ru/en |
| `explanation_depth` | `str` | Глубина: beginner/normal/expert |

### 4.10 Остальное

| Поле | Тип | Описание |
|------|-----|----------|
| `daily_streak` | `int` | Серия дневных входов |
| `daily_completed` | `bool` | Дейли выполнен сегодня |
| `last_daily_date` | `str` | Дата последнего дейли |
| `hint_credits` | `int` | Кредиты подсказок |
| `voice_enabled` | `bool` | TTS включён |
| `feature_flags` | `Dict[str, bool]` | Флаги возможностей |
| `found_evidence` | `List[str]` | Улики (расследования) |
| `current_case` | `Optional[str]` | Текущее расследование |
| `versus_active` | `bool` | Дуэль активна |
| `versus_history` | `List[Dict]` | История дуэлей (cap 50) |

---

## 5. SQLAlchemy модели (15 таблиц)

| Таблица | PK | Ключевые поля | Назначение |
|---------|----|---------------|------------|
| `messages` | `id` | role, content, timestamp, mode | История чата |
| `stats` | `id` | points, quizzes_passed, tasks_solved | Агрегированная статистика |
| `progress` | `topic` (UNIQUE) | correct, total, last_seen | Прогресс по темам |
| `query_cache` | `query_hash` (UNIQUE) | response, expires_at, ttl_seconds | Кэш LLM ответов |
| `achievements` | `id` | achievement_id (UNIQUE), name, earned | Достижения |
| `skills` | `id` | skill_id (UNIQUE), name, xp, level | Навыки |
| `flags` | `id` | flag_value (UNIQUE), captured | CTF флаги |
| `writeups` | `id` | title, content, tags | Writeup'ы |
| `daily_challenges` | `id` | date (UNIQUE), question, answer | Дейли-челленджи |
| `exploit_log` | `id` | cve_id, target, success, details | Лог эксплойтов |
| `purchase_history` | `id` | item_id, item_name, price | История покупок |
| `command_heatmap` | `id` | date, command, count | Тепловая карта |
| `review_schedule` | `id` | topic, ease_factor, interval, next_review | SM-2 повторения |
| `session_summaries` | `id` | start_time, end_time, duration_minutes, xp_earned | Сессии |
| `app_state` | `id` | user_id (INDEXED), state_data (JSON), version | Полное состояние |

---

## 6. PWA вкладки (18 — текущая архитектура)

| # | Вкладка | Иконка | API вызовы |
|---|---------|--------|------------|
| 1 | Режимы | 🎭 | `get_modes`, `set_mode` |
| 2 | Чат | 💬 | `chat_with_llm`, `get_history` |
| 3 | Прогресс | 📊 | `get_progress`, `get_detailed_stats`, `get_heatmap` |
| 4 | Квизы | 📝 | `generate_quiz`, `submit_quiz_result` |
| 5 | Дейли | 🎯 | `get_daily_challenge`, `submit_daily_challenge` |
| 6 | Профиль | 👤 | `get_profile`, `update_profile` |
| 7 | Курсы | 📚 | `get_courses`, `select_course` |
| 8 | История | 📖 | `get_story_episodes`, `start_story_episode`, `submit_story_answer` |
| 9 | Треки | 🛤️ | `get_tracks`, `start_track`, `update_track_progress` |
| 10 | CTF | 🚩 | `get_ctf_status`, `submit_flag` |
| 11 | Лабы | 🐳 | `get_labs`, `start_lab`, `stop_lab`, `docker_containers` |
| 12 | OSINT | 🔍 | `get_threats`, `get_cve`, `get_news` |
| 13 | Сканер | 💻 | `scan_code`, `get_scan_rules` |
| 14 | Магазин | 🛒 | `get_shop`, `purchase_item` |
| 15 | Malware | 🦠 | `analyze_malware` |
| 16 | Достижения | 🏆 | `get_achievements`, `get_achievements_list` |
| 17 | Дуэль | 🥊 | `get_versus_scenarios`, `start_versus`, `versus_move`, `stop_versus` |
| 18 | Статистика | 📈 | `get_detailed_stats`, `get_heatmap`, `get_skills` |

---

## 7. Дизайн-система

### 7.1 Цвета (3 темы)

**Ocean (по умолчанию):**
- Фон: `#1e1e2e`, Карточки: `#2a2a3c`, Акцент: `#00B4D8`, Текст: `#e0e0e0`

**Sunset:**
- Фон: `#1a1025`, Карточки: `#2d1f3d`, Акцент: `#FF6A00`, Вторичный: `#9D4EDD`

**Matrix:**
- Фон: `#0d0d0d`, Карточки: `#1a1a1a`, Акцент: `#00FF41`, Вторичный: `#00CC33`

### 7.2 Типографика
- Основной: Inter (UI)
- Моноширинный: Fira Code (код, терминал)

### 7.3 Компоненты
- Карточки с `border-radius: 12px`, `box-shadow`
- Кнопки с `border-radius: 8px`, hover-эффекты
- Адаптив: max-width 1200px (desktop), 100% (mobile)
- Неоновые glow-эффекты на акцентных элементах

---

## 8. Текущее состояние PWA (проблемы)

Текущий PWA в `web/pwa/` — **заглушка**:
- 1 файл `index.html` (inline CSS + JS, 132 строки)
- 3 hardcoded вопроса квиза, нет API-вызовов
- Нет state persistence (теряется при перезагрузке)
- Нет навигации/вкладок
- Нет иконок (manifest ссылается на отсутствующие файлы)
- Service Worker готов к кэшированию `/api/*`, но фронтенд не делает fetch()

**Нужно:** Полная пересборка SPA.

---

## 9. Требования к веб-реализации

### 9.1 Фронтенд
- **Framework:** React/Vue/Svelte (на выбор)
- **State management:** Zustand/Pinia/Svelte Store
- **Роутинг:** Tab-based (18 вкладок)
- **HTTP клиент:** fetch/axios с автоматическим retry
- **Стили:** CSS Modules/Tailwind/CSS-in-JS
- **i18n:** ru/en через API `get_config`
- **Темы:** 3 темы, переключение через `set_theme` state field
- **Адаптив:** Mobile-first (600px → 1200px)
- **Offline:** Service Worker (уже готов), IndexedDB для state

### 9.2 Бэкенд (уже готов, доработки)
- **CORS:** Добавить `CORSMiddleware` в FastAPI
- **Auth:** Опционально (JWT/API key)
- **WebSocket:** Для стриминга LLM ответов (сейчас polling)
- **Новые эндпоинты:**
  - `GET /api/personality` — текущие personality modifiers
  - `GET /api/context` — контекст (время суток, паттерн)
  - `GET /api/world` — persistent world state (incidents, factions)
  - `GET /api/episodes` — episode memory

### 9.3 Критичные UX-паттерны
- **Chat:** Стриминг ответов (chunk by chunk), markdown рендеринг, код-блоки
- **Quiz:** Анимация вопрос→ответ, прогресс-бар, sound effects
- **Labs:** Статус контейнеров в реальном времени (polling 5s)
- **Heatmap:** SVG/Canvas 28-дневная карта
- **Profile:** XP-бар с анимацией, radar chart навыков

---

## 10. Технические особенности

### 10.1 Гибридная LLM-архитектура
- **ResilientLLM:** primary → fallbacks chain, retry 2, circuit breaker 3
- **MockLLM:** Оффлайн заглушка (intent detection)
- **Context Budget:** Token-aware trimming (4 chars/token)
- **Кэширование:** SQLite + TTL (24ч), capped 1000 rows

### 10.2 Personality Drift
- 5 осей: sarcasm, patience, paranoia, enthusiasm, formality
- Дрейф на основе: время суток, паттерн сессии, прогресс
- Генерирует модификаторы для LLM system prompt

### 10.3 Context Awareness
- Время суток: morning/afternoon/evening/night/late_night
- Паттерны: normal/binge_learning/night_owl/perfectionist/chaotic
- Атмосферные подсказки: "...3 часа ночи. Мы оба ещё не спим."

### 10.4 Memory Caps
- `exploit_success`: max 200
- `bounty_reports`, `writeup_history`, `purchase_history`: max 100
- `versus_history`: max 50
- `htb_completed`, `thm_completed`: max 100
- `command_usage`: max 50 (top by count)
- `QueryCache`: max 1000 rows
- `terminal_log`: 512 KB rotation

### 10.5 Правила (rule-based, без LLM)
- Оценка ответов (`check_open_answer_heuristic`)
- Проверка достижений (`achievement_service`)
- Верификация флагов (SHA256, exact match)
- XP/очки (арифметика)
- Adaptive topic selection (weak_topics)
- SM-2 spaced repetition
- Skill tracking (level = xp // 50)

---

## 11. Команды (114 CLI-команд, 57 API)

### Ключевые группы команд

| Группа | Команды | API endpoint |
|--------|---------|--------------|
| Чат | любое сообщение | `chat_with_llm` |
| Квизы | `/quiz`, `/task`, `/smart_test` | `generate_quiz`, `submit_quiz_result` |
| Курсы | `/courses`, `/next`, `/topics`, `/course` | `get_courses`, `select_course` |
| Story | `/story`, `/episode`, `/quest` | `get_story_episodes`, `start_story_episode` |
| Треки | `/tracks` | `get_tracks`, `start_track` |
| Лабы | `/lab`, `/practice`, `/check` | `get_labs`, `start_lab`, `stop_lab` |
| CTF | `/flag`, `/ctf` | `submit_flag`, `get_ctf_status` |
| HTB/THM | `/htb`, `/thm` | HTB API integration |
| OSINT | `/osint`, `/shodan`, `/censys` | `get_threats`, `get_cve` |
| Сканер | `/scan`, `/scanv2` | `scan_code` |
| Магазин | `/shop`, `/equip` | `get_shop`, `purchase_item` |
| Достижения | `/achievements`, `/skills` | `get_achievements`, `get_skills` |
| Аналитика | `/stats`, `/analytics`, `/dashboard`, `/heatmap` | `get_detailed_stats`, `get_heatmap` |
| Дуэль | `/versus` | `start_versus`, `versus_move` |
| Дейли | `/daily` | `get_daily_challenge`, `submit_daily_challenge` |
| Профиль | `/profile`, `/reputation` | `get_profile`, `update_profile` |
| Конфиг | `/provider`, `/model`, `/theme`, `/lang`, `/doctor` | `get_config` |
| Контекст | `/context stats`, `/context clear` | context management |

---

## 12. Зависимости

### Python (backend)
```
fastapi, uvicorn, pydantic, sqlalchemy, langchain-openai, langchain-groq,
langchain-community, langchain-ollama, rich, prompt_toolkit, chromadb,
sentence-transformers, rank_bm25, jieba, tiktoken (опционально),
pyttsx3 (TTS), python-dotenv, aiohttp, semgrep
```

### Frontend (рекомендация)
```
react/vue/svelte, typescript, tailwindcss, axios/fetch,
zustand/pinia, react-router/vue-router, recharts/chart.js,
react-markdown/markdown-it, socket.io-client (для стриминга)
```

---

*CyberTeacher v5.2 — 2026-05-29*
