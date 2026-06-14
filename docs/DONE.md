# CyberTeacher — Реализованные фичи

*Все что уже сделано. Версия 5.2. Последнее обновление: 2026-05-29*

---

## 🧠 Атмосфера и личность (SPRINT 12 — 2026-05-29)

| Фича | Команда | Описание |
|------|---------|----------|
| Context Awareness | Автоматически | Время суток (утро/день/вечер/ночь/глубокая ночь), паттерны сессии (binge/night_owl/perfectionist/chaotic) |
| Personality Drift | Автоматически | Динамическая динамика: sarcasm, patience, paranoia, enthusiasm, formality — адаптируется под поведение |
| Atmosphere Hints | Автоматически | "...3 часа ночи. Мы оба ещё не спим." "...ты в ударе. Не забывай делать перерывы." |
| LLM Stats | Автоматически | llm_call_count и llm_total_tokens инкрементируются в CachedLLM |
| Backup Rotation | Автоматически | Макс 5 бэкапов, старые удаляются |
| Terminal Log Rotation | Автоматически | 512 KB cap, ротация (keep second half) |
| Setup Ollama | `scripts/setup_ollama.bat` | Пошаговая установка Ollama + модели (Windows) |
| Setup Ollama | `scripts/setup_ollama.sh` | Пошаговая установка Ollama + модели (Linux/Mac) |

---

## 🛡️ Стабильность (SPRINT 4 — 2026-05-29)

| Фича | Команда | Описание |
|------|---------|----------|
| Context Budget Manager | `/context stats` | Токен-осознанный budget manager (4 chars/token), budget allocation, stats |
| Context Clear | `/context clear` | Очистка истории чата |
| Provider Fallback Chain | Автоматически | ResilientLLM с retry (2), circuit breaker (3 fails), fallback chain (ollama→groq→openrouter→hf) |
| CachedLLM hardened | Автоматически | try/except + логирование ошибок в CachedLLM.invoke() и .stream() |
| Achievement service wired | Автоматически | `state.check_achievements()` → `services/achievement_service` (29 достижений, rule-based) |
| Memory caps | Автоматически | exploit_success(200), bounty(100), writeups(100), purchases(100), versus(50), htb/thm(100) |
| QueryCache cap | Автоматически | Max 1000 строк, eviction expired entries при insert |
| Log rotation | Автоматически | RotatingFileHandler 5MB × 3 для cyberteacher.log |
| Periodic cleanup | Автоматически | Cleanup сообщений каждые 50, auto-summarize каждые 20 |
| HANDLES optimization | Автоматически | Исключён из JSON-сериализации |

## 🤖 Гибридная LLM-архитектура (2026-05-29)

| Фича | Команда | Описание |
|------|---------|----------|
| MockLLM | Автоматически (fallback) | Оффлайн заглушка — при пустом .env все команды работают через шаблоны |
| /doctor | `/doctor` | Onboarding — статус всех LLM провайдеров, таблица health check |
| /doctor setup ollama | `/doctor setup ollama` | Пошаговая инструкция установки Ollama + модели |
| /doctor setup groq | `/doctor setup groq` | Пошаговая инструкция настройки Groq API |
| /doctor setup openrouter | `/doctor setup openrouter` | Пошаговая инструкция настройки OpenRouter API |
| /doctor mock | `/doctor mock` | Переключение в оффлайн-режим (MockLLM) |
| LazyLoader + MockLLM | Автоматически | При пустом .env → MockLLM → ResilientLLM не создаётся |
| Fallback + MockLLM | Автоматически | MockLLM как последний fallback в цепочке (ollama→groq→openrouter→hf→mock) |
| Integration tests | Автоматически | 20 тестов: context budget, quiz→XP→achievement, memory caps, provider fallback |

---

## 🎯 Режимы обучения

| Фича | Команда | Описание |
|------|---------|----------|
| Режим учителя | `/teacher` | Объяснения, аналогии, Socratic метод |
| Экспертный режим | `/expert` | Краткие технические ответы |
| CTF режим | `/ctf` | Флаги, соревнования, риск-трекинг |
| Code review | `/review` | Анализ кода на уязвимости |
| Hybrid persona | `/hybrid` | Адаптивный стиль (переключает роли) |
| Офлайн-режим | `/offline` | Работа без LLM (G-07) |
| Mood translator | `/mood` | 5 стилей: normal/hacker/formal/casual/minimal (G-08) |

