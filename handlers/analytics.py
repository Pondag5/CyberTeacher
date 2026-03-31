"""
📈 Advanced Analytics & AI Tutor (M-33)

Provides personalized insights, progress metrics, and AI-driven study recommendations.
"""

import logging
from typing import Any

from rich.bar import Bar
from rich.console import Console
from rich.table import Table

from config import get_llm
from state import get_state

logger = logging.getLogger(__name__)
console = Console()


def _compute_learning_metrics(state) -> dict[str, Any]:
    """Compute key learning metrics from state."""
    metrics = {
        "total_xp": state.points,
        "quizzes_taken": state.quizzes_taken,
        "labs_started": state.labs_started,
        "missions_completed": state.missions_completed,
        "flags_collected": state.total_flags_collected,
        "assignments_completed": state.assignments_completed,
        "tracks_enrolled": len(state.tracks_enrolled),
        "weak_topics_count": len(state.weak_topics),
        "weak_topics": state.get_weak_topics(threshold=70.0),
        "bounty_reports": len(getattr(state, "bounty_reports", [])),
    }
    # Success rate average from weak_topics (they have success_rate)
    if metrics["weak_topics"]:
        avg_weak_success = sum(t["success_rate"] for t in metrics["weak_topics"]) / len(
            metrics["weak_topics"]
        )
        metrics["avg_weak_success"] = avg_weak_success
    else:
        metrics["avg_weak_success"] = None
    return metrics


def _generate_ai_recommendation(metrics: dict[str, Any]) -> str:
    """Ask LLM for personalized study plan based on metrics."""
    llm = get_llm()
    weak_list = (
        ", ".join([t["topic"] for t in metrics["weak_topics"][:5]])
        if metrics["weak_topics"]
        else "none"
    )
    prompt = f"""Ты — AI tutor для CyberTeacher. На основе метрик ученика предложи персонализированный план на 3 дня.

Метрики:
- XP: {metrics["total_xp"]:.0f}
- Квизов: {metrics["quizzes_taken"]}
- Лабов: {metrics["labs_started"]}
- Миссий: {metrics["missions_completed"]}
- Бounty-отчётов: {metrics["bounty_reports"]}
- Слабые темы (<70%): {metrics["weak_topics_count"]} ({weak_list})
- Треков начато: {metrics["tracks_enrolled"]}

Дай конкретные рекомендации:
1. На какую тему потренироваться (выбери из слабых или предложи новую)
2. Какой тип активности (квиз, лаба, миссия, трек, bounty)
3. Пример цели на день (например, "пройти 5 квизов по SQLi")
4. Мотивирующая фраза

Ответbrief (3-4 строки), без лишних деталей."""
    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)
    except Exception as e:
        logger.error(f"AI recommendation failed: {e}")
        return "⚠️ Не удалось получить AI-рекомендацию. Проверь подключение LLM."


def handle_analytics(
    action: str = "analytics", args: str = ""
) -> tuple[bool, str, Any]:
    """Display advanced analytics and AI tutor insights."""
    state = get_state()
    metrics = _compute_learning_metrics(state)

    # Build output
    lines = []
    lines.append("[bold underline]📈 Advanced Analytics & AI Tutor[/bold underline]\n")

    # Overview metrics
    lines.append("[bold]📊 Overview:[/bold]")
    lines.append(f"  Total XP: [cyan]{metrics['total_xp']:.0f}[/cyan]")
    lines.append(f"  Quizzes taken: [cyan]{metrics['quizzes_taken']}[/cyan]")
    lines.append(f"  Labs started: [cyan]{metrics['labs_started']}[/cyan]")
    lines.append(f"  Missions completed: [cyan]{metrics['missions_completed']}[/cyan]")
    lines.append(f"  Flags collected: [cyan]{metrics['flags_collected']}[/cyan]")
    lines.append(
        f"  Assignments completed: [cyan]{metrics['assignments_completed']}[/cyan]"
    )
    lines.append(f"  Tracks enrolled: [cyan]{metrics['tracks_enrolled']}[/cyan]")
    lines.append(f"  Bounty reports: [cyan]{metrics['bounty_reports']}[/cyan]")

    # Weak topics summary
    lines.append("\n[bold]🔴 Weak Topics (Success <70%):[/bold]")
    weak = metrics["weak_topics"]
    if weak:
        # Show top 5
        for t in weak[:5]:
            sr = f"{t['success_rate']:.1f}%"
            attempts = t["attempts"]
            lines.append(
                f"  • {t['topic']}: [yellow]{sr}[/yellow] ({attempts} attempts)"
            )
        if len(weak) > 5:
            lines.append(f"  ... and {len(weak) - 5} more")
    else:
        lines.append("  [green]None – all topics >=70%![/green]")

    # Simple textual chart: XP by topic area (using weak_topics as proxy)
    if weak:
        lines.append("\n[bold]📊 Weak Topics Bar Chart (success rate):[/bold]")
        for t in weak[:5]:
            pct = int(t["success_rate"] // 10)  # 0-10 blocks
            bar = "█" * pct + "░" * (10 - pct)
            lines.append(f"  {t['topic'][:20]:20} {bar} {t['success_rate']:.1f}%")

    # AI Tutor recommendation
    lines.append("\n[bold]🤖 AI Tutor Recommendation:[/bold]")
    ai_rec = _generate_ai_recommendation(metrics)
    lines.append(f"  {ai_rec}")

    # Footer tip
    lines.append(
        "\n[dim]Tip: Use /adaptive to drill weak topics, /tracks for structured learning, /bounty for report practice.[/dim]"
    )

    return True, "\n".join(lines), None
