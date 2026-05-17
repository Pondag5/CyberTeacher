"""
🐛 Bug Bounty Simulation (M-31)

Interactive simulation of bug hunting and report writing.
Learner discovers a simulated vulnerability and writes a professional report.
LLM acts as triage reviewer, scoring the report and awarding XP.
"""

import logging
import time
import uuid
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from config import get_llm
from di import get_context

logger = logging.getLogger(__name__)
console = Console()

# Sample scenarios for bug bounty simulation
BOUNTY_SCENARIOS = [
    {
        "id": "sqli_login",
        "title": "SQL Injection in Login Form",
        "description": "Login form vulnerable to SQL injection due to unsanitized user input in SQL query.",
        "vulnerability": "SQL Injection",
        "context": "Tech stack: PHP + MySQL. Error messages are disabled.",
        "expected_cwe": "CWE-89",
    },
    {
        "id": "xss_reflected",
        "title": "Reflected XSS in Search",
        "description": "The search functionality reflects user input on the results page without proper escaping.",
        "vulnerability": "Cross-Site Scripting (XSS)",
        "context": "The input is inserted into HTML body via JavaScript innerHTML.",
        "expected_cwe": "CWE-79",
    },
    {
        "id": "csrf_profile",
        "title": "CSRF in Profile Update",
        "description": "The user profile update endpoint accepts POST requests without CSRF tokens.",
        "vulnerability": "Cross-Site Request Forgery (CSRF)",
        "context": "The endpoint is at /profile/update and changes email and password.",
        "expected_cwe": "CWE-352",
    },
    {
        "id": "file_upload",
        "title": "Unrestricted File Upload",
        "description": "Image upload accepts any file type and stores in web directory without validation.",
        "vulnerability": "Unrestricted File Upload",
        "context": "Uploaded files are served from /uploads/. No type validation.",
        "expected_cwe": "CWE-434",
    },
    {
        "id": "idor",
        "title": "Insecure Direct Object Reference (IDOR)",
        "description": "Accessing other users' data is possible by changing a numeric ID in the URL.",
        "vulnerability": "IDOR",
        "context": "API endpoint: GET /api/orders/{order_id}. No ownership check.",
        "expected_cwe": "CWE-639",
    },
]


def _select_scenario():
    """Select a random scenario for the bounty hunt"""
    import random

    scenario = random.choice(BOUNTY_SCENARIOS)
    return scenario


def _get_llm_review(report: dict) -> dict:
    """Send report to LLM for review and get score/feedback"""
    llm = get_llm()
    prompt = (
        "Ты — эксперт по безопасности, работающий в bug bounty программе. "
        "Оцени этот отчёт об уязвимости.\n\n"
        "Отчет:\n"
        "---\n"
        f"Название: {report['title']}\n"
        f"Тип уязвимости: {report['vulnerability']}\n"
        f"Описание: {report['summary']}\n"
        "Шаги воспроизведения:\n"
        f"{report['steps']}\n"
        f"Влияние: {report['impact']}\n"
        f"Рекомендуемое исправление: {report['fix']}\n"
        "---\n\n"
        "Оцени по критериям (0-100):\n"
        "1. Полнота (описывает ли уязвимость, шаги, impact, fix)\n"
        "2. Ясность и структура\n"
        "3. Техническая точность\n"
        "4. Практическая применимость (можно ли воспроизвести)\n\n"
        "Верни JSON:\n"
        "{\n"
        '  "score": <int 0-100>,\n'
        '  "feedback": "<краткий отзыв на русском, 1-2 абзаца>",\n'
        '  "strengths": ["список", "сильных", "сторон"],\n'
        '  "improvements": ["что", "улучшить"],\n'
        '  "badges": ["clear", "thorough", "technical", "concise"]\n'
        "}"
    )

    try:
        response = llm.invoke(prompt)
        # Parse JSON from response
        import json

        # Try to extract JSON block
        text = response.content if hasattr(response, "content") else str(response)
        # Find JSON braces
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = text[start:end]
            result = json.loads(json_str)
            return result
        else:
            # Fallback: parse manually
            return {
                "score": 50,
                "feedback": "Невозможно распарсить ответ LLM. Отчёт принят, но перепроверь форматирование.",
                "strengths": [],
                "improvements": ["Структурируй ответ в JSON"],
                "badges": [],
            }
    except Exception as e:
        logger.error(f"LLM review failed: {e}")
        return {
            "score": 30,
            "feedback": f"Ошибка при проверке: {e}. Отчёт сохранён, но получите низкий балл.",
            "strengths": [],
            "improvements": ["Попробуйте ещё раз"],
            "badges": [],
        }


