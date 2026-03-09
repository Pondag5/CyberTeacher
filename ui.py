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
    menu = """
[bold cyan]МЕНЮ:[/bold cyan]

  [green]/teacher[/green]   - Режим учителя
  [blue]/expert[/blue]      - Экспертный режим
  [red]/ctf[/red]          - CTF режим
  [yellow]/quiz[/yellow]    - Викторина
  [magenta]/review[/magenta] - Анализ кода

[dim]Основные команды: help, stats, clear, menu, exit[/dim]
    """
    console.print(menu)

def show_help():
    help_text = """
[bold cyan]КОМАНДЫ:[/bold cyan]
  /quiz         - Викторина
  /task         - Задание
  /story        - Режим истории (20 эпизодов)
  /flag         - Проверить флаг
  /achievements - Достижения
  /writeup      - Шаблон writeup
  /practice     - Практика (CTF/HTB)
  /lab          - Docker лаборатории
  /courses      - Учебные курсы
  /news         - Новости
  /guide        - Гайд по VM
  /stats        - Статистика
  /check        - Проверить контейнеры
  /terminal     - Лог терминала
  /help         - Справка
  /exit         - Выход
    """
    console.print(help_text)

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
