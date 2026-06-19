from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from shared_types import Mode

console = Console(legacy_windows=False, emoji=False)


def print_banner() -> None:
    banner = """
+========================================================+
|                                                        |
|   CyberTeacher v5.0 - Обучение кибербезопасности!      |
|                                                        |
|   CTF | Анализ кода | Викторины | Обучение             |
|                                                        |
+========================================================+
    """
    console.print(banner, style="bold cyan")


def show_menu() -> None:
    from config import NUMERIC_MENU

    menu = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║        CYBERTEACHER - ЦИФРОВОЕ МЕНЮ (введите цифру)          ║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]

[bold green]🎯 РЕЖИМЫ (1-5)[/bold green]
  [green] 1[/green] - Учитель (Teacher)      [blue] 2[/blue] - Эксперт (Expert)
  [red]  3[/red]  - CTF режим             [yellow] 4[/yellow] - Викторина (Quiz)
  [magenta]5[/magenta] - Анализ кода (Code Review)

[bold cyan]📊 ИНФОРМАЦИЯ & СПРАВКА (6-13)[/bold cyan]
  [cyan] 6[/cyan]  - Новости (News)         [bright_cyan] 7[/bright_cyan] - Достижения (Achievements)
  [bright_green] 8[/bright_green] - Статистика (Stats)  [bright_yellow] 9[/bright_yellow] - Справка (Help)
  [bright_magenta]10[/bright_magenta] - Подробная справка (/help detail)
  [cyan]11[/cyan]  - Гайд по VM (/guide)    [white]12[/white] - Версия (/version)
  [cyan]13[/cyan]  - Показать меню (/menu)

[bold blue]🔧 ПРАКТИКА & ОБУЧЕНИЕ (14-24)[/bold blue]
  [blue]14[/blue]  - Практика (Practice)
  [blue]15[/blue]  - HTB интеграция (/htb)
  [blue]16[/blue]  - Walkthrough (разбор)
  [blue]17[/blue]  - Exploit search (/exploit)
  [blue]18[/blue]  - Лаборатории (/lab)
  [blue]19[/blue]  - Курсы (Courses)
  [blue]20[/blue]  - Траектории (Tracks)
  [blue]21[/blue]  - Режим истории (Story)
  [blue]22[/blue]  - Задание (Task)
  [blue]23[/blue]  - Генератор заданий (/genassignment)
  [blue]24[/blue]  - Адаптивные темы (/adaptive)

[bold magenta]⚙️ УПРАВЛЕНИЕ (25-34)[/bold magenta]
  [magenta]25[/magenta] - Показать провайдера (/provider)
  [magenta]26[/magenta] - Показать модель (/model)
  [magenta]27[/magenta] - Лог терминала (/terminal)
  [magenta]28[/magenta] - Статистика кэша (/cache stats)
  [magenta]29[/magenta] - Очистить кэш (/clearcache)
  [magenta]30[/magenta] - Проверить контейнеры (/check)
  [magenta]31[/magenta] - История чата (/history)
  [magenta]32[/magenta] - Шаблон writeup (/writeup)
  [magenta]33[/magenta] - Добавить книгу (/add_book)
  [magenta]34[/magenta] - Social engineering trainer (/social)