---

## 📚 Обучение

| Фича | Команда | Описание |
|------|---------|----------|
| Викторина | `/quiz` | Адаптивная, фокус на слабых темах |
| Практическое задание | `/task` | Открытый ответ, оценка |
| Генератор заданий | `/genassignment` | CTF/лаба задания |
| Story mode | `/story` | Игровой режим с 21 эпизодом |
| Учебные треки | `/tracks` | 4 структурированных пути |
| Адаптивное обучение | `/adaptive` | Показать слабые темы |
| Интервальные повторения | `/repeat` | SM-2 алгоритм, календарь, статистика |
| Конспекты | `/summary` | Генерация Markdown-конспекта |
| Auto writeup | `/auto_writeup` | Автоматический writeup |
| Writeup template | `/writeup` | Шаблон writeup |
| Writeups browser | `/writeups` | Просмотр прошлых writeup'ов |
| Курсы | `/courses` | 6 курсов, прогресс |
| Следующая тема | `/next` | Переход к следующей теме курса |
| Темы курсов | `/topics` | Все темы по 6 курсам с прогрессом |
| Docker лаборатории | `/lab` | 21 лаба |
| Walkthroughs | `/walkthrough` | Пошаговый разбор эксплойта |
| Поиск эксплойтов | `/exploit` | По CVE |
| Тренажёр эксплойтов | `/exploits` | Написание эксплойтов |
| Exploits log | `/exploits_log` | История попыток, success rate |
| Jupyter Notebooks | `/jupyter` | Шаблоны для практики |
| Bug Bounty | `/bounty` | Симуляция написания отчётов |
| Exploit submission | `/exploit_submit` | Проверка PoC |
| Daily Challenge | `/daily` | Ежедневный челлендж со стриком |
| Шаблоны заданий | `/templates` | YAML шаблоны |
| Mind map | `/mindmap` | ASCII карта тем |
| Социальная инженерия | `/social` | Тренажёр социальной инженерии |
| Расследования | `/investigation` | Интерактивные расследования (M-10) |
| Медиа | `/media` | Видео/подкасты плеер (M-16) |
| Timeloop | `/timeloop` | Временная петля / альтернативные реальности (M-18) |
| Голосовой помощник | `/voice` | TTS/STT помощник (M-34) |
| Исторический режим | `/timeline` | Исторические события в кибербезопасности (M-05) |

---

## 📊 Информация и аналитика

| Фича | Команда | Описание |
|------|---------|----------|
| Новости | `/news` | Новости кибербезопасности (RSS) |
| CVE | `/cve` | Информация о CVE |
| APT досье | `/threats` | 27 группировок |
| Группировки | `/groups` | APT по странам |
| Сводка угроз | `/threat summary` | Еженедельный обзор |
| Статистика | `/stats` | Очки, курсы, флаги, длительность сессии |
| Продвинутая аналитика | `/analytics` | Графики, AI рекомендации |
| Дашборд | `/dashboard` | Личная аналитика, XP, навыки |
| Heatmap | `/heatmap` | Тепловая карта активности (28 дней) |
| История чата | `/history` | Лог диалогов |
| Достижения | `/achievements` | 29 ачивок с XP |
| Использование команд | `/usage` | Статистика команд |
| Кэш ответов | `/cache stats` | Статистика кэша |
| Очистка кэша | `/clearcache` | Очистить кэш ответов |
| База знаний | `/kb_status` | Статус RAG базы |
| Risk level | `/risk` | Уровень риска (CTF/Story) |
| Skills tracker | `/skills` | Трекер практических навыков |
| Сертификаты | `/certificates` | ASCII сертификаты навыков |
| Репутация | `/reputation` | Репутация и хэндлы |
| Глубина объяснений | `/depth` | beginner/normal/expert |
| Эмоции учителя | `/emotions` | Sentiment-анализ |
| Профиль | `/profile` | Имя, аватар, статистика |

---

