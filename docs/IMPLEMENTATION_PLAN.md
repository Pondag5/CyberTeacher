# CyberTeacher - Полный план реализации

*Последнее обновление: 2026-03-28*

---

## 📋 Оглавление

 1. [Infrastructure & Quality](#infrastructure--quality)
 2. [Blocker (Критические проблемы)](#blocker)
 3. [Critical (Высший приоритет)](#critical)
 4. [High (Высокий приоритет)](#high)
 5. [Medium (Средний приоритет)](#medium)
 6. [Low (Низкий приоритет)](#low)
 7. [Done (Завершено)](#done)

---

## Infrastructure & Quality (Инфраструктура и качество)

 Необходимо для стабильной разработки и деплоя.

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| Q-01 | Unit tests >70% coverage | Покрыть основные модули (state, handlers, knowledge). | H-11 | ✅ Done (359 tests passing, coverage 73%) |
| Q-02 | CI/CD GitHub Actions | Автотесты, ruff, mypy на каждый PR/commit. | H-12 | ✅ Done |
| Q-03 | Ruff + mypy линтинг | Единый стандарт кода, типы. | A-06 | ✅ Done (включено в CI) |
| Q-04 | Metrics & health checks | Логирование времени ответа, токенов, hit rate кэша. Эндпоинт /health. | H-18 | ✅ Done |
| Q-05 | Rate limiting | Максимум 10 запросов в минуту к боту. | M-21 | ✅ Done |
| Q-06 | Бэкапы state/БД | Автоматический бэкап memory/app_state.json, knowledge_base/news_cache.json. | — | ✅ Done |
| Q-07 | ADRs | Документирование ключевых архитектурных решений в docs/adr/. | M-33 | ✅ Done (5 ADRs) |
| Q-08 | Сканирование уязвимостей зависимостей | Запуск pip-audit/safety в CI, блокировать merge при критических уязвимостях. | H-17 | ✅ Done (pip-audit в CI) |

---

## Blocker (Критические проблемы)

 必须立即修复，否则系统无法正常工作或 сильно ограничен.

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| B-01 | Полная интеграция state.py | Убрать передачу mode/level через аргументы, везде использовать get_state(). Сейчас часть кода использует глобальные переменные, часть — параметры. | review_notes.md:219-221 | Done |
| B-02 | Устранение циклических импортов | Вынести общие функции (get_learning_context, logging utils) в отдельный модуль (common.py). Основная проблема: main ↔ handlers, handlers ↔ code_review ↔ config. | review_notes.md:222-224 | Done |
| B-03 | Исправить generators.py | Добавить недостающие импорты (random, get_relevant_docs, print_panel), реализовать extract_json_block. Сейчас код неработоспособен. | КОНТЕКСТ_2026-03-09.md:29 | Done |
| B-04 | Проверка Docker в practice.py | Добавить проверку availability перед запуском контейнеров, выводить понятное сообщение если Docker не запущен. | review_notes.md:263 | Done |
| B-05 | Валидация команд Docker exec | Экранировать пользовательский ввод через shlex.quote, использовать белый список разрешённых команд для предотвращения escape-а. | review_notes.md:309-313 | Done |

---

## Critical (Высший приоритет)

Ключевые фичи, которые значительно улучшат продукт.

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| C-01 | risk_level в state.py | Переменная для механики компрометации/следования. Интегрировать в CTF и story mode. | roadmap.md:165, fantasy-mao.md:41 | Done |
| C-02 | Команда /social (социальная инженерия) | Интерактивный диалоговый тренажёр: ученик общается с ботом-"жертвой", LLM оценивает убедительность фраз. Прототип через LLM с системой выборов. | roadmap.md:53-57, 245-252 | Done |
| C-03 | Команда /threats | Еженедельная сводка актуальных угроз (APT, DDoS, ransomware) с анализом от учителя. Парсить RSS-ленты (SecurityWeek, CISA). | roadmap.md:149-150, 172-173 | ✅ Done |
| C-04 | Команда /group <name> | Досье на APT-группы из JSON-файла (27 групп, техники, инструменты). | roadmap.md:151, 174 | ✅ Done (27 JSON файлов создано, команды /threats и /groups работают) |
| C-05 | Умный RAG с реранкингом | После top-K (10) чанков прогонять cross-encoder (cross-encoder/ms-marco-MiniLM-L-6v2) и оставлять top-3-5. | roadmap.md:199-201 | ✅ Done (интеграция в knowledge.py готова, работает)
| C-06 | Гибридный поиск (BM25) | Добавить keyword-based поиск к векторному для редких терминов. | roadmap.md:201 | ✅ Done (BM25 + jieba токенизация, комбинирование с векторными scores) |
| C-07 | Кэширование ответов LLM | Таблица query_cache в SQLite: hash запроса + режим + контекст → ответ. TTL: 1 день для актуальных, вечно для теории. | roadmap.md:205-210 | ✅ Done (CachedLLM класс, интеграция завершена, все LLM вызовы через SQLite кэш с TTL)
| C-08 | Песочница для кода | Запуск кода ученика (Python, Bash) в Docker-контейнере с проверкой результата. | roadmap.md:212-218 | ✅ Done (валидация, ограничения, команда /sandbox) |
| C-09 | Адаптивный план обучения | После квиза/задачи анализировать ошибки, записывать слабые темы в state. Подбор следующих материалов (фокус на weak_topics). | roadmap.md:227-230 | ✅ Done (интерактивные квизы/задачи с оценкой, weak_topics в state, команда /adaptive) |
| C-10 | Интервальные повторения (Spaced Repetition) | Алгоритм SuperMemo: повторение через 1 день, 3 дня, неделю, месяц. Уведомление при старте. | roadmap.md:233-238 | ✅ Done (SM-2 упрощённый, расписание review_schedule, команда /repeat, уведомление при старте) |
| C-11 | Генерация конспектов (/summary) | По теме генерировать структурированный конспект в Markdown с использованием RAG. | roadmap.md:241-242 | ✅ Done (команда /summary, RAG поиск, шаблон Markdown, сохранение в файл) |
| C-12 | Автоматическая генерация writeup | После задания/эпизода генерировать структурированный отчёт в Markdown с анализом, рекомендациями, ссылками на источники. | roadmap.md:320-321 | ✅ Done (команда /auto_writeup, сбор данных из квизов/заданий, RAG контекст, сохранение в файл) |
| C-13 | Расширенные достижения | Добавить ачивки: Social Engineer, APT Hunter, Ghost in the Shell, Сноуден с описаниями и XP-бонусами. | roadmap.md:271-276 | ✅ Done |
| C-14 | Магазин / прокачка | За XP покупать инструменты, темы, косметику, подсказки. | roadmap.md:279-285 | ✅ Done |

---

## High (Высокий приоритет)

Важные улучшения для перехода на новый уровень.

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| H-01 | Визуальная карта сети (ASCII) | Отображение узлов и соединений в терминале через ASCII-графику. | fantasy-mao.md:35, roadmap.md:36 | ✅ Done (/network) |
| H-02 | Система RAM (инструменты) | Ограниченный "снаряжение" перед заданием: выбирать скрипты/программы, которые занимают "память". | fantasy-mao.md:33, roadmap.md:27-28 | ✅ Done (/tools, /equip) |
| H-03 | Таймер Trace (опасность) | Обратный отсчёт при взломе, по истечении — обнаружение. Учитель даёт подсказку при неудаче. | fantasy-mao.md:36, roadmap.md:29-31 | ✅ Done (time_limit_minutes in labs, /network shows timer) |
| H-04 | Единая сюжетная кампания | Объединить 20 эпизодов в связанную историю с развитием. | fantasy-mao.md:37, roadmap.md:81-82 | ✅ Done (story_mode с последовательной разблокировкой) |
| H-05 | Редактор миссий | Формат JSON для пользовательских сценариев, валидация, загрузка. | fantasy-mao.md:38, roadmap.md:86-88 | ✅ Done (/missions, /mission start, /mission submit) |
| H-06 | Интеграция CVE | Команда /cve CVE-2024-1234: описание, эксплойты, рекомендации. Парсить NVD, Exploit-DB. | roadmap.md:291-294 | ✅ Done (/cve with NVD lookup) |
| H-07 | GitHub / GitLab интеграция | Анализ кода по URL, поиск секретов в истории коммитов, генерация отчёта. | roadmap.md:296-300 | ✅ Done (/scan <repo_url>) |
| H-08 | Telegram / Discord бот | Запуск квизов в чате, уведомления, достижения. | roadmap.md:302-309 | ✅ Done |
| H-09 | Web UI (Streamlit/Gradio) | Визуализация сети, карта угроз, красивые схемы, загрузка файлов. | fantasy-mao.md:39, roadmap.md:92-95 | ✅ Done (basic Streamlit dashboard) |
| H-10 | Документация (пир接头) | Полные docstrings, Architecture Decision Records, Руководство пользователя. | review_notes.md:6, 334-339 | ✅ Done (ADRs, README updated, docstrings) |
| H-11 | Увеличение coverage тестов | Deprecated: см. Q-01. | ЧЕКЛИСТ_2026-03-09.md:86 | Deprecated |
| H-12 | CI/CD (GitHub Actions) | Deprecated: см. Q-02. | ЧЕКЛИСТ_2026-03-09.md:85 | Deprecated |
| H-13 | Мульти-провайдер LLM | Поддержка Ollama, OpenRouter, HuggingFace с переключением через `/provider`. Каждый провайдер использует свои настройки из .env. | — | Done |
| H-14 | Команда `/model` | Переключение моделей внутри провайдера без редактирования конфига. | — | Done |
| H-15 | Команда `/set-api-key` | Установка API ключей для OpenRouter/HuggingFace прямо из CLI (сессионно). | — | Done |
| H-16 | Асинхронные обработчики | Параллельные запросы: RAG + LLM одновременно для скорости ответа. | — | ✅ Done |
| H-17 | Сканирование уязвимостей зависимостей | Deprecated: см. Q-08. | — | Deprecated |
| H-18 | Метрики производительности | Deprecated: см. Q-04. | — | Deprecated |

---

## Medium (Средний приоритет)

Фокус на **индивидуальное использование**. Командные и учебные функции deferred.

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| M-01 | Docker Compose | Запуск всего стека (бот, база, лаборатории) одной командой. | ЧЕКЛИСТ_2026-03-09.md:96 | ✅ Done |
| M-03 | Модуль OSINT | Симуляция разведки: поиск в соцсетях, анализ метаданных, leaks. | roadmap.md:390-397 | ✅ Done |
| M-04 | Конструктор фишинговых писем | Создание писем, оценка убедительности LLM, симуляция отправки. | roadmap.md:399-401 | ✅ Done |
| M-05 | Исторический режим | Курс "Эволюция взлома" от 80-х до 2020-х с эмуляцией инструментов эпохи. | roadmap.md:403-412 | ✅ Done |
| M-06 | Тренажёр эксплойтов | Практика написания эксплойтов на C/Python, проверка в песочнице. | roadmap.md:414-416 | ✅ Done |
| M-07 | Shodan / Censys интеграция | Поиск устройств в интернете по параметрам через API. | roadmap.md:422-424 | ✅ Done |
| M-08 | Анализ вредоносов (песочница) | Загрузка файла, динамический анализ (Cuckoo-style), отчёт поведения. | roadmap.md:426-428 | ✅ Done |
| M-09 | Инфографика (Mermaid) | Генерация кода Mermaid для mindmap и схем, отображение в Web UI. | roadmap.md:430-432 | ✅ Done |
| M-10 | Интерактивные расследования | Кейсы типа "Her Story": логи, дампы, переписка — нужно найти улики. | roadmap.md:383-385 | ✅ Done |
| M-11 | Голосовой учитель (TTS/STT) | Распознавание речи (Vosk) и синтез (Coqui TTS/Silero). | roadmap.md:386-388 | ✅ Done |
| M-12 | Поддержка Jupyter Notebook | Шаблоны ноутбуков для практики, выполнение ячеек, проверка. | roadmap.md:310-312 | ✅ Done |
| M-16 | Видео / подкасты внутри | Встроенный плеер для YouTube, синхронизация с конспектом. | roadmap.md:338-341 | ✅ Done |
| M-17 | Новости с аналитикой | Учитель комментирует новости: "Эта атака напоминает Митника..." | roadmap.md:343-344 | ✅ Done (команда /news analyze) |
| M-18 | Временная петля / альтернативные реальности | Ветвящиеся сюжеты в story_mode, разные концовки. | roadmap.md:350-352 | ✅ Done |
| M-19 | Учитель с эмоциями | Сентимент-анализ ответов ученика, изменение тона учителя (обида, радость). | roadmap.md:354-357 | ✅ Done |
| M-20 | Кроссплатформенная синхронизация | Firebase/custom бэкенд для синхронизации прогресса между ПК, вебом, мобильным. | roadmap.md:358-361 | ✅ Done |
| M-22 | Sumarization истории | Каждые 20 сообщений сворачивать в краткий вывод через LLM. | ЧЕКЛИСТ_2026-03-09.md:93 | ✅ Done (команда /summarize, auto-check каждые 20 сообщений) |
| M-23 | Расширение QUIZ_TOPICS | Добавить cloud, mobile, iot, blockchain. | ЧЕКЛИСТ_2026-03-09.md:93 | ✅ Done (cloud, mobile, iot, blockchain, api, phishing, forensics) |
| M-24 | Команда /help detail | Подробная справка по каждой команде с примерами. | ЧЕКЛИСТ_2026-03-09.md:90 | ✅ Done |

### Приоритетные (высокий individual impact)

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| M-25 | **HackTheBox / TryHackMe Integration** | Парсинг API, импорт машин как миссий, синхронизация прогресса. | FUTURE_VISION.md:1 | ✅ Done |
| M-26 | **Step-by-Step Exploit Walkthroughs** | После прохождения лаборатории интерактивный разбор: уязвимый код, шаги эксплуатации, root cause, рекомендации. | FUTURE_VISION.md:8 | ✅ Done |
| M-27 | **Exploit Submission (PoC verification)** | Замена флагов на скрипты-эксплойты, проверка в песочнице, автоматическая оценка. | FUTURE_VISION.md:15 | ✅ Done |
| M-28 | **Learner Dashboard (личная аналитика)** | Подробные графики: XP over time, success_rate по темам, heatmap активности. | FUTURE_VISION.md:30 | ✅ Done (basic stats + weak topics; xp over time and heatmap can be extended) |
| M-29 | **Path-based Adaptive Learning Tracks** | Обучающие треки (Web Security 101), ветвление на основе успехов, рекомендации. | FUTURE_VISION.md:37 | ✅ Done |
| M-30 | **Real-time Hints & Co-pilot** | Контекстные подсказки во время лабораторий (на основе ввода), лимит на подсказки. | FUTURE_VISION.md:45 | ✅ Done |
| M-31 | **Bug Bounty Simulation** | Симуляция bug bounty: написание отчётов, LLM-рецензирование, награды. | FUTURE_VISION.md:53 | ✅ Done |
| M-32 | **Mobile Companion App (PWA)** | Приложение для квизов и уведомлений, синхронизация прогресса. | FUTURE_VISION.md:61 | ✅ Done |
| M-33 | **Advanced Analytics & AI Tutor** | Графики прогресса, AI-рекомендации, predictive modeling. | FUTURE_VISION.md:69 | ✅ Done |
| M-34 | **Voice Assistant (TTS/STT)** | Голосовой ввод/вывод для удобства практики. | FUTURE_VISION.md:76 | ✅ Done (TTS only, STT optional) |

### Отложено / не для индивидуального использования

| ID | Задача | Причина |
|----|--------|---------|
| M-02 | Red vs Blue мультиплеер | Требует multi-user инфраструктуры |
| M-13 | SCORM / LTI | Интеграция с LMS (для учебных заведений) |
| M-14 | Плагинная архитектура | Избыточна для одного пользователя |
| M-15 | Курсы от экспертов | Будет через миссии/треки, а не отдельный контент |
| M-21 | Rate limiting | Deprecated: см. Q-05 |
| M-35 | Graceful degradation LLM | Уже сделано в Q-04 через кэш и fallback |

| M-25 | Graceful degradation LLM | Если OpenRouter недоступен, показать "LLM временно недоступна" вместо падения. | ЧЕКЛИСТ_2026-03-09.md:96 | Done |
| M-26 | Проверка длины ответа LLM | Лимит 2000 символов. | ЧЕКЛИСТ_2026-03-09.md:97 | Done |
| M-27 | Улучшение новостного парсера | Заменить html.parser на lxml, добавить обработку ошибок. | review_notes.md:245 | ✅ Done |
| M-28 | Интерактивный мастер настройки | Команда `/config` для установки провайдера, модели, API ключа вместо ручного .env. | — | ✅ Done |
| M-29 | Смена цветовой схемы | Команда `/theme` для выбора темы (dark/light/colorblind), сохранение в state. | — | ✅ Done |
| M-30 | Экспорт истории чата | Сохранение диалога в Markdown/JSON с форматированием через `/export [file]`. | — | ✅ Done |
| M-31 | Статистика использования команд | Количество вызовов каждой команды, среднее время выполнения. `/usage`. | — | ✅ Done |
| M-32 | Система feature flags | Включение/выключение модулей (social, sandbox и др.) через конфиг. `/features list`. | — | ✅ Done |
| M-33 | ADRs (Architecture Decision Records) | Deprecated: см. Q-07. | — | Deprecated |
| M-34 | Кэширование хешей PDF | Хранить хеши файлов для быстрой проверки изменений при инкрементальном обновлении. | — | ✅ Done (уже было в knowledge.py) |

---

## Low (Низкий приоритет)

Долгосрочные, "игрушечные" улучшения.

| ID | Задача | Описание | Источник | Статус |
|----|--------|----------|----------|--------|
| L-01 | Мультимодальность | Подключение LLaVA для анализа скриншотов, схем, фото штрих-кодов. | идеи.txt:115-116 | ✅ Done |
| L-02 | Трекер практических навыков | Отслеживание навыков: "написание эксплойтов", "анализ трафика", "конфигурация фаервола". | идеи.txt:149-151 | ✅ Done |
| L-03 | Mind map визуализация | Генерация структуры темы в Mermaid и рендеринг в Web UI. | идеи.txt:146-148 | ✅ Done |
| L-04 | Авто-логирование ввода | Декоратор/переопределение input() для автоматического /log без ручного ввода. | review_notes.md:267-268 | ✅ Done (уже было в main.py:465-469) |
| L-05 | Динамическая глубина объяснений | Параметр "новичок/продвинутый/эксперт" в промпт для адаптации ответов. | идеи.txt:82-85 | ✅ Done |
| L-06 | Генерация docker-compose.yml | Автоматическое создание конфигов для практических заданий. | идеи.txt:86-92 | ✅ Done |
| L-07 | Перевод на английский | Приведение всех комментариев и строк к английскому для международной поддержки. | review_notes.md:354-355 | Not started |
| L-08 | Инкрементальная индексация | Добавление только новых/изменённых PDF, без полной перестройки. | review_notes.md:371-374 | ✅ Done |
| L-09 | Модуль code review улучшения | Генерация безопасной версии кода после обнаружения уязвимости. | идеи.txt:143-145 | ✅ Done |
| L-10 | Система репутации (хэндлы) | Рейтинг известности, открытие заданий при достижении уровня. | roadmap.md:71-73 | ✅ Done |
| L-11 | Кооперативные миссии | Совместные задания для групп учеников (один атакует, другой прикрывает). | roadmap.md:74, 262-264 | Not started |
| L-12 | Командные соревнования | Создание команд, CTF между учениками, таблица лидеров. | roadmap.md:259-264 | Not started |
| L-13 | Подписка на уведомления | Уведомления о новых группировках, атаках через Telegram. | roadmap.md:306-308 | ✅ Done |
| L-14 | Экспорт диалога в Markdown | Команда /export для сохранения истории чата. | ЧЕКЛИСТ_2026-03-09.md:97 | ✅ Done (HTML/PDF/Markdown) |
| L-15 | Руководство по развертыванию | Инструкция для учебных классов: Docker Compose, настройка сети, бэкапы. | — | ✅ Done |
| L-16 | REST API для отслеживания прогресса | JSON endpoint для интеграции с внешними системами (LMS, мониторинг). | — | ✅ Done (FastAPI) |
| L-17 | Шаблоны заданий для преподавателей | YAML-шаблоны с валидацией для кастомных заданий. | — | ✅ Done |
| L-18 | Режим "наблюдатель" (teacher monitor) | Просмотр прогресса учеников, статистики по группам. | — | Not started |

---

## Done (Завершено)

Выполненные задачи текущей сессии.

| ID | Задача | Описание | Дата завершения |
|----|--------|----------|-----------------|
| D-01 | Переход на OpenRouter | Замена VL Studio на OpenRouter с моделью Nemotron 3 Nano. | 2026-03-10 |
| D-02 | Загрузка .env | Добавлен python-dotenv, создан .env для API ключа. | 2026-03-10 |
| D-03 | Исправление импортов | Исправлен импорт handle_commands в main.py. | 2026-03-10 |
| D-04 | Кэширование LLM | In-memory кэш (100 items) для экономии токенов. | 2026-03-09 |
| D-05 | Валидация промпта | Проверка пустого промпта и лимита 8000 символов. | 2026-03-09 |
| D-06 | Удаление мусора | Удалены llm.py, db_operations.py. | 2026-03-09 |
| D-07 | Характер учителя | teacher_prompt.txt + stories.json (20 историй). | 2026-03-09 |
| D-08 | LLM-based проверка ответов | question_generation.check_open_answer через LLM. | 2026-03-09 |
| D-09 | Команда /history | Показать последние 10 сообщений чата. | 2026-03-09 |
| D-10 | Команда /version | Версия + последний git commit. | 2026-03-09 |
| D-11 | Команда /add_book | Добавление PDF в knowledge_base. | 2026-03-09 |
| D-12 | Команда /clear | Очистка чата из БД. | 2026-03-09 |
| D-13 | Улучшенный news_fetcher | RSS SecurityWeek + CISA, кэш 1 час, fallback. | 2026-03-09 |
| D-14 | Unit tests | 8 тестов (quiz, news, cache, memory, config). | 2026-03-09 |
| D-15 | Форматирование | black + isort. | 2026-03-09 |
| D-16 | requirements.txt | Полный список зависимостей. | 2026-03-09 |
| D-17 | .gitignore | Исключены __pycache__, memory/, embeddings/, *.db, *.log. | 2026-03-09 |
| D-18 | Исправление generators.py | Добавлены импорты, extract_json_block, ALLOWED_TOPICS. | 2026-03-09 |
| D-19 | Проверка Docker в practice.py | Добавлена docker_available(). | 2026-03-09 |
 | D-20 | Инкрементальное обновление RAG | Перестраивается только при изменении PDF. | 2026-03-09 |
 | D-21 | Завершено цифровое меню (0-39) | Добавлены недостающие маппинги цифр 34-39 в NUMERIC_MENU (read_url, threats, groups, threat summary, cve, news search). | 2026-03-14 |
 | D-22 | Блокировка неизвестных команд | handle_commands теперь возвращает action_taken=True для неизвестных команд, предотвращая передачу в LLM. | 2026-03-14 |
 | D-23 | Удаление неиспользуемого handle_mode | Удалён импорт и экспорт handle_mode из handlers/__init__.py (функция отсутствовала). | 2026-03-14 |
| D-24 | Tests for risk_level integration | Created test_risk_integration.py with 13 tests covering risk mechanics, story mode adjustments, and study_context integration. | 2026-03-14 |
| D-25 | Tests for /social command | Created test_social.py with 9 tests covering scenarios, evaluation, invalid input. | 2026-03-14 |
| D-26 | UTF-8 encoding fix for Windows | Created utils/console_encoding.py, integrated into main.py. Solved UnicodeEncodeError for emojis/special chars. | 2026-03-14 |
| D-27 | Threat summary with LLM analysis | Implemented handle_threat_summary() that fetches fresh news, filters threats (APT/DDoS/ransomware), and uses LLM to generate weekly summary with recommendations. | 2026-03-14 |
 | D-28 | Tests for threat summary | Created test_threat_summary.py with 4 tests covering LLM analysis, fallback, no news scenarios. | 2026-03-14 |
   | C-04 | APT досье | 27 групп JSON файлов создано, команды /threats и /groups функционируют. | 2026-03-15 |
   | C-06 | Гибридный BM25 поиск | BM25 + jieba токенизация, комбинирование с векторными results. | 2026-03-15 |
   | C-08 | Песочница для кода | Docker-песочница с валидацией, ограничениями по ресурсам, командой /sandbox. | 2026-03-15 |
   | C-09 | Адаптивный план обучения | Интерактивные квизы/задачи с оценкой ответов, weak_topics в state, приоритизация тем, команда /adaptive. | 2026-03-15 |
   | C-10 | Интервальные повторения | Упрощённый SM-2 алгоритм, review_schedule, команда /repeat, уведомление при старте о просроченных повторениях. | 2026-03-15 |
   | C-11 | Генерация конспектов | Команда /summary, RAG поиск, структурированный Markdown, сохранение в файл. | 2026-03-15 |
    | C-12 | Автоматическая генерация writeup | После активности (квиз/задание) генерировать структурированный отчёт в Markdown с анализом, рекомендациями, ссылками на источники. | 2026-03-15 |
    | C-13 | Расширенные достижения | Добавлены ачивки: Social Engineer, APT Hunter, Ghost in the Shell, Snowden с описаниями и XP-бонусами. | 2026-03-18 |
    | C-14 | Магазин / прокачка | За XP покупать инструменты, темы, косметику, подсказки. Полная интеграция в handlers и state. | 2026-03-18 |


---

## 📊 Статистика плана

- **Всего задач:** ~171 (всех категорий, включая REF-01..REF-15)
- **Blocker:** 5 ✅ Все выполнены
- **Critical:** 14 (C-01..C-14 ✅)
- **High:** 18 (H-13..H-16 ✅; H-08 ✅)
- **Medium:** 34 (M-03, M-05, M-06, M-07, M-08, M-10, M-11, M-12, M-16, M-18, M-20, M-32 ✅)
- **Low:** 18 (L-01, L-02, L-03, L-05, L-06, L-08, L-09, L-10, L-13, L-14, L-15, L-16, L-17 ✅)
- **Refactoring:** 15 (REF-02, REF-03, REF-06, REF-08, REF-14 ✅; остальные ⏳)
- **Done:** 105 (все Q, B, C + H-08, H-16 + новые M + L + REF)
- **Partially:** 1 (M-17)

---

## 🎯 Следующие шаги (приоритеты на ближайшие сессии)

### Immediate: Refactoring (сроки: 1-2 недели)
После модуляризации state — укрепим архитектуру:

1. **REF-05**: Устранить циклические импорты (Mode enum → `types.py`) ✅ Быстро
2. **REF-08**: Вынести `check_achievements` в `services/achievement_service.py` ✅ Средняя сложность
3. **REF-06**: Заменить `__getattr__` на явные property ⏳ Средняя сложность
4. **REF-07**: Pydantic для валидации состояния ⏳ Средняя сложность
5. **REF-13**: Объединить мелкие state модули (10 → 4) ⏳ Низкая сложность

### Feature: Качество кода
- **REF-09**: Валидация входных данных при загрузке JSON
- **REF-10**: `.env` поддержка для всех секретов
- **REF-12**: Вынести пути в конфигурацию

### Отложенные или удалённые задачи
- **L-07, L-11, L-12, L-18**: низкий приоритет
- **REF-04**: Dependency Injection — масштабный рефакторинг, отложено

### Что уже Done (не трогать)
- Все C-01..C-14 (вкл. расширенные достижения и магазин)
- H-08, H-13..H-16 (Telegram бот, мульти-провайдер, async)
- M-03, M-05, M-06, M-07, M-08, M-10, M-11, M-12, M-16, M-18, M-20, M-32
- M-24..M-34 (все завершены)
- L-01, L-02, L-03, L-05, L-06, L-08, L-09, L-10, L-13, L-14, L-15, L-16, L-17
- REF-02, REF-03, REF-06 (частично), REF-08 (частично), REF-14

---

## 💡 Идеи и brainstorm

Записки для будущего развития. Не привязаны к приоритетам.

### Сообщество и совместное обучение
- Multi-user режим (несколько учеников в одной сессии)
- Shared whiteboard — пошаговое решение задач вместе в реальном времени
- Peer review — ученики проверяют writeup друг друга
- Community challenges — еженедельные CTF от сообщества, таблица лидеров

### Контент и учебные программы
- Curriculum Builder — визуальный конструктор программ (drag-n-drop темы)
- Auto-alignment — автоматическое сопоставление тем с MITRE ATT&CK, NIST, OWASP
- Lesson plans — готовые занятия на 90 минут с таймером и сценарием
- Prerequisites graph — граф зависимостей тем, рекомендации "что изучать дальше"

### AI Teacher улучшения
- Persona marketplace — обмен промптами персон (like GPTs)
- Context-aware hints — учитель подсказывает исходя из контекста, без спойлеров
- Mistake patterns — сбор типичных ошибок → улучшение курсов
- Socratic mode — учитель только задаёт наводящие вопросы (не даёт ответ)

### Безопасность и Compliance
- GDPR/FERPA compliance mode — анонимизация, экспорт/удаление данных
- Secure sandbox escape detection — мониторинг контейнера на выход за пределы
- Secret scanning — автоматический scan кода на API keys/credentials

### Аналитика и отчёты (для админов)
- Student dashboard — прогресс по ученикам (heatmap активности, слабые темы)
- Predictive dropout — ML модель для выявления риска прекращения обучения
- Auto-generated progress reports (PDF) для родителей/преподавателей

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
- PWA (Progressive Web App) — иконка, offline кэш ✅ Done
- Push notifications для напоминаний (repeat, new content)

### Управление файлами
- Versioning uploads (как Git для PDF)
- Bulk operations (загрузка папки с курсом)
- File sharing между учениками (с одобрением админа)

---

## 📊 Сессия 2026-05-16 — Bugfix + Dedup + Daily Challenge + 12 новых фич

### Критические баги (починено)
| Баг | Файл | Фикс |
|-----|------|------|
| `CachedLLM.invoke()` возвращал `None` | `main.py:116` | Добавлен `return response` |
| 70 строк dead code | `knowledge.py:297-455` | Удалён unreachable блок |
| `handle_stats()` читал несуществующие ключи | `handlers/core.py:265` | Исправлены ключи |
| `/courses` — "временно недоступны" | `handlers/misc.py:238` | Подключено к `courses.py` |
| `/genassignment` — отключён | `handlers/core.py:392` | Восстановлен через `generators.generate_task()` |

### Дедупликация кода
| Функция | Было копий | Решение |
|---------|-----------|---------|
| `extract_json_block` | 4 | → `utils/common.py` |
| `check_open_answer` | 5 | → `utils/common.py` (heuristic) + LLM-версии в `question_generation.py`, `generators.py` |
| `_ask_confirm()` | 2 | → `utils/common.py` |
| `clear_chat_db()` | 2 | → `utils/common.py` |

### Мёртвый код (удалено)
- `StudentLevel`, `AssessmentResult`, `ASSESSMENT_TOPICS`, `LevelAssessor` из `pedagogy.py` (~130 строк)
- `is_cybersecurity_related()` и `Task` dataclass из `main.py` (~12 строк)
- `downloader.py` — неиспользуемый файл

### Новые фичи (12 штук)
| ID | Фича | Команда | Описание |
|----|------|---------|----------|
| M-03 | OSINT Module | `/osint` | Поиск по никнейму, email, телефону, метаданным |
| M-05 | Historical Mode | `/timeline` | Эволюция взлома от 80-х до 2020-х |
| M-06 | Exploit Trainer | `/exploits` | Тренажёр написания эксплойтов |
| M-07 | Shodan/Censys | `/shodan`, `/censys` | Поиск устройств в интернете |
| M-08 | Malware Analysis | `/malware` | Анализ вредоносов (симуляция) |
| M-10 | Investigations | `/investigation` | Интерактивные расследования |
| M-11 | Voice STT | `/voice listen` | Распознавание речи |
| M-12 | Jupyter | `/jupyter` | Шаблоны ноутбуков |
| M-16 | Media Player | `/media` | Видео и подкасты |
| M-18 | Time Loop | `/timeloop` | Ветвящиеся сюжеты |
| M-20 | Cross-sync | `/sync` | Синхронизация прогресса |
| M-32 | PWA App | `/pwa` | Мобильное приложение |

### Статистика
- **536 тестов** проходят (было 420, +116)
- **~230 строк** дубликатов и мёртвого кода удалено
- **80+ команд** в цифровом меню
- **12 новых модулей** в handlers/

---

## 📊 Сессия 2026-05-16 #2 — L-03, L-14, L-16, H-16 + Registry Refactor

### Новые фичи (4 + рефакторинг)
| ID | Фича | Команда | Описание |
|----|------|---------|----------|
| L-03 | Mind Map | `/mindmap` | ASCII-визуализация структуры тем |
| L-14 | Extended Export | `/export extended` | Экспорт в HTML/PDF/Markdown |
| L-16 | REST API | `/api start` | FastAPI сервер для LMS интеграции |
| H-16 | Async Handlers | (internal) | Параллельные RAG + LLM запросы |
| REF-01 | Registry Pattern | (internal) | Рефакторинг handlers/core.py |

### Статистика
- **545 тестов** проходят (было 536, +9)
- **92 задачи** завершены (из ~162)
- **4 новых модуля**: mindmap, export_extended, api_server, async_handler, registry

---

## 📊 Сессия 2026-05-16 #3 — L-01, L-08, L-13, H-08

### Новые фичи (4)
| ID | Фича | Команда | Описание |
|----|------|---------|----------|
| L-01 | Multimodality (LLaVA) | `/vision` | Анализ изображений, OCR |
| L-08 | KB Manager | `/kb` | Оптимизация и переиндексация |
| L-13 | Threat Subscriptions | `/subscribe` | Подписка на угрозы |
| H-08 | Telegram Bot | `/telegram` | Бот для квизов и уведомлений |

### Статистика
- **565 тестов** проходят (было 545, +20)
- **96 задач** завершены (из ~162)
- **4 новых модуля**: kb_manager, vision, telegram_bot, subscribe

---

## 📊 Сессия 2026-05-16 #4 — State Refactoring (REF-02)

### Выполнено
| Компонент | Описание |
|-----------|----------|
| **Модульная архитектура** | `AppState` использует 10 модульных компонентов через композицию |
| **Обратная совместимость** | `__getattr__`/`__setattr__` делегируют атрибуты к модулям |
| **Методы обновлены** | Все методы делегируют к соответствующим модулям |
| **Исправлены модули** | `shop_state.py`, `persona_state.py`, `user_state.py` |
| **Исправлены тесты** | `test_user_state.py` — 3 бага исправлено |

### Созданные модули
| Файл | Строк | Ответственность |
|------|-------|-----------------|
| `achievements_state.py` | 89 | Достижения, XP, счётчики |
| `explanation_state.py` | 22 | Глубина объяснений |
| `hints_state.py` | 15 | Подсказки |
| `learning_state.py` | 57 | Курсы, темы, контекст |
| `metrics_state.py` | 44 | Метрики, rate limiting |
| `persona_state.py` | 14 | Персона, режим |
| `risk_state.py` | 35 | Уровень риска |
| `shop_state.py` | 61 | Магазин, темы, XP boost |
| `user_state.py` | 69 | Профиль, репутация, HTB |
| `voice_state.py` | 22 | Голосовой помощник |

### Статистика
- **577/579 тестов** проходят (2 ошибки — проблемы окружения Windows)
- **0 фейлов** — все assertions проходят
- **state.py:** 1019 → 885 строк (-13%)
- **Модульная архитектура:** 10 файлов, ~428 строк суммарно

---

### Оставшиеся задачи рефакторинга

| ID | Задача | Приоритет | Сложность | Статус |
|----|--------|-----------|-----------|--------|
| REF-04 | Dependency Injection вместо глобального singleton | 🟡 Medium | Высокая | ⏳ Planned |
| REF-05 | Устранить циклические импорты (Mode enum → `shared_types.py`) | 🟡 Medium | Низкая | ✅ Done |
| REF-06 | Заменить `__getattr__` на явные property | 🟡 Medium | Средняя | ✅ Done |
| REF-07 | Pydantic для валидации состояния | 🟡 Medium | Средняя | ✅ Done (все 10 модулей) |
| REF-08 | Вынести `check_achievements` в `services/` | 🟡 Medium | Средняя | ⏳ Planned |
| REF-09 | Валидация входных данных при загрузке JSON | 🟢 Low | Низкая | ⏳ Planned |
| REF-10 | `.env` поддержка для всех секретов | 🟢 Low | Низкая | ⏳ Planned |
| REF-12 | Вынести пути в конфигурацию | 🟢 Low | Низкая | ⏳ Planned |
| REF-13 | Объединить мелкие state модули (10 → 4) | 🟢 Low | Низкая | ⏳ Planned |

---

## 📊 Сессия 2026-05-16 #5 — Pydantic State Validation (REF-07)

### Выполнено
| Компонент | Описание |
|-----------|----------|
| **REF-05** | Mode enum → `shared_types.py`, устранены циклические импорты |
| **REF-06** | `__getattr__`/`__setattr__` → явные `@property` в `state.py` |
| **REF-07** | Все 10 state-модулей переведены на Pydantic v2 |

### Переведённые модули на Pydantic
| Файл | Валидация |
|------|-----------|
| `achievements_state.py` | `ge=0` для счётчиков, `ge=0.0` для XP |
| `user_state.py` | `ge=0` для репутации, `validate_assignment` |
| `explanation_state.py` | `validate_assignment` |
| `hints_state.py` | `ge=0` для кредитов, `gt=0` для cooldown |
| `learning_state.py` | `ge=0` для current_topic |
| `metrics_state.py` | `ge=0` для всех метрик |
| `persona_state.py` | `validate_assignment` |
| `risk_state.py` | `ge=0, le=100` для risk_level |
| `shop_state.py` | `ge=0` для hint_credits, XP boost |
| `voice_state.py` | `gt=0` для voice_rate |

### Статистика
- **47 тестов** проходят (state, achievements, user_state)
- **10/10 модулей** состояния теперь с Pydantic валидацией
- **0 фейлов** — полная обратная совместимость

---

*Примечание: Приоритеты могут меняться в зависимости от обратной связи и потребностей обучения.*
