"""Exploit walkthrough handler - step-by-step guidance"""

import logging
from typing import Any

from rich.console import Console
from rich.panel import Panel

from config import get_llm
from handlers.cve import CACHE_TTL, _cve_cache, _fetch_cve

console = Console()
logger = logging.getLogger(__name__)

# Simple cache for walkthroughs
_walkthrough_cache: dict[str, tuple[float, str]] = {}
WALKTHROUGH_CACHE_TTL = 3600  # 1 hour


def handle_walkthrough(action: str) -> tuple[bool, None, None, bool]:
    """Handle /walkthrough <topic> - generate step-by-step exploit guide."""
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[cyan]Использование: /walkthrough <тема>[/cyan]")
        console.print("[dim]Примеры:[/dim]")
        console.print("  /walkthrough SQL Injection")
        console.print("  /walkthrough buffer overflow")
        console.print("  /walkthrough XSS reflected")
        return True, None, None, True

    topic = parts[1].strip()

    # Check cache
    cached = _walkthrough_cache.get(topic.lower())
    if cached and (__import__("time").time() - cached[0] < WALKTHROUGH_CACHE_TTL):
        walkthrough = cached[1]
        console.print(
            Panel(walkthrough, title=f"Walkthrough: {topic}", border_style="green")
        )
        return True, None, None, True

    try:
        llm = get_llm()
        prompt = f"""
Ты - опытный пентестер и преподаватель кибербезопасности.
Создай подробные пошаговые инструкции по exploitation для темы: "{topic}"

Требования к структуре:

1. **Введение**: Кратко объясни, что это за уязвимость и где встречается.

2. **Предварительные условия**: Что нужно для exploitation (доступ, инструменты, условия).

3. **Пошаговое руководство**:
   - Шаг 1: [Название]
     * Цель: ...
     * Команды/действия:
       ```bash
       # пример
       $ nmap -sV target.com
       ```
     * Что должно произойти / ожидаемый результат
     * Альтернативные варианты если что-то пошло не так

   - Шаг 2: ...
   (и так далее, минимум 5 шагов)

4. **Проверка успеха**: Как понять, что эксплуатация удалась?

5. **Пост-эксплуатация** (если применимо): Что делать после получения доступа?

6. **Защита**: Как предотвратить эту уязвимость?

7. **Тестирование в legal environment**: Где практиковаться (HTB, DVWA, TryHackMe, etc.)

Форматирование:
- Используй markdown
- Выделяй команды в блоки кода
- Используй эмодзи для визуального различения типов шагов (🔍 👣 💥 🛡️)
- Будь конкретным, но安全 (без запрещённых деталей)
"""

        resp = llm.invoke(prompt)
        walkthrough = resp.content if hasattr(resp, "content") else str(resp)

        # Cache it
        _walkthrough_cache[topic.lower()] = (__import__("time").time(), walkthrough)

        console.print(
            Panel(walkthrough, title=f"📘 Walkthrough: {topic}", border_style="cyan")
        )
        return True, None, None, True

    except Exception as e:
        console.print(f"[red]❌ Ошибка генерации walkthrough: {e!s}[/red]")
        return True, None, None, True


def handle_exploit_search(action: str) -> tuple[bool, None, None, bool]:
    """Handle /exploit <cve> or /exploit <tech> - search for exploits."""
    parts = action.split()
    if len(parts) < 2:
        console.print("[cyan]Использование: /exploit <CVE-ID>[/cyan]")
        console.print("[dim]Пример: /exploit CVE-2021-44228[/dim]")
        return True, None, None, True

    query = parts[1].upper()

    # If it looks like a CVE
    if query.startswith("CVE-"):
        # Check CVE cache first (from handlers.cve)
        import time

        cached = _cve_cache.get(query)
        if cached and (time.time() - cached[0] < CACHE_TTL):
            cve_data = cached[1]
        else:
            cve_data = _fetch_cve(query)
            if cve_data is None:
                console.print(f"[red]CVE {query} не найден[/red]")
                return True, None, None, True
            _cve_cache[query] = (time.time(), cve_data)

        # Extract references (exploit links)
        refs = cve_data.get("references", [])
        exploit_refs = [
            r.get("url")
            for r in refs
            if "exploit" in r.get("url", "").lower()
            or "exploit-db" in r.get("url", "").lower()
        ]

        out = f"[bold]🔎 Результаты для {query}[/bold]\n\n"
        if exploit_refs:
            out += "[cyan]Найдены ссылки на эксплойты:[/cyan]\n"
            for url in exploit_refs[:5]:
                out += f"  • {url}\n"
        else:
            out += "[yellow]Прямых ссылок на эксплойты не найдено[/yellow]\n"
            out += "[dim]Попробуй поискать на:[/dim]\n"
            out += "  • https://www.exploit-db.com\n"
            out += "  • https://nvd.nist.gov\n"
            out += "  • https://github.com/search?q=" + query + "\n"

        console.print(Panel(out, title="Exploit Search", border_style="magenta"))
        return True, None, None, True
    else:
        console.print(f"[yellow]🔎 Поиск эксплойтов для: {query}[/yellow]")
        console.print("[dim]Для CVE используй формат: CVE-YYYY-NNNN[/dim]")
        console.print("[dim]Или попробуй /walkthrough для пошагового разбора[/dim]")
        return True, None, None, True