[bold yellow]🔍 РАЗНОЕ (35-52)[/bold yellow]
  [yellow]35[/yellow] - Повторение (/repeat)
  [yellow]36[/yellow] - Генерация конспекта (/summary <тема>)
  [yellow]37[/yellow] - Авто-writeup (/auto_writeup)
  [yellow]38[/yellow] - Проверить флаг (/flag) [нужен аргумент]
  [yellow]39[/yellow] - Записать лог (/log <cmd>)
  [yellow]40[/yellow] - Установить API ключ (/set-api-key)
  [yellow]41[/yellow] - Умный тест (/smart_test)
  [yellow]42[/yellow] - Чтение URL (/read_url)
  [yellow]43[/yellow] - Угрозы (/threats)
  [yellow]44[/yellow] - Группы APT (/groups)
  [yellow]45[/yellow] - Сводка угроз (/threat summary)
  [yellow]46[/yellow] - CVE информация (/cve)
  [yellow]47[/yellow] - Search (/news search)
  [yellow]48[/yellow] - Песочница (/sandbox <lang> <code>)
  [yellow]49[/yellow] - Подсказки в реальном времени (/hint)
  [yellow]50[/yellow] - Личный дашборд (/dashboard)
    [yellow]51[/yellow] - Bug Bounty симуляция (/bounty)
    [yellow]52[/yellow] - Продвинутая аналитика и AI рекомендации (/analytics)
    [yellow]53[/yellow] - Голосовой помощник (/voice on/off/test)
    [yellow]54[/yellow] - Экспорт чата (/export [файл])
    [yellow]55[/yellow] - Статистика команд (/usage)
    [yellow]56[/yellow] - Мастер настройки (/config)
    [yellow]57[/yellow] - Тема оформления (/theme)
    [yellow]58[/yellow] - Язык интерфейса (/lang)
    [yellow]59[/yellow] - Управление модулями (/features)
    [yellow]60[/yellow] - Суммаризация истории (/summarize)
    [yellow]61[/yellow] - Конструктор фишинга (/phishing)
    [yellow]62[/yellow] - Mermaid-диаграммы (/mermaid)
    [yellow]63[/yellow] - Трекер навыков (/skills)
    [yellow]64[/yellow] - Репутация (/reputation)
    [yellow]65[/yellow] - Глубина объяснений (/depth)
    [yellow]66[/yellow] - Безопасный код (/fixcode)
    [yellow]67[/yellow] - Шаблоны заданий (/templates)
    [yellow]68[/yellow] - Эмоции учителя (/emotions)
    [yellow]69[/yellow] - Docker Compose (/dockergen)
    [yellow]70[/yellow] - CTF-флаги (/ctf)
    [yellow]71[/yellow] - Профиль (/profile)
    [yellow]72[/yellow] - Ежедневный челлендж (/daily)

  [bold red]🚪 ВЫХОД[/bold red]
  [red] 0[/red]   - Выход из приложения

[dim]Примечание: Можно также вводить команды со / (например, /news, /provider)[/dim]
[dim]Для команд с аргументами: /flag FLAG{...}, /model qwen2.5:7b, /set-api-key openrouter xxx[/dim]
    """
    console.print(menu)


def show_help() -> None:
    help_text = """
[bold cyan]КОМАНДЫ:[/bold cyan]

[bold green]🎯 РЕЖИМЫ:[/bold green]
  /teacher     - Режим учителя (объяснения, аналогии)
  /expert      - Экспертный режим (краткие ответы)
  /ctf         - CTF режим (флаги, соревнования)
  /review      - Анализ кода (безопасность)
  /hybrid      - Адаптивный режим (подстраивается под уровень)

[bold blue]📚 ОБУЧЕНИЕ:[/bold blue]
  /quiz        - Викторина (адаптивная, фокус на слабых темах)
  /task        - Практическое задание (открытый ответ)
  /genassignment - Генератор заданий (CTF/лаба)
  /story       - Режим истории (эпизоды)
  /tracks      - Учебные траектории (структурированные пути)
  /dashboard   - Личный дашборд (аналитика, слабые темы, XP)
  /bounty      - Bug Bounty симуляция (написание отчётов)
  /progress    - Прогресс по активному заданию
  /timeline    - Исторический режим (эволюция взлома)
  /investigation - Интерактивные расследования (кейсы, улики)
  /media       - Видео и подкасты (встроенный плеер)
  /timeloop    - Временная петля (ветвящиеся сюжеты)

[bold magenta]📊 ИНФОРМАЦИЯ:[/bold magenta]
  /news        - Новости кибербезопасности
  /cve         - Информация о CVE
  /threats     - APT досье (7 групп)
  /groups      - Группировка APT по странам
   /threat      - Сводка угроз (недельная)
   /stats       - Статистика (очки, курсы, флаги)
   /analytics   - Продвинутая аналитика и AI рекомендации (M-33)
   /voice       - Голосовой помощник (TTS/STT) (M-34)
    /voice listen - Распознавание речи (STT)
   /achievements- Достижения и XP
  /history     - История чата
  /guide       - Гайд по VM (Kali, HTB)

[bold yellow]🔧 ПРАКТИКА:[/bold yellow]
  /practice    - Практика (CTF/HTB)
  /htb         - Интеграция HackTheBox (машины, флаги)
  /walkthrough - Пошаговый разбор эксплойта
   /exploit     - Поиск эксплойтов по CVE
   /exploits_log- История успешных эксплойтов
  /lab         - Docker лаборатории (21 шт.)
   /courses     - Учебные курсы (6 курсов)
   /topics      - Все темы курсов (прогресс, поиск)
  /next        - Следующая тема курса
  /adaptive    - Показать слабые темы
  /repeat      - Интервальные повторения (SM-2)
  /exploits    - Тренажёр написания эксплойтов
  /jupyter     - Jupyter Notebooks (шаблоны для практики)

