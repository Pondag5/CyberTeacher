# CyberTeacher v4.3 - Идеи и план развития

*Все фичи, архитектурные решения и планы. Консолидировано из IMPLEMENTATION_PLAN.md, INDIVIDUAL_ROADMAP.md, IDEAS_FOR_INDIVIDUAL_LEARNING.md, FUTURE_VISION.md.*
*Последнее обновление: 2026-05-18*

> **📂 Документация реорганизована:**
> - **[DONE.md](DONE.md)** — всё что уже реализовано
> - **[ROADMAP.md](ROADMAP.md)** — 42 идеи, возможные без внешних сервисов
> - **[BACKLOG.md](BACKLOG.md)** — отложено (multi-user, cloud, external APIs)

---

## О проекте

CyberTeacher — CLI для обучения кибербезопасности с LLM-учителем.

| Параметр | Значение |
|----------|----------|
| **LLM** | Ollama / Groq / OpenRouter / HuggingFace |
| **RAG** | Chroma + sentence-transformers + BM25 + cross-encoder reranking |
| **UI** | Rich (CLI) + PWA Companion App (8 вкладок) |
| **DB** | SQLite |
| **Тесты** | 985 unittest, ~95% coverage |
| **API** | FastAPI, 15+ эндпоинтов |
| **CI** | ruff, GitHub Actions, pip-audit |

---

## Легенда

| Параметр | Описание |
|----------|----------|
| **Impact** | Влияние на продукт (1-10) |
| **Effort** | Сложность реализации (1-5) |
| **Status** | Not started / In progress / Done / Deferred |

---

## Ключевые паттерны

1. **State:** `get_state()` — синглтон `AppState` с 4 Pydantic-модулями
2. **Config:** `get_settings()` — синглтон `Settings` (pydantic-settings)
3. **DI:** `get_context()` — `AppContext` с state, settings, db_conn, llm, kb
4. **Services:** Чистые функции, принимают данные, возвращают результат
5. **Tests:** `unittest.mock` для `get_context()` и `console`
6. **i18n:** `t(lang, 'ui.key')` для переводов (ru/en)
7. **Язык:** Код на английском, документация/комментарии на русском

---

## Архитектура (текущая)

```
CyberTeacher/
├── main.py                    # Главный цикл, точка входа
├── handlers/                  # 60+ хендлеров (DI-мигрированы)
├── state.py                   # Core state orchestration (4 Pydantic модуля)
├── settings.py                # Pydantic Settings (get_settings())
├── shared_types.py            # Mode enum
├── state_models.py            # AppStateModel (JSON validation)
├── progress_state.py          # ProgressState (Pydantic)
├── settings_state.py          # SettingsState (Pydantic)
├── user_profile_state.py      # UserProfileState (Pydantic)
├── metrics_state.py           # MetricsState (Pydantic)
├── di.py                      # Dependency Injection container
├── i18n.py                    # Localization engine
├── services/                  # Business logic services
│   ├── achievement_service.py
│   ├── weak_topics_service.py
│   ├── spaced_repetition_service.py
│   └── skill_tracker_service.py
├── api_server.py              # FastAPI REST API + PWA сервер
├── web_ui.py                  # Streamlit dashboard
├── static/                    # PWA файлы (HTML/CSS/JS/SW)
├── locales/                   # Translation files (ru.json, en.json)
├── tests/                     # 985 тестов
└── docs/                      # Документация
```

---

## Критические проблемы (решены)

| ID | Проблема | Статус |
|----|----------|--------|
| B-01 | Полная интеграция state.py | Done |
| B-02 | Циклические импорты | Done |
| B-03 | generators.py исправлен | Done |
| B-04 | Docker availability check | Done |
| B-05 | Docker exec validation | Done |
| S-01 | Command injection (practice) | Done |

---

## Высокий приоритет

