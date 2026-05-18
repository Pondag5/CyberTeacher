"""Health check command for /health."""

import time
from typing import Any

from rich.console import Console
from rich.table import Table

from di import get_context

console = Console()


def handle_health(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Handle /health command."""
    ctx = get_context()
    state = ctx.state
    uptime_seconds = time.time() - state.start_time
    hours, rem = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    total_cache = state.cache_hits + state.cache_misses
    cache_hit_rate = (state.cache_hits / total_cache * 100) if total_cache else 0.0

    table = Table(title="Health Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Uptime", uptime_str)
    table.add_row("LLM Requests", str(state.llm_call_count))
    table.add_row(
        "LLM Avg Time (s)",
        f"{(state.llm_total_time / state.llm_call_count if state.llm_call_count else 0):.3f}",
    )
    table.add_row("LLM Total Tokens", str(state.llm_total_tokens))
    table.add_row("Cache Hits", str(state.cache_hits))
    table.add_row("Cache Misses", str(state.cache_misses))
    table.add_row("Cache Hit Rate", f"{cache_hit_rate:.1f}%")
    table.add_row("Current Mode", state.current_mode)

    console.print(table)
    return True, None, None, True