## 🔧 Практика и инструменты

| Фича | Команда | Описание |
|------|---------|----------|
| Практика | `/practice` | CTF/HTB |
| HackTheBox | `/htb` | 7 команд, машины, флаги |
| TryHackMe | `/thm` | 6 команд |
| Песочница | `/sandbox` | Docker-песочница для кода |
| Terminal log | `/terminal`, `/log` | Лог терминала |
| OSINT | `/osint` | Разведка (симуляция) |
| Shodan | `/shodan` | Поиск устройств |
| Censys | `/censys` | Поиск сервисов |
| Malware analysis | `/malware` | Анализ вредоносов (симуляция) |
| Phishing | `/phishing` | Конструктор фишинговых писем |
| Mermaid | `/mermaid` | Инфографика |
| Metasploit | `/msf` | Интеграция с Metasploit |
| PCAP анализ | `/pcap` | Анализ pcap файлов |
| Code scan v2 | `/scanv2` | Semgrep + OWASP Top 10 |
| Code scan | `/scan` | Сканирование кода на уязвимости |
| Fix code | `/fixcode` | Генерация безопасного кода |
| CTF dynamic flags | `/ctf` | Динамические флаги |
| Docker compose | `/dockergen` | Генерация docker-compose |

---

## ⚙️ Управление

| Фича | Команда | Описание |
|------|---------|----------|
| Флаг | `/flag` | Проверить флаг |
| LLM провайдер | `/provider` | Показать/сменить провайдера |
| LLM модель | `/model` | Показать/сменить модель |
| API ключ | `/set-api-key` | Установить API ключ |
| Добавить PDF | `/add_book` | Добавить в базу знаний |
| Проверить контейнеры | `/check` | Docker контейнеры |
| Версия | `/version` | Версия приложения |
| Очистить чат | `/clear` | Очистить историю |
| Меню | `/menu` | Цифровое меню (76 команд) |
| Экспорт | `/export` | Экспорт чата (Markdown/JSON) |
| Настройки | `/config` | Интерактивный мастер |
| Тема | `/theme` | 3 темы: ocean/sunset/matrix |
| Язык | `/lang` | ru/en |
| Feature flags | `/features` | Вкл/выкл модулей |
| Суммаризация | `/summarize` | Суммаризация диалога |
| Подписка | `/subscribe` | Подписка на угрозы |
| Sync | `/sync` | Кроссплатформенная синхронизация |
| PWA | `/pwa` | Мобильное приложение |
| API | `/api` | REST API сервер |
| Versus | `/versus` | LLM-Соперник (4 сценария) |
| Vision | `/vision` | Анализ изображений (LLaVA) |
| Telegram | `/telegram` | Telegram бот |
| Health check | `/health` | Проверка здоровья системы |
| Backup | `/backup` | Бэкап состояния |
| Network | `/network` | Сетевые утилиты |
| Tools | `/tools` | Управление инструментами |
| Equipment | `/equip` | Экипировка |
| Missions | `/missions` | Миссии |
| Hint | `/hint` | Контекстные подсказки |
| Магазин | `/shop` | 17 товаров, динамические цены |
| State management | `/state` | Экспорт/импорт/листинг состояния |
| Launcher | `python launcher.py` | GUI-панель запуска |

---

## 🌐 Интеграции

| Фича | Статус | Описание |
|------|--------|----------|
| Ollama | ✅ | Локальная LLM |
| Groq | ✅ | Быстрая облачная LLM |
| OpenRouter | ✅ | Мульти-провайдер |
| HuggingFace | ✅ | Бесплатный tier |
| TryHackMe API | ✅ | 6 команд |
| HackTheBox API | ✅ | 7 команд, 17 тестов |
| RSS (SecurityWeek, CISA) | ✅ | Новости кибербезопасности |
| ChromaDB | ✅ | Векторное хранилище |
| SQLite | ✅ | База данных |
| PostgreSQL | ✅ | Альтернативная БД (SQLAlchemy) |
| Docker | ✅ | Лаборатории, песочница |
| Metasploit | ✅ | Интеграция с Metasploit |
| Shodan | ✅ | Поиск устройств |
| Censys | ✅ | Поиск сервисов |
| Semgrep | ✅ | Статический анализ кода |
| Telegram Bot | ✅ | Telegram-бот |
| Alembic | ✅ | Миграции БД |

