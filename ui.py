from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from enum import Enum

console = Console()

class Mode(Enum):
    TEACHER = "Учитель"
    EXPERT = "Эксперт"
    CTF = "CTF"
    CODE_REVIEW = "Анализ кода"
    QUIZ = "Викторина"

def print_banner():
    banner = """
+========================================================+
|                                                        |
|   CyberTeacher v3.2 - Обучение кибербезопасности!      |
|                                                        |
|   CTF | Анализ кода | Викторины | Обучение             |
|                                                        |
+========================================================+
    """
    console.print(banner, style="bold cyan")

def show_menu():
    from config import NUMERIC_MENU
    menu = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║        CYBERTEACHER - ЦИФРОВОЕ МЕНЮ (введите цифру)          ║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]

[bold green]🎯 РЕЖИМЫ (1-5)[/bold green]
  [green] 1[/green] - Учитель (Teacher)      [blue] 2[/blue] - Эксперт (Expert)
  [red]  3[/red]  - CTF режим             [yellow] 4[/yellow] - Викторина (Quiz)
  [magenta]5[/magenta] - Анализ кода (Code Review)

[bold cyan]📊 ИНФОРМАЦИЯ & СПРАВКА (6-14)[/bold cyan]
  [cyan] 6[/cyan]  - Новости (News)         [bright_cyan] 7[/bright_cyan] - Достижения (Achievements)
  [bright_green] 8[/bright_green] - Статистика (Stats)  [bright_yellow] 9[/bright_yellow] - Справка (Help)
  [bright_magenta]10[/bright_magenta] - Подробная справка (/help detail)
  [cyan]11[/cyan]  - Гайд по VM (/guide)    [white]12[/white] - Версия (/version)
  [cyan]13[/cyan]  - Показать меню (/menu)

[bold blue]🔧 ПРАКТИКА & КУРСЫ (15-19)[/bold blue]
  [blue]14[/blue]  - Практика (Practice)     [blue]15[/blue] - Лаборатории (Lab status)
  [blue]16[/blue]  - Курсы (Courses)        [blue]17[/blue] - Режим истории (Story)
  [blue]18[/blue]  - Задание (Task)          [blue]19[/blue] - Генератор заданий (/genassignment)

[bold magenta]⚙️ УПРАВЛЕНИЕ (20-29)[/bold magenta]
  [magenta]20[/magenta] - Показать провайдера (/provider)
  [magenta]21[/magenta] - Показать модель (/model)
  [magenta]22[/magenta] - Лог терминала (/terminal)
  [magenta]23[/magenta] - Статистика кэша (/cache stats)
  [magenta]24[/magenta] - Очистить кэш (/clearcache)
  [magenta]25[/magenta] - Проверить контейнеры (/check)
  [magenta]26[/magenta] - История чата (/history)
  [magenta]27[/magenta] - Шаблон writeup (/writeup)
  [magenta]28[/magenta] - Добавить книгу (/add_book)
   [magenta]29[/magenta] - Social engineering trainer (/social)

  [bold yellow]🔍 РАЗНОЕ (30-42)[/bold yellow]
    [yellow]30[/yellow] - Проверить флаг (/flag) [нужен аргумент]
    [yellow]31[/yellow] - Записать лог (/log <cmd>)
    [yellow]32[/yellow] - Установить API ключ (/set-api-key)
    [yellow]33[/yellow] - Умный тест (/smart_test)
    [yellow]34[/yellow] - Чтение URL (/read_url)
    [yellow]35[/yellow] - Угрозы (/threats)
    [yellow]36[/yellow] - Группы APT (/groups)
    [yellow]37[/yellow] - Сводка угроз (/threat summary)
    [yellow]38[/yellow] - CVE информация (/cve)
    [yellow]39[/yellow] - Search (/news search)
    [yellow]40[/yellow] - Песочница (/sandbox <lang> <code>)
    [yellow]41[/yellow] - Адаптивные слабые темы (/adaptive)
    [yellow]42[/yellow] - Повторение (Spaced Repetition) (/repeat)

[bold red]🚪 ВЫХОД[/bold red]
  [red] 0[/red]   - Выход из приложения

[dim]Примечание: Можно также вводить команды со / (например, /news, /provider)[/dim]
[dim]Для команд с аргументами: /flag FLAG{...}, /model qwen2.5:7b, /set-api-key openrouter xxx[/dim]
    """
    console.print(menu)

def show_help():
    help_text = """
