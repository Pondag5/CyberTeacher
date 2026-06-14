# handlers/cve.py
import json
import os
import time
from typing import Any, Dict, Optional, Tuple

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from handlers.types import HandlerResult


console = Console()

CVE_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
CACHE_TTL = 3600 * 24  # 24 часа


def _fetch_cve(cve_id: str) -> Optional[Dict[str, Any]]:
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        vulnerabilities = data.get("vulnerabilities", [])
        if not vulnerabilities:
            return None
        cve_data = vulnerabilities[0].get("cve", {})
        return {
            "id": cve_data.get("id"),
            "description": cve_data.get("descriptions", [{}])[0].get("value", ""),
            "published": cve_data.get("published"),
            "severity": cve_data.get("metrics", {})
            .get("cvssMetricV31", [{}])[0]
            .get("cvssData", {})
            .get("baseSeverity", "UNKNOWN"),
            "score": cve_data.get("metrics", {})
            .get("cvssMetricV31", [{}])[0]
            .get("cvssData", {})
            .get("baseScore", 0),
            "references": [
                {"url": ref.get("url")} for ref in cve_data.get("references", [])
            ],
        }
    except (ValueError, KeyError, IndexError, TypeError):
        return None


def handle_cve(action: str) -> HandlerResult:
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[cyan]Использование: /cve CVE-YYYY-XXXX[/cyan]")
        return True, None, None, True

    cve_id = parts[1].strip().upper()
    cached = CVE_CACHE.get(cve_id)
    cve_data: Optional[Dict[str, Any]] = None
    if cached and (time.time() - cached[0] < CACHE_TTL):
        cve_data = cached[1]
    else:
        cve_data = _fetch_cve(cve_id)
        if cve_data is None:
            console.print(f"[red]❌ CVE {cve_id} не найден[/red]")
            return True, None, None, True
        CVE_CACHE[cve_id] = (time.time(), cve_data)

    out = f"""[bold]🔍 {cve_data["id"]}[/bold]
[yellow]Severity: {cve_data["severity"]} (Score: {cve_data["score"]})[/yellow]
[dim]Published: {cve_data["published"]}[/dim]

[bold]📝 Description:[/bold]
{cve_data["description"][:500]}...

[bold]🔗 References:[/bold]
"""
    for ref in cve_data.get("references", [])[:5]:
        out += f"  • {ref['url']}\n"

    console.print(Panel(out, title=f"CVE Details", border_style="red"))
    return True, None, None, True


def handle_walkthrough(action: str) -> HandlerResult:
    """Handle /walkthrough command."""
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[cyan]Использование: /walkthrough <topic>[/cyan]")
        console.print("[dim]Пример: /walkthrough SQL Injection[/dim]")
        return True, None, None, True

    topic = parts[1].strip()
    console.print(
        Panel(
            f"[bold]📚 Walkthrough: {topic}[/bold]\n\n"
            "Для получения walkthrough по машине HackTheBox используйте:\n"
            "  /htb walkthrough <machine_id>",
            title="Walkthrough",
            border_style="cyan",
        )
    )
    return True, None, None, True


def handle_exploit_search(action: str) -> HandlerResult:
    """Handle /exploit command — search exploits or CVE details."""
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[cyan]Использование: /exploit <query>[/cyan]")
        console.print("[dim]Примеры:[/dim]")
        console.print("  /exploit CVE-2024-1234  — поиск информации о CVE")
        console.print("  /exploit buffer overflow — поиск эксплойтов")
        return True, None, None, True

    query = parts[1].strip()
    query_upper = query.upper()

    if query_upper.startswith("CVE-"):
        cve_data = _fetch_cve(query_upper)
        if cve_data is None:
            console.print(f"[red]❌ CVE {query_upper} не найден[/red]")
            return True, None, None, True

        out = f"""[bold]🔍 Exploit search for {cve_data["id"]}[/bold]
[yellow]Severity: {cve_data["severity"]} (Score: {cve_data["score"]})[/yellow]
[dim]Published: {cve_data["published"]}[/dim]

[bold]📝 Description:[/bold]
{cve_data["description"][:500]}...

[bold]🔗 References:[/bold]
"""
        for ref in cve_data.get("references", [])[:5]:
            out += f"  • {ref['url']}\n"

        console.print(Panel(out, title="Exploit / CVE Info", border_style="red"))
    else:
        console.print(
            Panel(
                f"[bold]🔍 Поиск эксплойтов: {query}[/bold]\n\n"
                "Для поиска CVE используйте /exploit CVE-YYYY-XXXX\n"
                "Для HTB walkthrough: /htb walkthrough <machine_id>",
                title="Exploit Search",
                border_style="yellow",
            )
        )

    return True, None, None, True
