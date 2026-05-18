"""CVE lookup handler"""

import time
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()

# Simple in-memory cache: {cve_id: (timestamp, data)}
_cve_cache: dict[str, tuple[float, dict[str, Any]]] = {}
CACHE_TTL = 3600  # 1 hour


def _fetch_cve(cve_id: str) -> dict[str, Any] | None:
    """Fetch CVE from NVD API."""
    import requests

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        # Extract the first CVE
        vulns = data.get("vulnerabilities", [])
        if not vulns:
            return None
        return vulns[0]["cve"]
    except Exception:
        return None


def handle_cve(action: str):
    """Обработка команды /cve <id>."""
    parts = action.split()
    if len(parts) < 2:
        console.print("[cyan]Использование: /cve <CVE-ID>[/cyan]")
        return True, None, None, True

    cve_id = parts[1].upper()

    # Check cache
    cached = _cve_cache.get(cve_id)
    if cached and (time.time() - cached[0] < CACHE_TTL):
        data = cached[1]
    else:
        data = _fetch_cve(cve_id)
        if data is None:
            console.print(f"[red]CVE {cve_id} не найден[/red]")
            return True, None, None, True
        _cve_cache[cve_id] = (time.time(), data)

    # Build output
    desc = data.get("descriptions", [{}])[0].get("value", "Нет описания")
    severity = "N/A"
    metrics = data.get("metrics", {}).get("cvssMetricV31", [{}])[0]
    if metrics:
        severity = metrics.get("cvssData", {}).get("baseScore", "N/A")
    refs = [ref.get("url") for ref in data.get("references", []) if ref.get("url")]
    ref_lines = "\n".join(f"  • {url}" for url in refs[:5])

    out = f"""[bold]CVE: {cve_id}[/bold]
[magenta]Уровень CVSS: {severity}[/magenta]
[white]Описание: {desc}[/white]
[cyan]Ссылки:[/cyan]
{ref_lines}
"""
    console.print(Panel(out, title="CVE lookup", border_style="cyan"))
    return True, None, None, True
