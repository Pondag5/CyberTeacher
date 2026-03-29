"""Network topology visualization (ASCII)"""

from rich.console import Console
from rich.tree import Tree

from state import get_state

console = Console()


def handle_network(action: str):
    """Обработка команды /network — отображение сети лабораторий."""
    from practice import DOCKER_LABS, get_container_status

    state = get_state()
    tree = Tree("[bold]Host (CyberTeacher)[/bold]")

    # Count running for summary
    running = 0
    for key, lab in DOCKER_LABS.items():
        container_name = f"{key}-web"
        status = get_container_status(container_name)
        if status["running"]:
            running += 1
            label = f"[green]{key}[/green] - {lab['name']} (ports: {', '.join(lab['ports'])})"
        else:
            label = f"[red]{key}[/red] - {lab['name']} (stopped)"
        tree.add(label)

    console.print(tree)
    console.print(f"[cyan]Итого запущено: {running}/{len(DOCKER_LABS)}[/cyan]")
    return True, None, None, True
