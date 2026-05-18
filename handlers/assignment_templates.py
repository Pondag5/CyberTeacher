# handlers/assignment_templates.py — YAML шаблоны заданий (L-17)
"""Конструктор кастомных заданий с валидацией через YAML."""

import os
from typing import Any

import yaml
from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()

TEMPLATES_DIR = "./assignment_templates"

DEFAULT_TEMPLATES = {
    "web_discovery": {
        "name": "Веб-разведка",
        "category": "recon",
        "difficulty": "easy",
        "description": "Найди скрытые endpoint'ы на целевом сайте",
        "objective": "Обнаружить /admin, /api/config, /.env",
        "tools": ["gobuster", "dirb", "nikto"],
        "validation": "Скриншот или список найденных endpoint'ов",
        "hints": [
            "Используй wordlist: common.txt",
            "Проверь robots.txt и sitemap.xml",
            "Попробуй разные HTTP методы",
        ],
        "xp_reward": 50,
    },
    "sqli_extract": {
        "name": "SQL Injection — извлечение данных",
        "category": "exploitation",
        "difficulty": "medium",
        "description": "Извлеки данные из БД через UNION-based SQLi",
        "objective": "Получить usernames и passwords из таблицы users",
        "tools": ["sqlmap", "burpsuite", "browser"],
        "validation": "Список credentials в формате user:pass",
        "hints": [
            "Проверь параметр id на инъекцию: ' OR 1=1--",
            "Определи количество колонов: UNION SELECT NULL,NULL",
            "Используй UNION SELECT для извлечения данных",
        ],
        "xp_reward": 100,
    },
    "xss_payload": {
        "name": "XSS — доказательство концепции",
        "category": "exploitation",
        "difficulty": "easy",
        "description": "Докажи XSS через payload",
        "objective": "Выполнить alert(1) через отражённый XSS",
        "tools": ["browser", "burpsuite"],
        "validation": "Скриншот с alert(1)",
        "hints": [
            "Попробуй <script>alert(1)</script>",
            "Если фильтр — используй <img src=x onerror=alert(1)>",
            "Проверь обход фильтра через encoding",
        ],
        "xp_reward": 75,
    },
    "priv_esc_linux": {
        "name": "Linux Privilege Escalation",
        "category": "privilege_escalation",
        "difficulty": "hard",
        "description": "Получи root доступ на Linux машине",
        "objective": "Прочитать /root/flag.txt",
        "tools": ["linpeas", "sudo -l", "find / -perm -4000"],
        "validation": "Содержимое /root/flag.txt",
        "hints": [
            "Проверь sudo -l на разрешённые команды",
            "Ищи SUID бинарники: find / -perm -4000",
            "Проверь cron job'и и writable файлы",
        ],
        "xp_reward": 150,
    },
    "crypto_basic": {
        "name": "Криптография — базовый уровень",
        "category": "cryptography",
        "difficulty": "easy",
        "description": "Расшифруй сообщение",
        "objective": "Декодировать Base64 → ROT13 → Hex",
        "tools": ["cyberchef", "python", "cyberchef"],
        "validation": "Расшифрованный текст",
        "hints": [
            "Начни с Base64 декодирования",
            "Примени ROT13 к результату",
            "Последний шаг — Hex decoding",
        ],
        "xp_reward": 40,
    },
}


def handle_assignment_templates(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Управление YAML шаблонами заданий."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        console.print(Panel(
            "[bold cyan]📋 Шаблоны заданий[/bold cyan]\n\n"
            "Использование:\n"
            "  /templates list              — показать шаблоны\n"
            "  /templates show <имя>        — показать детали\n"
            "  /templates create <имя>      — создать новый шаблон\n"
            "  /templates generate <имя>    — сгенерировать задание\n"
            "  /templates validate <файл>   — валидировать YAML\n\n"
            f"Директория: {TEMPLATES_DIR}/",
            title="ШАБЛОНЫ ЗАДАНИЙ",
            border_style="cyan",
        ))
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "list":
        return _list_templates()

    if subcommand == "show" and len(parts) >= 3:
        return _show_template(parts[2])

    if subcommand == "create" and len(parts) >= 3:
        return _create_template(parts[2])

    if subcommand == "generate" and len(parts) >= 3:
        return _generate_assignment(parts[2])

    if subcommand == "validate" and len(parts) >= 3:
        return _validate_template(parts[2])

    console.print("[yellow]Неизвестная подкоманда. /templates для справки.[/yellow]")
    return True, None, None, True