[bold cyan]🛠️ ИНСТРУМЕНТЫ:[/bold cyan]
  /sandbox     - Песочница для кода (Docker)
  /terminal    - Лог терминала
  /log <cmd>   - Записать команду в лог
  /read_url    - Чтение URL
  /smart_test  - Умный тест
  /osint       - OSINT разведка (симуляция: поиск, утечки, метаданные)
  /shodan      - Поиск устройств в Shodan
  /censys      - Поиск сервисов в Censys
  /malware     - Анализ вредоносов (симуляция песочницы)

[bold green]📝 ОТЧЁТЫ:[/bold green]
  /summary     - Генерация конспекта (Markdown)
   /writeup     - Шаблон writeup
   /writeups    - История writeups (поиск, просмотр)
   /auto_writeup- Автоматический writeup

[bold magenta]⚙️ УПРАВЛЕНИЕ:[/bold magenta]
  /flag        - Проверить флаг
  /provider    - Показать/сменить провайдера LLM
  /model       - Показать/сменить модель
  /set-api-key - Установить API ключ
  /risk        - Уровень риска (CTF/Story)
  /add_book    - Добавить PDF в базу знаний
  /cache stats - Статистика кэша
  /clearcache  - Очистить кэш
  /kb_status   - Статус базы знаний
  /check       - Проверить контейнеры Docker
  /version     - Версия приложения
  /clear       - Очистить чат
  /menu        - Показать цифровое меню
   /usage       - Статистика использования команд
   /heatmap     - Heatmap активности (28 дней)
  /export      - Экспорт истории чата (Markdown/JSON)
   /config      - Интерактивный мастер настройки
   /state       - Экспорт/импорт состояния (бэкапы)
   /theme       - Смена цветовой схемы
   /lang        - Язык интерфейса (ru/en)
   /features    - Вкл/выкл модулей
  /summarize   - Суммаризация истории диалога
  /phishing    - Конструктор фишинговых писем
  /mermaid     - Mermaid-инфографика
   /skills      - Трекер практических навыков
   /certificates- Сертификаты мастерства (lvl 5)
  /reputation  - Репутация и хэндлы
  /depth       - Глубина объяснений (beginner/normal/expert)
  /fixcode     - Генерация безопасной версии кода
  /templates   - YAML шаблоны заданий
  /emotions    - Эмоции учителя (sentiment-анализ)
  /dockergen   - Генерация docker-compose для лаб
  /ctf         - Динамические CTF-флаги
  /profile     - Профиль пользователя (имя, аватар, статистика)
   /daily       - Ежедневный челлендж со стриком
   /shop        - Магазин (темы, бусты, подсказки)
   /sync        - Синхронизация прогресса между устройствами
   /pwa         - Мобильное приложение (PWA)
   /versus      - LLM-Соперник (режим дуэли)
   /offline     - Офлайн-режим (без LLM)
   /mood        - Стиль общения (hacker/formal/casual/minimal)
   /api         - REST API сервер

  [bold cyan]❓ СПРАВКА:[/bold cyan]
  /help        - Краткая справка (эта команда)
  /help detail - Подробная справка с примерами
  /exit        - Выход из приложения

[dim]Примечание: можно использовать цифры 0-72 вместо команд (см. /menu).[/dim]
[dim]Для команд с аргументами: /flag FLAG{...}, /model qwen2.5:7b, /sandbox python print('hello')[/dim]
    """
    console.print(help_text)


def show_help_detail() -> None:
    """Подробная справка по каждой команде"""
    help_detail = """
[bold cyan]ПОДРОБНАЯ СПРАВКА ПО КОМАНДАМ[/bold cyan]

[bold green]🎯 РЕЖИМЫ[/bold green]

[green]/teacher[/green] — Режим учителя
  Переключение в режим учителя. Бот объясняет концепции, отвечает на вопросы подробно, использует аналогии и пошаговые объяснения. Идеально для новичков.
  Пример: /teacher

[blue]/expert[/blue] — Экспертный режим
  Бот выступает как эксперт в кибербезопасности. Даёт краткие точные ответы без лишних объяснений. Для продвинутых пользователей.
  Пример: /expert