[bold cyan]КОМАНДЫ:[/bold cyan]
  /quiz         - Викторина (адаптивная, фокус на слабых темах)
  /task         - Практическое задание
  /genassignment - Сгенерировать практическое задание (CTF/лаба/упражнение)
  /progress     - Прогресс по активному заданию
  /story        - Режим истории (20 эпизодов)
  /flag         - Проверить флаг (включая из заданий)
  /achievements - Достижения
  /writeup      - Шаблон writeup
  /practice     - Практика (CTF/HTB)
  /lab          - Docker лаборатории (start/stop/status)
  /courses      - Учебные курсы
  /news         - Новости
  /guide        - Гайд по VM
  /stats        - Статистика (включает кэш и прогресс)
  /check        - Проверить контейнеры
  /terminal     - Лог терминала
  /log <cmd>    - Записать команду в лог
  /cache stats  - Статистика кэша
  /clearcache   - Очистить кэш
  /version      - Версия приложения
  /adaptive     - Показать слабые темы (адаптивное обучение)
  /help         - Справка
  /exit         - Выход
    """
    console.print(help_text)


def show_help_detail():
    """Подробная справка по каждой команде"""
    help_detail = """
[bold cyan]ПОДРОБНАЯ СПРАВКА ПО КОМАНДАМ[/bold cyan]

[green]1 /teacher[/green] — Режим учителя
  Переключение в режим учителя. Бот объясняет концепции, отвечает на вопросы подробно, использует аналогии и пошаговые объяснения. Идеально для новичков.
  Пример: /teacher

[blue]2 /expert[/blue] — Экспертный режим
  Бот выступает как эксперт в кибербезопасности. Даёт краткие точные ответы без лишних объяснений. Для продвинутых пользователей.
  Пример: /expert

[red]3 /ctf[/red] — CTF режим
  Режим Capture The Flag. Бот задаёт задачи, проверяет флаги, вестит счёт. Используйте /flag FLAG{...} для отправки.
  Пример: /ctf

[yellow]4 /quiz[/yellow] — Викторина
  Генерация случайной викторины по темам кибербезопасности. Вопросы с вариантами ответов. После прохождения начисляются очки.
  Пример: /quiz

[magenta]5 /review[/magenta] — Анализ кода
  Отправьте фрагмент кода для анализа уязвимостей. Бот проверит на опасные функции, SQL-инъекции, XSS и т.д.
  Пример: /review

[cyan]6 /news[/cyan] — Новости
  Последние новости кибербезопасности (SecurityWeek, CISA). Бот кратко переводит и комментирует.
  Пример: /news

[bright_cyan]7 /achievements[/bright_cyan] — Достижения
  Просмотр списка достижений и вашего прогресса. Можно получить за сбор флагов, прохождение курсов и т.д.
  Пример: /achievements

[bright_green]8 /stats[/bright_green] — Статистика
  Показывает статистику: очки, пройденные курсы, собранные флаги, запущенные лаборатории, кэш.
  Пример: /stats

[bright_yellow]9 /help[/bright_yellow] — Справка (эта команда)
  Показать краткую справку по командам.
  Пример: /help

[bright_red]0 /exit[/bright_red] — Выход
  Выход из приложения. Состояние сохраняется автоматически.
  Пример: /exit

[bold]Другие полезные команды:[/bold]
  /task           — Сгенерировать задание (как /quiz, но открытый ответ)
  /practice       — Практика (CTF/HTB) — показать список лаб
  /lab start <name> — Запустить Docker-лабораторию
  /lab stop <name>  — Остановить лабораторию
  /lab status       — Показать запущенные лабы
  /flag FLAG{...}   — Проверить флаг (в активном задании или глобальной базе)
  /writeup          — Шаблон для撰写 отчёта о решении задачи
  /terminal         — Показать лог терминала (последние 20 строк)
  /log <cmd>        — Записать команду в лог (для истории)
  /cache stats      — Статистика кэша ответов LLM
  /clearcache       — Очистить кэш ответов
  /version          — Версия приложения
  /guide            — Гайд по настройке VM

[dim]Примечание: можно использовать цифры 0-9 вместо команд (см. меню).[/dim]
    """
    console.print(help_detail)

def print_response(text: str, mode: str):
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
        "Викторина": "yellow"
    }
    color = color_map.get(mode, "white")
    console.print(Panel(text, title=f"БОТ: {mode}", border_style=color))

def print_thinking(thinking: str):
    console.print(Panel(thinking, title="МЫСЛИ", border_style="dim cyan", style="italic"))

def print_panel(text: str, title: str = "", border_style: str = "cyan"):
    console.print(Panel(text, title=title, border_style=border_style))

import sys
import io

def print_streaming_response(generator, mode: str, sources: list = None):
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
        "Викторина": "yellow"
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
    
    return text