| ID | Идея | Impact | Effort | Статус |
|----|------|--------|--------|--------|
| C-01 | `risk_level` в state.py | 7 | 2 | Done |
| C-02 | Команда `/social` (социальная инженерия) | 9 | 5 | Done |
| C-03 | Команда `/threats` (сводки угроз) | 9 | 4 | Done |
| C-04 | Команда `/groups` (APT досье, 27 групп) | 8 | 3 | Done |
| C-05 | Умный RAG с реранкингом (cross-encoder) | 9 | 4 | Done |
| C-06 | Гибридный поиск (BM25 + jieba) | 8 | 5 | Done |
| C-07 | Кэширование ответов LLM (SQLite + TTL) | 7 | 4 | Done |
| C-08 | Песочница для кода (`/sandbox`) | 10 | 8 | Done |
| C-09 | Адаптивный план обучения (`/adaptive`) | 9 | 6 | Done |
| C-10 | Интервальные повторения SM-2 (`/repeat`) | 8 | 5 | Done |
| C-11 | Генерация конспектов (`/summary`) | 8 | 4 | Done |
| C-12 | Автоматическая генерация writeup (`/auto_writeup`) | 7 | 4 | Done |
| C-13 | Расширенные достижения | 6 | 3 | Done |
| C-14 | Магазин / прокачка (`/shop`) | 9 | 7 | Done |
| H-13 | Мульти-провайдер LLM | 9 | 4 | Done |
| H-16 | Асинхронные обработчики | 8 | 4 | Done |
| NEW-01 | LLM-Соперник (`/versus`) | 9 | 4 | Done |

---

## Средний приоритет

| ID | Идея | Impact | Effort | Статус |
|----|------|--------|--------|--------|
| M-03 | Модуль OSINT (`/osint`) | 8 | 6 | Done |
| M-04 | Конструктор фишинговых писем (`/phishing`) | 7 | 5 | Done |
| M-05 | Исторический режим (`/timeline`) | 6 | 4 | Done |
| M-06 | Тренажёр эксплойтов (`/exploits`) | 9 | 7 | Done |
| M-07 | Shodan / Censys (`/shodan`, `/censys`) | 7 | 4 | Done |
| M-08 | Анализ вредоносов (`/malware`) | 9 | 8 | Done |
| M-09 | Инфографика Mermaid (`/mermaid`) | 6 | 3 | Done |
| M-10 | Интерактивные расследования (`/investigation`) | 8 | 5 | Done |
| M-11 | Голосовой учитель TTS/STT (`/voice`) | 6 | 6 | Done |
| M-12 | Поддержка Jupyter Notebook (`/jupyter`) | 7 | 4 | Done |
| M-16 | Видео / подкасты (`/media`) | 5 | 4 | Done |
| M-18 | Временная петля (`/timeloop`) | 6 | 5 | Done |
| M-19 | Учитель с эмоциями (`/emotions`) | 7 | 4 | Done |
| M-20 | Кроссплатформенная синхронизация (`/sync`) | 6 | 5 | Done |
| M-22 | Summarization истории (`/summarize`) | 7 | 4 | Done |
| M-25 | HackTheBox интеграция (7 команд, 17 тестов) | 9 | 5 | Done |
| M-26 | Step-by-Step Exploit Walkthroughs | 9 | 4 | Done |
| M-27 | Exploit Submission (PoC verification) | 9 | 5 | Done |
| M-28 | Learner Dashboard (личная аналитика) | 8 | 5 | Done |
| M-29 | Path-based Adaptive Learning Tracks | 8 | 5 | Done |
| M-30 | Real-time Hints & Co-pilot | 8 | 4 | Done |
| M-31 | Bug Bounty Simulation | 8 | 5 | Done |
| M-32 | PWA Companion App (8 вкладок, Groq, offline) | 8 | 5 | Done |
| M-33 | Advanced Analytics & AI Tutor | 7 | 4 | Done |
| M-34 | Voice Assistant (TTS/STT) | 6 | 4 | Done |
| NEW-02 | Daily Challenge v2 | 7 | 2 | Done |
| NEW-03 | Code Review v2 (`/scanv2`) | 8 | 3 | Done |

### Отложено (не для индивидуального использования)

| ID | Задача | Причина |
|----|--------|---------|
| M-02 | Red vs Blue мультиплеер | Требует multi-user инфраструктуры |
| M-13 | SCORM / LTI | Интеграция с LMS (для учебных заведений) |
| M-14 | Плагинная архитектура | Избыточна для одного пользователя |
| M-15 | Курсы от экспертов | Будет через миссии/треки |
| L-11 | Кооперативные миссии | Solo-focus проект |
| L-12 | Командные соревнования | Solo-focus проект |
| L-18 | Режим "наблюдатель" | Solo-focus проект |