[red]/ctf[/red] — CTF режим
  Режим Capture The Flag. Бот задаёт задачи, проверяет флаги, вестит счёт. Используйте /flag FLAG{...} для отправки.
  Пример: /ctf

[magenta]/review[/magenta] — Анализ кода
  Отправьте фрагмент кода для анализа уязвимостей. Бот проверит на опасные функции, SQL-инъекции, XSS и т.д.
  Пример: /review

[bold blue]📚 ОБУЧЕНИЕ[/bold blue]

[yellow]/quiz[/yellow] — Викторина
  Генерация случайной викторины по темам кибербезопасности. Вопросы с вариантами ответов. После прохождения начисляются очки.
  Пример: /quiz

[yellow]/task[/yellow] — Практическое задание
  Открытое задание по темам кибербезопасности. Нужно написать развёрнутый ответ. Бот оценивает и даёт обратную связь.
  Пример: /task

[magenta]/genassignment[/magenta] — Генератор заданий
  Генерация конспекта, задания, лабы или CTF-задачи по указанной теме (в разработке).
  Пример: /genassignment

[cyan]/story[/cyan] — Режим истории
  Прохождение сценариев-эпизодов с нарративом и заданиями (21 эпизод).
  Пример: /story

[cyan]/progress[/cyan] — Прогресс по заданию
  Показывает текущий прогресс по активному CTF-заданию (собрано флагов, очков).
  Пример: /progress

[bold magenta]📊 ИНФОРМАЦИЯ[/bold magenta]

[cyan]/news[/cyan] — Новости
  Последние новости кибербезопасности (SecurityWeek, CISA). Бот кратко переводит и комментирует.
  Пример: /news

[red]/cve[/red] — CVE информация
  Поиск информации об уязвимостях по ID (CVE-XXXX-XXXX).
  Пример: /cve CVE-2021-44228

[bright_cyan]/threats[/bright_cyan] — APT досье
  Показать досье на известные APT-группы (APT28, APT29, Lazarus, APT41, Sandworm, FIN7, REvil).
  Пример: /threats

[bright_cyan]/groups[/bright_cyan] — Группы APT по странам
  Группировка всех APT-групп по странам, топ-10 тактик и инструментов.
  Пример: /groups

[bright_yellow]/threat[/bright_yellow] — Сводка угроз
  Еженедельная сводка актуальных угроз (APT, DDoS, ransomware, CVE) с анализом от учителя.
  Пример: /threat

[green]/stats[/green] — Статистика
  Показывает статистику: очки, пройденные курсы, собранные флаги, запущенные лаборатории, кэш.
  Пример: /stats

[green]/achievements[/green] — Достижения
  Просмотр списка достижений и вашего прогресса. Можно получить за сбор флагов, прохождение курсов и т.д.
  Пример: /achievements

[green]/analytics[/green] — Продвинутая аналитика и AI рекомендации (M-33)
  Расширенная аналитика прогресса: очки, статистика, слабые темы, график успеваемости, AI-рекомендации по обучению на основе метрик.
  Пример: /analytics

[yellow]/voice[/yellow] — Голосовой помощник (TTS) (M-34)
  Управление голосовым выводом ответов бота. Включите, чтобы бот зачитывал свои ответы вслух.
  Команды: /voice on, /voice off, /voice test, /voice status.
  Пример: /voice on

[blue]/history[/blue] — История чата
  Показать последние сообщения из чата.
  Пример: /history

[blue]/guide[/blue] — Гайд по VM
  Инструкция по настройке виртуальных машин (Kali, HTB) для практики.
  Пример: /guide

[bold blue]🔧 ПРАКТИКА[/bold blue]

[blue]/practice[/blue] — Практика (CTF/HTB)
   Список практических заданий с фильтрацией по категориям (Web, Network, Crypto и др.).
   Пример: /practice

[blue]/htb[/blue] — Интеграция HackTheBox
   Работа с HackTheBox: авторизация, просмотр машин, отправка флагов, получение walkthrough.
   Примеры: /htb login, /htb machines, /htb submit, /htb walkthrough <id>
   Команды: login, machines, machine <id>, walkthrough <id>, submit <id> <flag>, sync, status

[blue]/walkthrough[/blue] — Пошаговый разбор эксплойта
   Генерация детального пошагового гайда по эксплуатации уязвимости (SQLi, XSS, Buffer Overflow и т.д.).
   Пример: /walkthrough SQL Injection

