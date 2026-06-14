"""Network topology visualization (ASCII)"""

from typing import Any, Tuple
from rich.console import Console
from rich.tree import Tree

from di import get_context
from handlers.types import HandlerResult


console = Console()


def get_container_status(container_name: str) -> dict[str, bool]:
    """Заглушка – возвращает статус контейнера."""
    # В реальности здесь был бы вызов Docker API
    return {"running": False}


def handle_network(action: str) -> HandlerResult:
    """Визуализация сетевой топологии – список лабораторий."""
    try:
        from practice import DOCKER_LABS
    except ImportError:
        console.print("[red]Модуль practice не найден[/red]")
        return True, None, None, True

    ctx = get_context()
    state = ctx.state
    tree = Tree("[bold]Host (CyberTeacher)[/bold]")

    # Count running for summary
    running = 0
    for key, lab in DOCKER_LABS.items():
        container_name = f"{key}-web"
        status = get_container_status(container_name)
        if status.get("running", False):
            running += 1
            label = f"[green]{key}[/green] - {lab.get('name', '')} (ports: {', '.join(lab.get('ports', []))})"
        else:
            label = f"[red]{key}[/red] - {lab.get('name', '')} (stopped)"
        tree.add(label)

    console.print(tree)
    console.print(f"[cyan]Активных лабораторий: {running}/{len(DOCKER_LABS)}[/cyan]")
    return True, None, None, True