---

## 🏆 Достижения (29 total)

| Категория | Кол-во | Примеры |
|-----------|--------|---------|
| Флаги | 3 | first_flag, flag_collector_10, flag_master_50 |
| Задания | 2 | assignment_completer, assignment_master_10 |
| Очки | 2 | points_earner_100, points_earner_500 |
| Docker | 1 | docker_explorer |
| Квизы | 1 | quiz_taker |
| Новости | 1 | news_follower |
| Социальная инженерия | 2 | social_engineer_5, social_engineer_20 |
| APT | 2 | apt_hunter_10, apt_hunter_25 |
| Stealth | 2 | ghost_in_the_shell_5, ghost_in_the_shell_15 |
| Threats | 2 | snowden_10, snowden_25 |
| Стрики | 3 | streak_3, streak_7, streak_30 |
| Треки | 2 | track_completer_1, track_completer_5 |
| Bug Bounty | 2 | bounty_reporter_1, bounty_reporter_10 |
| Навыки | 2 | skill_master_3, skill_master_5 |
| Повторения | 2 | review_streak_5, review_streak_25 |

---

## 🛒 Магазин (17 товаров)

| Категория | Кол-во | Примеры |
|-----------|--------|---------|
| Темы | 5 | Matrix, Cyberpunk, Hacker, Amber, Nord |
| Подсказки | 3 | hint_single, hint_pack_3, hint_pack_10 |
| XP Бусты | 3 | xp_boost_1h, xp_boost_4h, xp_boost_24h |
| Расходники | 2 | lucky_charm, risk_reset |
| Топики | 4 | Cloud Security, Mobile Security, IoT, ICS/SCADA |

**Фичи магазина:** динамические цены (скидка от репутации), история покупок (`/shop history`)

---

## 📱 PWA Companion App (18 вкладок)

| # | Вкладка | Иконка | Описание |
|---|---------|--------|----------|
| 1 | Режимы | 🎭 | Переключение 6 режимов обучения |
| 2 | Чат | 💬 | Интерфейс чата с LLM |
| 3 | Прогресс | 📊 | XP, уровень, стрик, навыки, XP-бар |
| 4 | Квизы | 📝 | Динамическая генерация (5 тем) |
| 5 | Дейли | 🎯 | Ежедневный челлендж со стриком |
| 6 | Профиль | 👤 | Имя, аватар, статистика |
| 7 | Курсы | 📚 | 6 курсов, выбор, прогресс |
| 8 | История | 📖 | 21 эпизод story mode |
| 9 | Треки | 🛤️ | 4 учебных трека с прогрессом |
| 10 | CTF | 🚩 | Флаги, статус, отправка |
| 11 | Лабы | 🐳 | 21 Docker-лаба, запуск/остановка |
| 12 | OSINT | 🔍 | APT группы, новости, CVE lookup |
| 13 | Сканер | 💻 | Анализ кода на уязвимости |
| 14 | Магазин | 🛒 | 17 товаров, покупка за XP |
| 15 | Malware | 🦠 | Анализ вредоносов (симуляция) |
| 16 | Достижения | 🏆 | 29 ачивок с иконками и XP |
| 17 | Дуэль | 🥊 | 4 сценария, чат с LLM |
| 18 | Статистика | 📈 | Графики активности, навыки, слабые темы |
| 19 | Настройки | ⚙️ | 3 темы, push, офлайн-режим |

**Service Worker:** Network First стратегия, авто-обновление (cache v12).

---

## 🎨 Дизайн-система

### Персонаж учителя
**Рик Санчез + Док Браун** — саркастичный, гениальный, эксцентричный наставник.
- Фирменные фразы: "*отрыжка*", "ВЕЛИКОЛЕПНО!", "1.21 гигаватт знаний!"
- Безумные аналогии из научной фантастики
- 5 режимов: teacher/expert/ctf/review/hybrid
- 5 стилей общения: normal/hacker/formal/casual/minimal