[blue]/exploit[/blue] — Поиск эксплойтов
   Поиск готовых эксплойтов для CVE. Поддерживает только CVE-ID.
   Пример: /exploit CVE-2021-44228

[blue]/lab[/blue] — Docker лаборатории
  Управление лабораториями: /lab start <name>, /lab stop <name>, /lab status, /lab list.
  Пример: /lab start dvwa

[blue]/courses[/blue] — Учебные курсы
  Список доступных курсов, прогресс, прохождение тем.
  Пример: /courses

[blue]/tracks[/blue] — Учебные траектории
  Структурированные learning paths с последовательными темами, адаптивным подбором и отслеживанием прогресса. Команды: /tracks list, /tracks start <id>, /tracks next, /tracks progress.
  Пример: /tracks list

[blue]/dashboard[/blue] — Личный дашборд
  Показывает обзор прогресса: XP, статистику, слабые темы, активность по трекам.
  Пример: /dashboard

[blue]/next[/blue] — Следующая тема курса
  Переход к следующей теме в текущем курсе.
  Пример: /next

[yellow]/adaptive[/yellow] — Адаптивные слабые темы
  Показывает темы, в которых вы допускаете ошибки (успешность <70%). Рекомендуется потренировать их через /quiz.
  Пример: /adaptive

[magenta]/bounty[/magenta] — Bug Bounty симуляция
  Интерактивное написание отчёта об уязвимости. LLM выступает в роли триage-рецензента, оценивает отчёт и начисляет XP.
  Пример: /bounty

[yellow]/repeat[/yellow] — Интервальные повторения
  Показывает темы, готовые к повторению (алгоритм SuperMemo SM-2), и запускает квиз для повторения.
  Пример: /repeat

[bold cyan]🛠️ ИНСТРУМЕНТЫ[/bold cyan]

[magenta]/sandbox[/magenta] — Песочница для кода
  Запуск пользовательского кода (Python, Bash) в изолированном Docker-контейнере с ограничениями (256MB RAM, no network).
  Пример: /sandbox python "print('hello')"
  Пример: /sandbox bash "ls -la"

[cyan]/terminal[/cyan] — Лог терминала
  Показать последние команды, которые вы запускали в контексте обучения.
  Пример: /terminal

[cyan]/log <cmd>[/cyan] — Записать команду в лог
  Записать команду в историю терминала (для последующего анализа).
  Пример: /log nmap -sS target

[bright_cyan]/read_url[/bright_cyan] — Чтение URL
  Загрузить и проанализировать содержимое веб-страницы (используется RAG для ответа).
  Пример: /read_url https://example.com

[bright_magenta]/smart_test[/bright_magenta] — Умный тест
  Генерация адаптивного теста по выбранной теме с вопросами разного типа.
  Пример: /smart_test

[bold green]📝 ОТЧЁТЫ[/bold green]

[green]/summary[/green] — Генерация конспекта
  Создание Markdown-конспекта по указанной теме с примерами и выводами.
  Пример: /summary "SQL инъекции"

[green]/writeup[/green] — Шаблон writeup
  Получить структурированный шаблон для отчёта о решении CTF-задачи.
  Пример: /writeup

[green]/auto_writeup[/green] — Автоматический writeup
  Автоматическая генерация отчёта по последней завершённой активности (квиз, задание, эпизод).
  Пример: /auto_writeup

[bold magenta]⚙️ УПРАВЛЕНИЕ[/bold magenta]

[magenta]/flag[/magenta] — Проверить флаг
  Проверка флага (например, FLAG{...}) на правильность. Можно использовать в CTF-режиме или в активном задании.
  Пример: /flag FLAG{SQLi_is_awesome}

[magenta]/exploit_submit[/magenta] — Отправить PoC (эксплойт-скрипт)
  Для миссий, где шаг требует PoC verification. Запускает скрипт в песочнице и проверяет вывод на ожидаемый флаг.
  Миссия должна иметь step с accepts_exploit: true и exploit_validation.
  Пример: /exploit_submit intro_web 1 exploit.py

[magenta]/provider[/magenta] — Провайдер LLM
  Показать или сменить провайдера (ollama, openrouter, huggingface).
  Пример: /provider
  Пример: /provider openrouter

[magenta]/model[/magenta] — Модель LLM
  Показать или сменить модель (qwen2.5:7b, mistral, llama2 и др.).
  Пример: /model
  Пример: /model qwen2.5:7b

