"""
📊 Learner Dashboard (M-28) — персональная аналитика прогресса
"""

from typing import Any

from rich.console import Console

from di import get_context

console = Console()


def handle_dashboard(action: str, args: str = "") -> tuple[bool, str, Any]:
    """Display learner dashboard with stats and insights"""
    ctx = get_context()
    state = ctx.state

    # Overview metrics
    metrics = [
        ("Total XP", f"{state.points:.0f}"),
        ("Quizzes Taken", str(state.quizzes_taken)),
        ("Labs Started", str(state.labs_started)),
        ("Missions Completed", str(state.missions_completed)),
        ("Flags Collected", str(state.total_flags_collected)),
        ("Assignments Completed", str(state.assignments_completed)),
        ("Courses Completed", str(len(state.course_progress))),
        ("Tracks Enrolled", str(len(state.tracks_enrolled))),
        ("Weak Topics", str(len(state.weak_topics))),
    ]

    # Build output with Rich markup
    lines = []
    lines.append("[bold underline]📊 Learner Dashboard[/bold underline]\n")
    lines.append("[bold]Overview:[/bold]")
    for label, value in metrics:
        lines.append(f"  {label}: [cyan]{value}[/cyan]")

    # Weak topics (need practice)
    weak = state.get_weak_topics(threshold=70.0)
    if weak:
        lines.append("\n[bold]Weak Topics (Success <70%):[/bold]")
        for t in weak[:10]:
            sr = f"{t['success_rate']:.1f}%"
            attempts = t["attempts"]
            lines.append(
                f"  • {t['topic']}: [yellow]{sr}[/yellow] ({attempts} attempts)"
            )
    else:
        lines.append(
            "\n[bold]Weak Topics:[/bold] [green]None – all topics >=70%![/green]"
        )

    # Tracks progress summary
    if state.tracks_enrolled:
        lines.append("\n[bold]Learning Tracks:[/bold]")
        try:
            from track_engine import get_track_engine

            engine = get_track_engine()
        except ImportError:
            engine = None
        for tid in state.tracks_enrolled[:3]:  # show up to 3
            prog = state.track_progress.get(tid, {})
            completed = len(prog.get("completed_topics", []))
            if engine:
                track = engine.get_track(tid)
                total = len(track.topics) if track else 0
                lines.append(f"  • {tid}: {completed}/{total} topics completed")
            else:
                lines.append(f"  • {tid}: {completed} topics completed")
        if len(state.tracks_enrolled) > 3:
            lines.append(f"  ... and {len(state.tracks_enrolled) - 3} more")

    # Activity counters
    lines.append("\n[bold]Activity Counters:[/bold]")
    lines.append(f"  Messages sent: [cyan]{state.messages_sent}[/cyan]")
    lines.append(f"  News checks: [cyan]{state.news_checked}[/cyan]")

    # SKL-02: Skill-based recommendations
    try:
        from services.skill_tracker_service import get_all_skills
        skills = get_all_skills(getattr(state, "skill_tracker", {}))
        if skills:
            low_skills = [s for s in skills if s["level"] < 3]
            if low_skills:
                lines.append("\n[bold]Рекомендации по навыкам:[/bold]")
                for s in low_skills[:5]:
                    lines.append(
                        f"  • [yellow]{s['name']}[/yellow] (lvl {s['level']}) — "
                        f"попробуй /quiz по теме '{s['name']}'"
                    )
            else:
                lines.append("\n[bold]Навыки:[/bold] [green]Все на хорошем уровне![/green]")
    except Exception:
        pass

    # Footer tip
    lines.append(
        "\n[dim]Tip: Use /adaptive to focus on weak topics. Use /tracks for structured learning paths.[/dim]"
    )

    return True, "\n".join(lines), None