### Визуальные темы (3)
| Тема | Цвета | Вайб |
|------|-------|------|
| 🌊 Ocean | `#00B4D8` / `#48CAE4` | Океан, технологичный |
| 🌅 Sunset | `#FF6A00` / `#9D4EDD` | Закат, synthwave |
| 💻 Matrix | `#00FF41` / `#00CC33` | Матрица, хакерский |

### Типографика
- **Основной:** Inter (UI)
- **Моноширинный:** Fira Code (код, терминал)

### Палитра проекта
| Элемент | Цвет |
|---------|------|
| Фон | `#1e1e2e` |
| Карточки | `#2a2a3c` |
| Акцент | Зависит от темы |
| Текст | `#e0e0e0` |
| Neon glow | Зависит от темы |

---

## 🏗️ Архитектура

| Компонент | Описание |
|-----------|----------|
| State | 4 Pydantic-модуля: progress, settings, user_profile, metrics |
| DI | AppContext container, @inject decorator |
| Services | achievement, weak_topics, spaced_repetition, skill_tracker |
| Registry | Pattern для handlers (exact/prefix matching) |
| i18n | ru/en переводы |
| RAG | Chroma + sentence-transformers + BM25 + cross-encoder |
| LLM Cache | SQLite + TTL |
| Config | pydantic-settings, .env |
| Lazy Loader | config.py — ленивая загрузка LLM/embeddings |
| Response Cache | OrderedDict с LRU eviction |
| DB Layer | SQLAlchemy (SQLite + PostgreSQL) |
| Migrations | Alembic (авто-миграции) |

---