[magenta]/set-api-key[/magenta] — Установить API ключ
  Установка API ключа для OpenRouter или другого облачного провайдера.
  Пример: /set-api-key openrouter sk-...

[red]/risk[/red] — Уровень риска
  Показать текущий уровень риска (CTF/Story режимы) или установить значение вручную.
  Пример: /risk
  Пример: /risk 30

[yellow]/add_book[/yellow] — Добавить PDF в базу знаний
  Загрузка PDF-файла в RAG базу знаний для последующего поиска.
  Пример: /add_book /path/to/book.pdf

[cyan]/hint[/cyan] — Подсказки в реальном времени (M-30)
  Автоматические контекстные подсказки при вводе команд (nmap, sqlmap и др.). Тратит кредиты и снижает XP.
  Пример: /hint on|off|status|get|clear
  • on/off — включить/выключить авто-подсказки
  • status — статистика
  • get — получить ручную подсказку
  • clear — сбросить счётчики

[cyan]/cache stats[/cyan] — Статистика кэша
  Показать hit rate, размер кэша ответов LLM.
  Пример: /cache stats

[cyan]/clearcache[/cyan] — Очистить кэш
  Очистка кэша ответов LLM (все записи).
  Пример: /clearcache

[cyan]/kb_status[/cyan] — Статус базы знаний
  Информация о количестве файлов, чанков, последних добавленных документах.
  Пример: /kb_status

[cyan]/check[/cyan] — Проверить контейнеры Docker
  Статус всех запущенных лабораторий, использование ресурсов.
  Пример: /check

[blue]/version[/blue] — Версия приложения
  Показать версию и информацию о сборке.
  Пример: /version

[blue]/clear[/blue] — Очистить чат
  Удалить историю сообщений в текущем сеансе.
  Пример: /clear

[blue]/menu[/blue] — Показать цифровое меню
  Отобразить числовое меню (0-44) для быстрого выбора команд.
  Пример: /menu

[bold cyan]❓ СПРАВКА[/bold cyan]

[green]/help[/green] — Краткая справка
  Показать компактный список команд (эта команда).
  Пример: /help

[green]/help detail[/green] — Подробная справка
  Полное описание всех команд с примерами использования.
  Пример: /help detail

[red]/exit[/red] — Выход
  Выход из приложения. Состояние сохраняется автоматически.
  Пример: /exit

[dim]Примечание: команды можно вводить без косой черты, если это цифра из меню (0-53).[/dim]
[dim]Команды с аргументами: /flag FLAG{...}, /model qwen2.5:7b, /sandbox python "print('hello')", /summary "SQL инъекции"[/dim]
    """
    console.print(help_detail)


def print_response(text: str, mode: str) -> None:
    color_map = {
        "teacher": "green",
        "expert": "blue",
        "ctf": "red",
        "code_review": "magenta",
        "quiz": "yellow",
        "Учитель": "green",
        "Эксперт": "blue",
        "CTF": "red",
        "Code Review": "magenta",
        "Анализ кода": "magenta",
        "Викторина": "yellow",
    }
    color = color_map.get(mode, "white")
    console.print(Panel(text, title=f"БОТ: {mode}", border_style=color))


def print_thinking(thinking: str) -> None:
    console.print(
        Panel(thinking, title="МЫСЛИ", border_style="dim cyan", style="italic")
    )


def print_panel(text: str, title: str = "", border_style: str = "cyan") -> None:
    console.print(Panel(text, title=title, border_style=border_style))


import io
import sys


def print_streaming_response(
    generator: Any, mode: str, sources: list[str] | None = None
) -> None:
    """Вывод ответа без стриминга (для Windows)"""
    color_map = {
        "teacher": "green",
        "expert": "blue",
        "ctf": "red",
        "code_review": "magenta",
        "quiz": "yellow",
        "Учитель": "green",
        "Эксперт": "blue",
        "CTF": "red",
        "Анализ кода": "magenta",
        "Викторина": "yellow",
    }
    color = color_map.get(mode, "white")

    # Собираем весь ответ
    text = ""
    for chunk in generator:
        text += chunk

    # Выводим весь текст
    if text:
        console.print(Panel(text, title=f"БОТ: {mode.upper()}", border_style=color))

    if sources:
        console.print(f"[dim]Источники: {', '.join(sources)}[/dim]")