def _ensure_dir() -> None:
    """Создать директорию шаблонов если нет."""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)


def _list_templates() -> tuple[bool, Any | None, Any | None, bool]:
    """Показать список шаблонов."""
    _ensure_dir()

    # Встроенные
    console.print("[bold cyan]📚 Встроенные шаблоны:[/bold cyan]\n")
    for tid, t in DEFAULT_TEMPLATES.items():
        diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(t["difficulty"], "white")
        console.print(f"  [cyan]{tid:<20}[/cyan] [{diff_color}]{t['difficulty']}[/] — {t['name']} ({t['category']})")

    # Пользовательские
    user_templates = []
    for f in os.listdir(TEMPLATES_DIR):
        if f.endswith(".yaml") or f.endswith(".yml"):
            user_templates.append(f)

    if user_templates:
        console.print(f"\n[bold cyan]📁 Пользовательские шаблоны ({len(user_templates)}):[/bold cyan]\n")
        for f in user_templates:
            console.print(f"  [green]{f}[/green]")
    else:
        console.print(f"\n[dim]Нет пользовательских шаблонов в {TEMPLATES_DIR}/[/dim]")

    return True, None, None, True


def _show_template(name: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Показать детали шаблона."""
    template = DEFAULT_TEMPLATES.get(name)

    if not template:
        # Проверить пользовательский
        filepath = os.path.join(TEMPLATES_DIR, f"{name}.yaml")
        if not os.path.exists(filepath):
            filepath = os.path.join(TEMPLATES_DIR, f"{name}.yml")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                template = yaml.safe_load(f)

    if not template:
        console.print(f"[red]❌ Шаблон '{name}' не найден[/red]")
        return True, None, None, True

    diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(template.get("difficulty", ""), "white")

    content = (
        f"[bold]Название:[/bold] {template.get('name', '?')}\n"
        f"[bold]Категория:[/bold] {template.get('category', '?')}\n"
        f"[bold]Сложность:[/bold] [{diff_color}]{template.get('difficulty', '?')}[/]\n"
        f"[bold]Описание:[/bold] {template.get('description', '?')}\n"
        f"[bold]Цель:[/bold] {template.get('objective', '?')}\n"
        f"[bold]Инструменты:[/bold] {', '.join(template.get('tools', []))}\n"
        f"[bold]Валидация:[/bold] {template.get('validation', '?')}\n"
        f"[bold]XP награда:[/bold] {template.get('xp_reward', 0)}\n\n"
        f"[bold]Подсказки:[/bold]"
    )

    for i, hint in enumerate(template.get("hints", []), 1):
        content += f"\n  {i}. {hint}"

    console.print(Panel(content, title=f"📋 {template.get('name', name)}", border_style="cyan"))
    return True, None, None, True


def _create_template(name: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Создать новый шаблон через wizard."""
    _ensure_dir()

    filepath = os.path.join(TEMPLATES_DIR, f"{name}.yaml")
    if os.path.exists(filepath):
        console.print(f"[yellow]⚠️ Файл уже существует: {filepath}[/yellow]")
        return True, None, None, True

    console.print(f"[bold cyan]📝 Создание шаблона: {name}[/bold cyan]\n")

    # Интерактивный wizard
    fields = {
        "name": "Название задания",
        "category": "Категория (recon/exploitation/privilege_escalation/cryptography/forensics)",
        "difficulty": "Сложность (easy/medium/hard)",
        "description": "Описание",
        "objective": "Цель",
        "tools": "Инструменты (через запятую)",
        "validation": "Как валидировать результат",
        "xp_reward": "XP награда (число)",
    }

    template = {}
    for key, label in fields.items():
        value = input(f"{label}: ").strip()
        if key == "tools":
            template[key] = [t.strip() for t in value.split(",") if t.strip()]
        elif key == "xp_reward":
            try:
                template[key] = int(value)
            except ValueError:
                template[key] = 50
        else:
            template[key] = value

    # Подсказки
    console.print("\nПодсказки (пустая строка для завершения):")
    hints = []
    while True:
        hint = input(f"  Подсказка {len(hints)+1}: ").strip()
        if not hint:
            break
        hints.append(hint)
    template["hints"] = hints

    # Сохранить
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(template, f, default_flow_style=False, allow_unicode=True)

    console.print(f"[green]✅ Шаблон сохранён: {filepath}[/green]")
    return True, None, None, True


def _generate_assignment(name: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Сгенерировать задание из шаблона."""
    template = DEFAULT_TEMPLATES.get(name)

    if not template:
        filepath = os.path.join(TEMPLATES_DIR, f"{name}.yaml")
        if not os.path.exists(filepath):
            filepath = os.path.join(TEMPLATES_DIR, f"{name}.yml")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                template = yaml.safe_load(f)

    if not template:
        console.print(f"[red]❌ Шаблон '{name}' не найден[/red]")
        return True, None, None, True

    ctx = get_context()
    state = ctx.state
    state.active_assignment = {
        "template": name,
        "started_at": __import__("time").time(),
        "hints_used": 0,
        "completed": False,
    }
    state.save_to_file()

    console.print(Panel(
        f"[bold]🎯 Задание: {template.get('name', name)}[/bold]\n\n"
        f"{template.get('description', '')}\n\n"
        f"[bold]Цель:[/bold] {template.get('objective', '')}\n"
        f"[bold]Инструменты:[/bold] {', '.join(template.get('tools', []))}\n"
        f"[bold]XP награда:[/bold] {template.get('xp_reward', 0)}\n\n"
        "[yellow]Используй /hint для подсказки, /submit для отправки результата[/yellow]",
        title="АКТИВНОЕ ЗАДАНИЕ",
        border_style="green",
    ))

    return True, None, None, True


def _validate_template(filepath: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Валидировать YAML шаблон."""
    if not os.path.exists(filepath):
        # Проверить в директории шаблонов
        full_path = os.path.join(TEMPLATES_DIR, filepath)
        if not os.path.exists(full_path):
            full_path = os.path.join(TEMPLATES_DIR, f"{filepath}.yaml")
        if not os.path.exists(full_path):
            full_path = os.path.join(TEMPLATES_DIR, f"{filepath}.yml")
        filepath = full_path

    if not os.path.exists(filepath):
        console.print(f"[red]❌ Файл не найден: {filepath}[/red]")
        return True, None, None, True

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        required = ["name", "category", "difficulty", "description", "objective"]
        missing = [k for k in required if k not in data]

        if missing:
            console.print(f"[red]❌ Отсутствуют обязательные поля: {', '.join(missing)}[/red]")
            return True, None, None, True

        if data.get("difficulty") not in ("easy", "medium", "hard"):
            console.print("[red]❌ difficulty должен быть: easy, medium, или hard[/red]")
            return True, None, None, True

        console.print(Panel(
            f"[green]✅ Шаблон валиден![/green]\n\n"
            f"Файл: {filepath}\n"
            f"Полей: {len(data)}\n"
            f"Обязательные: все присутствуют",
            title="ВАЛИДАЦИЯ",
            border_style="green",
        ))
    except yaml.YAMLError as e:
        console.print(f"[red]❌ YAML ошибка: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Ошибка: {e}[/red]")

    return True, None, None, True