## 🔌 API Endpoints (40+)

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/health` | GET | Статус сервера |
| `/api/progress` | GET | Прогресс (XP, уровень, стрик) |
| `/api/stats` | GET | Расширенная статистика |
| `/api/courses` | GET | Список курсов |
| `/api/labs` | GET | Список лабораторий |
| `/api/achievements` | GET | Достижения |
| `/api/skills` | GET | Навыки |
| `/api/weak-topics` | GET | Слабые темы |
| `/api/quiz/generate` | POST | Генерация квиза |
| `/api/quiz/result` | POST | Результат квиза |
| `/api/chat` | POST | Чат с LLM (Rick persona) |
| `/api/modes` | GET | Список режимов |
| `/api/mode/set` | POST | Переключить режим |
| `/api/profile` | GET | Профиль пользователя |
| `/api/profile/update` | POST | Обновить профиль |
| `/api/daily` | GET | Ежедневный челлендж |
| `/api/daily/submit` | POST | Отправить ответ |
| `/api/story` | GET | Список эпизодов |
| `/api/story/start` | POST | Начать эпизод |
| `/api/story/submit` | POST | Отправить ответ |
| `/api/tracks` | GET | Список треков |
| `/api/tracks/start` | POST | Начать трек |
| `/api/tracks/progress` | POST | Обновить прогресс |
| `/api/ctf/status` | GET | Статус CTF |
| `/api/flags/submit` | POST | Отправить флаг |
| `/api/missions` | GET | Список миссий |
| `/api/missions/start` | POST | Начать миссию |
| `/api/threats` | GET | APT досье |
| `/api/cve/{id}` | GET | CVE lookup |
| `/api/news` | GET | Новости |
| `/api/scan` | POST | Сканирование кода |
| `/api/scanv2` | POST | Semgrep + OWASP |
| `/api/scanv2/rules` | GET | Список правил |
| `/api/malware` | POST | Анализ вредоноса |
| `/api/shop` | GET | Товары магазина |
| `/api/shop/purchase` | POST | Купить товар |
| `/api/heatmap` | GET | Heatmap активности |
| `/api/history` | GET | История чата |
| `/api/config` | GET | Конфигурация |
| `/api/writeups` | GET | Список writeup'ов |
| `/api/versus/*` | GET/POST | Дуэль (4 endpoint'а) |
| `/api/docker/*` | GET/POST | Docker labs (5 endpoint'ов) |
| `/api/offline` | GET/POST | Офлайн-режим |
| `/` | GET | PWA index.html |
| `/static/*` | GET | Статические файлы PWA |

---

## 🧪 Тестирование

| Метрика | Значение |
|---------|----------|
| Тестов | 985 |
| Покрытие | ~95% |
| Ошибок | 0 |
| Skipped | 4 |

---

## 📋 Рефакторинг (15/15 Done)

| ID | Задача | Статус |
|----|--------|--------|
| REF-01 | Registry Pattern | Done |
| REF-02 | Модульная архитектура state | Done |
| REF-03 | Убрать дублирование xp_boost | Done |
| REF-04 | Dependency Injection | Done |
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

## 📖 ADR (5/5 Done)

| № | Тема |
|---|------|
| 0001 | Lazy Loader |
| 0002 | Hybrid RAG |
| 0003 | LLM Caching |
| 0004 | Singleton State |
| 0005 | Rate Limiting |

---

## 🚀 Launcher

GUI-панель запуска (`python launcher.py`):
- 🗄️ **Database:** Start/Stop PostgreSQL, Run Migrations, Status
- 🖥️ **Application:** Start CLI, Start API, Open PWA
- 🐳 **Docker Labs:** Start/Stop, Status
- 📊 **Monitoring:** Open pgAdmin, View Logs, System Info

Тёмная cyberpunk тема, авто-обновление статусов каждые 5 секунд.

---

## 🧹 Code Polish (Спринт 7)

| Фича | Описание |
|------|----------|
| Ruff linting | 0 ошибок (было 1170 → 15 auto-fixed → 12 fixed manually → 5 ignored) |
| Lambda bug fix | Fixed F821: lambda capturing exception variable `e` |
| Subprocess safety | Added `check=False` to all `subprocess.run()` calls |
| Iterable unpacking | Replaced list concatenation with `*args` unpacking |
| Trailing whitespace | Cleaned migration file |
| DTZ timezone rules | Added DTZ006/DTZ007 to ignore list (pre-existing patterns) |
| Import sorting | Auto-fixed with `ruff --fix` |

---

## 📁 File Organization (Спринт 8)

| Фича | Описание |
|------|----------|
| Junk cleanup | Удалено 25 файлов (coverage, lint, test outputs, temp) |
| Cache cleanup | Удалено 6 директорий (htmlcov, .mypy_cache, .ruff_cache, MagicMock, temp_cheatsheets, __pycache__) |
| State models | 14 файлов перемещено в `models/` пакет |
| Backups | Сокращено с 30 до 3 файлов (оставлены новейшие) |
| Import updates | Обновлены импорты в state.py и тестах |
| .gitignore | Обновлён для новой структуры |

---

## 🗄️ State Migration (Спринт 9)

| Фича | Описание |
|------|----------|
| AppStateRecord model | Новая модель в `db.py` — хранит состояние в БД (JSON column) |
| DB save/load | `save_app_state()`, `load_app_state()`, `migrate_json_to_db()` |
| STATE_BACKEND | Переменная окружения: `json` (default) или `db` |
| JSON fallback | Автоматический fallback на JSON если БД недоступна |
| Alembic migration | `8ff380d95f4a_add_app_state_table.py` |
| CLI команды | `/state migrate to-db`, `/state migrate to-json`, `/state migrate status` |
| Refactored state.py | `_to_dict()`, `_from_dict()`, `_save_json()` — чистая архитектура |

---

## 🔤 Type Hints (Спринт 10 — Partial)

| Файл | Исправлено |
|------|------------|
| di.py | `get_llm()`, `get_knowledge_base()`, `save_state()`, `inject()` |
| knowledge.py | `get_current_vectordb()`, `set_current_vectordb()`, `ProgressEmbeddings`, `load_metadata()`, `save_metadata()`, `scan_knowledge_files()`, `load_and_split_file()`, `load_knowledge_base()`, `get_relevant_docs()`, `get_knowledge_status()` |
| main.py | `CachedLLM`, `get_llm()`, `get_cached_llm()`, `set_learning_context()`, `get_learning_context()`, `get_news_context()`, `get_embeddings()`, `main()`, `_save_session_summary()` |
| api_server.py | `scan_code_simple()`, `analyze_malware()`, `start_api_server()`, `stop_api_server()`, `is_server_running()` |

---

*CyberTeacher v5.0 — 2026-05-18*