---

## Низкий приоритет

| ID | Идея | Impact | Effort | Статус |
|----|------|--------|--------|--------|
| L-01 | Мультимодальность LLaVA (`/vision`) | 8 | 7 | Done |
| L-02 | Трекер практических навыков (`/skills`) | 7 | 5 | Done |
| L-03 | Mind map визуализация (`/mindmap`) | 6 | 4 | Done |
| L-05 | Gamification (уровни, бейджи) | 5 | 3 | Done |
| L-06 | Dark mode для CLI (`/theme`) | 4 | 2 | Done |
| L-08 | Поддержка Python 3.13+ | 3 | 1 | Done (3.14) |
| L-09 | Интеграция с Metasploit | 9 | 9 | Done |
| L-10 | Продвинутый анализатор кода (Semgrep) | 8 | 6 | Done |
| L-13 | Подписка на уведомления (`/subscribe`) | 6 | 3 | Done |
| L-14 | Экспорт диалога (`/export`) | 6 | 2 | Done |
| L-15 | Руководство по развертыванию | 5 | 3 | Done |
| L-16 | REST API для отслеживания прогресса | 7 | 4 | Done |
| L-17 | Шаблоны заданий (`/templates`) | 6 | 3 | Done |

### Не начато

| ID | Идея | Причина |
|----|------|---------|
| L-07 | Перевод комментариев на английский | Низкий приоритет |
| G-08 | Mood translator (сленг → нормальный) | ✅ Готово |

---

## Архитектурные улучшения

| ID | Идея | Impact | Effort | Статус |
|----|------|--------|--------|--------|
| A-01 | Документация ADR | 7 | 4 | Done (5 ADRs) |
| A-02 | Type hints 100% | 8 | 5 | In progress (~80%) |
| A-03 | Dependency Injection | 8 | 6 | Done (REF-04, все 60+ хендлеров) |
| A-04 | Unit tests >70% | 9 | 5 | Done (985 тестов, ~95%) |
| A-05 | CI/CD GitHub Actions | 7 | 4 | Done |
| A-06 | ruff/mypy линтинг | 6 | 2 | Done (ruff) |
| A-07 | Конфиг в pyproject.toml | 5 | 3 | Done |

---

## Интеграции и внешние системы

| ID | Идея | Статус |
|----|------|--------|
| G-01 | TryHackMe API (6 команд) | Done |
| G-02 | HackTheBox API (7 команд, 17 тестов) | Done |
| G-03 | Генерация CTF-флагов на лету | Done |
| G-04 | Мультиязычность EN/RU (`/lang`) | Done |
| G-05 | Webhook уведомления (Telegram/Discord) | Done |
| G-06 | Docker lab templates (YAML) | Done |
| G-07 | Офлайн-режим (без LLM) | ✅ Готово |
| G-09 | Профили пользователей (`/profile`) | Done |
| G-10 | Wireshark интеграция (анализ pcap, 9 тестов) | Done |

---

## Рефакторинг (REF-01 — REF-15)

| ID | Задача | Статус |
|----|--------|--------|
| REF-01 | Registry Pattern для handlers | Done |
| REF-02 | Модульная архитектура state (10 модулей) | Done |
| REF-03 | Убрать дублирование xp_boost | Done |
| REF-04 | Dependency Injection (все 60+ хендлеров) | Done |
| REF-05 | Mode enum → shared_types.py | Done |
| REF-06 | `__getattr__` → явные @property | Done |
| REF-07 | Все state-модули → Pydantic v2 | Done |
| REF-08 | check_achievements → services/ | Done |
| REF-09 | JSON валидация через AppStateModel | Done |
| REF-10 | Все секреты из .env | Done |
| REF-12 | Все пути из .env | Done |
| REF-13 | 10 state-модулей → 4 consolidated | Done |
| REF-14 | Pydantic Settings | Done |
| REF-15 | Бизнес-логика → сервисы | Done |

---

## Реализовано в PWA