def handle_bounty(action: str = "bounty", args: str = "") -> tuple[bool, str, Any]:
    """Bug bounty simulation command"""
    ctx = get_context()
    state = ctx.state

    # For now, only interactive start; subcommands could be added later
    if action != "bounty" and not action.startswith("bounty "):
        return False, "❌ Использование: /bounty (интерактивный режим)", None

    console.print(
        Panel(
            "🐛 Bug Bounty Simulation\n"
            "Вы — white-hat хакер. Вам предоставлен тестовый стенд с уязвимостью.\n"
            "Ваша задача: составить профессиональный отчет для разработчиков.",
            title="Bug Bounty",
            border_style="magenta",
        )
    )

    # Select scenario
    scenario = _select_scenario()
    console.print(f"\n[bold cyan]Цель:[/bold cyan] {scenario['title']}")
    console.print(f"[dim]{scenario['description']}[/dim]")
    console.print(f"[yellow]Контекст:[/yellow] {scenario['context']}\n")

    # Interactive report collection
    console.print("[bold]Заполните отчет:[/bold]\n")
    title = Prompt.ask("Краткий заголовок отчета", default=scenario["title"])
    vuln_type = Prompt.ask("Тип уязвимости", default=scenario["vulnerability"])
    summary = Prompt.ask("Краткое описание уязвимости (что, где, как)")
    steps = Prompt.ask("Шаги воспроизведения (пошагово)", default="1. ...\n2. ...")
    impact = Prompt.ask("Возможный ущерб/риски (что может сделать атакующий)")
    fix = Prompt.ask("Рекомендуемое исправление (как починить)")

    report_id = str(uuid.uuid4())[:8]
    report = {
        "id": report_id,
        "timestamp": time.time(),
        "scenario_id": scenario["id"],
        "title": title,
        "vulnerability": vuln_type,
        "summary": summary,
        "steps": steps,
        "impact": impact,
        "fix": fix,
    }

    console.print("\n[bold]📤 Отправляю отчет на триаж...[/bold]")
    review = _get_llm_review(report)

    score = review.get("score", 0)
    feedback = review.get("feedback", "Нет отзыва")
    badges = review.get("badges", [])
    strengths = review.get("strengths", [])
    improvements = review.get("improvements", [])

    # Calculate XP reward: base 50 + score*2
    xp_earned = 50 + int(score * 2)
    state.points += xp_earned

    # Save report with review
    report["review"] = review
    report["xp_earned"] = xp_earned
    if not hasattr(state, "bounty_reports"):
        state.bounty_reports = []
    state.bounty_reports.append(report)
    ctx.save_state()

    # Display results
    result_lines = [
        "[bold green]✅ Отчет принят![/bold green]",
        f"ID отчета: [cyan]{report_id}[/cyan]",
        f"Набрано: [yellow]{score}[/yellow]/100 баллов",
        f" XP получено: [bold]{xp_earned}[/bold]",
        "",
        "[bold]Отзыв эксперта:[/bold]",
        feedback,
    ]
    if strengths:
        result_lines.append("\n[bold]💪 Сильные стороны:[/bold]")
        for s in strengths:
            result_lines.append(f"  • {s}")
    if improvements:
        result_lines.append("\n[bold]🔧 Что улучшить:[/bold]")
        for i in improvements:
            result_lines.append(f"  • {i}")
    if badges:
        result_lines.append(f"\n[bold]🏷️ Значки:[/bold] {' '.join(badges)}")

    console.print(
        Panel("\n".join(result_lines), border_style="green", title="Результат")
    )

    return True, "Bug bounty отчет завершён.", None
