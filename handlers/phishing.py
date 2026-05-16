# handlers/phishing.py — Конструктор фишинговых писем (M-04)
"""Создание и оценка фишинговых писем через LLM."""

import json
import random
from typing import Any

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()

PHISHING_TEMPLATES = {
    "bank": {
        "name": "Фишинг банка",
        "scenario": "Поддельное письмо от банка с просьбой подтвердить данные карты",
        "elements": ["логотип банка", "срочность", "ссылка на фейковый сайт", "форма ввода данных"],
    },
    "password_reset": {
        "name": "Сброс пароля",
        "scenario": "Фейковое письмо о сбросе пароля корпоративной учётки",
        "elements": ["корпоративный стиль", "кнопка сброса", "дедлайн", "поддельный sender"],
    },
    "invoice": {
        "name": "Фейковый счёт",
        "scenario": "Письмо с вложением-счётом, содержащим макрос-вирус",
        "elements": ["вложение Excel/PDF", "срочная оплата", "знакомый отправитель", "макрос"],
    },
    "ceo_fraud": {
        "name": "CEO Fraud (BEC)",
        "scenario": "Письмо от 'гендиректора' с просьбой срочного перевода",
        "elements": ["имитация CEO", "конфиденциальность", "срочность", "wire transfer"],
    },
    "oauth": {
        "name": "OAuth фишинг",
        "scenario": "Поддельная страница авторизации через Google/Microsoft",
        "elements": ["OAuth consent screen", "поддельный домен", "permissions request", "token theft"],
    },
}

PHISHING_CRITERIA = [
    "Социальная инженерия (urgency, authority, familiarity)",
    "Техническая реализация (спуфинг домена, подделка sender)",
    "Визуальная достоверность (логотипы, стиль, форматирование)",
    "Обход фильтров (текст vs картинки, обход спам-фильтров)",
    "Целевая подготовка (reconnaissance, персонализация)",
]


def handle_phishing(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Конструктор фишинговых писем."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        console.print(Panel(
            "[bold cyan]📧 Конструктор фишинговых писем[/bold cyan]\n\n"
            "Использование:\n"
            "  /phishing generate [тип]  — сгенерировать письмо\n"
            "  /phishing analyze         — проанализировать своё письмо\n"
            "  /phishing templates       — показать шаблоны\n"
            "  /phishing tips            — советы по распознаванию\n\n"
            "Типы: bank, password_reset, invoice, ceo_fraud, oauth",
            title="ФИШИНГ КОНСТРУКТОР",
            border_style="cyan",
        ))
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "templates":
        _show_templates()
        return True, None, None, True

    if subcommand == "tips":
        _show_tips()
        return True, None, None, True

    if subcommand == "generate":
        template_type = parts[2].strip() if len(parts) >= 3 else None
        return _generate_phishing(template_type)

    if subcommand == "analyze":
        return _analyze_phishing()

    console.print("[yellow]Неизвестная подкоманда. Используй /phishing для справки.[/yellow]")
    return True, None, None, True


def _show_templates() -> None:
    """Показать доступные шаблоны."""
    console.print("[bold cyan]📋 Шаблоны фишинговых писем[/bold cyan]\n")
    for tid, t in PHISHING_TEMPLATES.items():
        console.print(f"[bold]{t['name']}[/bold] [dim]({tid})[/dim]")
        console.print(f"  Сценарий: {t['scenario']}")
        console.print(f"  Элементы: {', '.join(t['elements'])}")
        console.print()


def _show_tips() -> None:
    """Советы по распознаванию фишинга."""
    tips = [
        "🔍 Проверяйте URL — наведите на ссылку, не кликая",
        "📧 Смотрите на адрес отправителя — spoofing часто выдаёт подделку",
        "⏰ Фишинг часто использует срочность — 'срочно подтвердите!'",
        "📎 Не открывайте вложения от неизвестных отправителей",
        "🔑 Никогда не вводите пароли по ссылкам из писем",
        "🏢 При подозрении — свяжитесь с отправителем другим каналом",
        "📝 Обращайте внимание на орфографию — фишинговые письма часто с ошибками",
        "🔒 Проверяйте HTTPS и сертификат на страницах входа",
    ]
    console.print(Panel(
        "\n".join(tips),
        title="🛡️ РАСПОЗНАВАНИЕ ФИШИНГА",
        border_style="green",
    ))


def _generate_phishing(template_type: str | None) -> tuple[bool, Any | None, Any | None, bool]:
    """Сгенерировать фишинговое письмо через LLM."""
    from config import LazyLoader

    if template_type and template_type not in PHISHING_TEMPLATES:
        console.print(f"[red]❌ Тип '{template_type}' не найден[/red]")
        console.print("[dim]Доступные: " + ", ".join(PHISHING_TEMPLATES.keys()) + "[/dim]")
        return True, None, None, True

    if not template_type:
        template_type = random.choice(list(PHISHING_TEMPLATES.keys()))

    template = PHISHING_TEMPLATES[template_type]

    llm = LazyLoader.get_llm()
    if llm is None:
        console.print("[red]❌ LLM недоступна[/red]")
        return True, None, None, True

    prompt = f"""Ты — эксперт по социальной инженерии (в образовательных целях).
Создай пример фишингового письма для обучения кибербезопасности.

Тип: {template['name']}
Сценарий: {template['scenario']}
Ключевые элементы: {', '.join(template['elements'])}

Создай:
1. Subject (тема письма)
2. Sender (отправитель)
3. Body (тело письма)
4. Объясни, какие техники социальной инженерии использованы
5. Покажи, как распознать этот фишинг

ВАЖНО: Это образовательный пример. Не используй реальные данные компаний."""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        console.print(Panel(
            content,
            title=f"📧 ФИШИНГ: {template['name']}",
            border_style="yellow",
        ))
        # Track usage
        state = get_state()
        state.phishing_generated = getattr(state, "phishing_generated", 0) + 1
        state.save_to_file()
    except Exception as e:
        console.print(f"[red]Ошибка генерации: {e}[/red]")

    return True, None, None, True


def _analyze_phishing() -> tuple[bool, Any | None, Any | None, bool]:
    """Проанализировать письмо пользователя."""
    from config import LazyLoader

    console.print("[bold cyan]🔍 Анализ фишингового письма[/bold cyan]")
    console.print("[dim]Вставьте текст письма (или описание). Введите /end для завершения.[/dim]\n")

    lines = []
    while True:
        try:
            line = input().strip()
            if line == "/end":
                break
            lines.append(line)
        except KeyboardInterrupt:
            break

    email_text = "\n".join(lines)
    if not email_text.strip():
        console.print("[yellow]Письмо не вставлено[/yellow]")
        return True, None, None, True

    llm = LazyLoader.get_llm()
    if llm is None:
        console.print("[red]❌ LLM недоступна[/red]")
        return True, None, None, True

    prompt = f"""Ты — эксперт по кибербезопасности. Проанализируй письмо на признаки фишинга.

Письмо:
{email_text}

Оцени по шкале 0-100 (100 = точно фишинг):
1. Вероятность фишинга (0-100)
2. Какие признаки фишинга найдены
3. Какие техники социальной инженерии использованы
4. Рекомендации: что делать с этим письмом

Верни структурированный анализ."""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        console.print(Panel(content, title="🔍 АНАЛИЗ ПИСЬМА", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Ошибка анализа: {e}[/red]")

    return True, None, None, True