| Фича | Описание | Статус |
|------|----------|--------|
| Чат с LLM | Полноценный интерфейс через Groq | Done |
| Прогресс | XP, уровень, стрик, навыки, XP-бар | Done |
| Квизы | Динамическая генерация через LLM (5 тем) | Done |
| Курсы | 6 курсов, выбор активного, прогресс | Done |
| Лаборатории | 21 Docker-лаба, запуск/остановка | Done |
| Достижения | 8 ачивок с иконками и XP | Done |
| Дуэль | 4 сценария, чат с LLM | Done |
| Статистика | Графики активности, навыки, слабые темы | Done |
| Настройки | Тёмная/светлая тема, push-уведомления | Done |
| Service Worker | Network First, offline-режим | Done |

---

## Идеи для будущего развития (brainstorm)

### Сообщество и совместное обучение
- Multi-user режим (несколько учеников в одной сессии)
- Shared whiteboard — пошаговое решение задач вместе
- Peer review — ученики проверяют writeup друг друга
- Community challenges — еженедельные CTF от сообщества

### Контент и учебные программы
- Curriculum Builder — визуальный конструктор программ (drag-n-drop)
- Auto-alignment — сопоставление тем с MITRE ATT&CK, NIST, OWASP
- Lesson plans — готовые занятия на 90 минут с таймером
- Prerequisites graph — граф зависимостей тем

### AI Teacher улучшения
- Persona marketplace — обмен промптами персон (like GPTs)
- Context-aware hints — подсказки без спойлеров
- Mistake patterns — сбор типичных ошибок → улучшение курсов
- Socratic mode — учитель только задаёт наводящие вопросы

### Безопасность и Compliance
- GDPR/FERPA compliance mode — анонимизация, экспорт/удаление данных
- Secure sandbox escape detection — мониторинг контейнера
- Secret scanning — автоматический scan кода на API keys/credentials

### Аналитика и отчёты
- Student dashboard — прогресс по ученикам
- Predictive dropout — ML модель для выявления риска прекращения обучения
- Auto-generated progress reports (PDF)

### DevOps и инфраструктура
- Docker Swarm/K8s manifests для масштабирования
- Blue-green deployments без простоя
- Automated backups to S3/Google Cloud
- Health checks + alerting (Telegram/Discord webhook)

### Доступность (Accessibility)
- High-contrast mode для слабовидящих
- Screen reader optimization (ARIA labels)
- Keyboard-only navigation

### Мобильная версия
- PWA — иконка, offline кэш (Done)
- Push notifications для напоминаний (repeat, new content)

### Управление файлами
- Versioning uploads (как Git для PDF)
- Bulk operations (загрузка папки с курсом)
- File sharing между учениками (с одобрением админа)

---

## Фокус на индивидуальное обучение

Проект ориентирован на **одного пользователя**. Командные функции отложены.

### Приоритетный порядок (следующие сессии)

1. **Углубить обучающий контент** — walkthroughs, bug bounty, PoC verification
2. **Добавить адаптивность** — tracks, real-time hints, AI-рекомендации
3. **Интегрировать внешние платформы** — HTB, THM (Done)
4. **Расширить аналитику** — графики, predictive modeling (Done)
5. **Улучшить PWA** — offline, push-уведомления

### Что уже сделано для индивидуального обучения
- HTB/THM интеграция — сотни реальных машин
- Step-by-Step Walkthroughs — разбор каждой уязвимости
- PoC Verification — проверка реальных эксплойтов
- Learner Dashboard — XP over time, heatmap, skill bars
- Adaptive Learning Tracks — персонализированные пути
- Real-time Hints — контекстные подсказки во время лаб
- Bug Bounty Simulation — написание и ревью отчётов
- Voice Assistant — TTS/STT для обучения без экрана
- Exam Mode — симуляция стрессовой среды
- Weekly Progress Reports — автоматический анализ прогресса

---

## Как выбирать задачи

1. **Impact/Effort матрица**:
   - Quick wins: Impact 7-10, Effort 1-2
   - Strategic: Impact 9-10, Effort 3-5
   - Big bets: Impact 8-10, Effort 6+

2. **Фокус на соло-опыт**: Многопользовательские фичи отложены.

3. **User pain**: Что больше всего просят? → `/versus`, `/analytics`, `/walkthrough`

4. **Technical debt**: A-01..A-07 делать постепенно вместе с фичами

---

*Консолидировано: 2026-05-18*
*Источники: IMPLEMENTATION_PLAN.md, INDIVIDUAL_ROADMAP.md, IDEAS_FOR_INDIVIDUAL_LEARNING.md, FUTURE_VISION.md*
