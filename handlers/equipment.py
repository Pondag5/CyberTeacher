"""Equipment (tool selection) handling"""

from rich.console import Console
from rich.table import Table

from di import get_context
from tools_ram import MAX_RAM, TOOL_RAM_COSTS

console = Console()


def handle_tools(action: str):
    """Показать доступные инструменты и текущую экипировку."""
    ctx = get_context()
    state = ctx.state
    selected = set(state.selected_tools)

    table = Table(title="Инструменты (RAM)")
    table.add_column("Инструмент", style="cyan")
    table.add_column("RAM", justify="right", style="magenta")
    table.add_column("Статус", style="yellow")

    for tool, cost in sorted(TOOL_RAM_COSTS.items()):
        status = "[green]Выбран[/green]" if tool in selected else "[dim]Не выбран[/dim]"
        table.add_row(tool, str(cost), status)

    console.print(table)
    used = sum(TOOL_RAM_COSTS.get(t, 0) for t in selected)
    console.print(f"Использовано RAM: {used}/{MAX_RAM}")
    return True, None, None, True


def handle_equip(action: str):
    """Экипировать/снять инструмент: /equip <tool>."""
    ctx = get_context()
    state = ctx.state
    parts = action.split()
    if len(parts) < 2:
        console.print("[red]Укажите инструмент: /equip <tool>[/red]")
        return True, None, None, True

    tool = parts[1].lower()
    if tool not in TOOL_RAM_COSTS:
        console.print(f"[red]Инструмент '{tool}' неизвестен.[/red]")
        console.print(
            "[dim]Доступные: " + ", ".join(sorted(TOOL_RAM_COSTS.keys())) + "[/dim]"
        )
        return True, None, None, True

    # Toggle selection
    if tool in state.selected_tools:
        state.selected_tools.remove(tool)
        console.print(f"[yellow]{tool} удалён из экипировки.[/yellow]")
    else:
        # Check capacity
        new_total = (
            sum(TOOL_RAM_COSTS.get(t, 0) for t in state.selected_tools)
            + TOOL_RAM_COSTS[tool]
        )
        if new_total > MAX_RAM:
            console.print(
                f"[red]Недостаточно RAM! Добавление {tool} превысит лимит ({new_total}/{MAX_RAM}).[/red]"
            )
            return True, None, None, True
        state.selected_tools.append(tool)
        console.print(f"[green]{tool} экипирован.[/green]")

    # Persist
    ctx.save_state()
    return True, None, None, True
