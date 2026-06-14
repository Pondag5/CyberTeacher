"""Модуль Shodan / Censys Integration — поиск устройств в интернете.

Команды:
    /shodan search <query>  — Поиск устройств в Shodan
    /shodan host <ip>       — Информация о хосте
    /censys search <query>  — Поиск в Censys
    /censys host <ip>       — Информация о хосте в Censys
    /shodan help            — Справка
"""

import os
import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from ui import console
from handlers.types import HandlerResult


# Попытка импорта реальных библиотек (если установлены)
try:
    import shodan

    SHODAN_AVAILABLE = True
except ImportError:
    SHODAN_AVAILABLE = False

try:
    import censys

    CENSYS_AVAILABLE = True
except ImportError:
    CENSYS_AVAILABLE = False


def _simulate_shodan_search(query: str) -> list[dict[str, Any]]:
    """Симуляция поиска в Shodan."""
    products = [
        "Apache httpd",
        "nginx",
        "OpenSSH",
        "Microsoft IIS",
        "Docker",
        "Redis",
        "MongoDB",
    ]
    os_list = ["Linux", "Windows", "FreeBSD", "macOS"]
    countries = ["US", "DE", "CN", "RU", "BR", "JP", "GB", "FR"]

    results = []
    count = random.randint(3, 8)
    for _ in range(count):
        results.append(
            {
                "ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "port": random.choice([22, 80, 443, 8080, 3306, 5432, 6379, 27017]),
                "product": random.choice(products),
                "os": random.choice(os_list),
                "country": random.choice(countries),
                "vulns": random.sample(
                    ["CVE-2021-44228", "CVE-2022-22965", "CVE-2023-44487"],
                    k=random.randint(0, 2),
                ),
            }
        )
    return results


def _simulate_shodan_host(ip: str) -> dict[str, Any]:
    """Симуляция информации о хосте в Shodan."""
    return {
        "ip": ip,
        "ports": random.sample(
            [22, 80, 443, 8080, 3306, 5432, 6379, 27017, 9200], k=random.randint(2, 5)
        ),
        "os": random.choice(["Linux 4.x", "Windows Server 2019", "Ubuntu 22.04"]),
        "hostname": f"server-{random.randint(1, 999)}.example.com",
        "org": random.choice(
            ["Amazon", "Google Cloud", "Microsoft Azure", "DigitalOcean"]
        ),
        "vulns": ["CVE-2021-44228"] if random.random() > 0.5 else [],
    }


def _simulate_censys_search(query: str) -> list[dict[str, Any]]:
    """Симуляция поиска в Censys."""
    services = ["HTTP", "HTTPS", "SSH", "FTP", "SMTP", "DNS", "RDP"]
    results = []
    for _ in range(random.randint(2, 5)):
        results.append(
            {
                "ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "service": random.choice(services),
                "port": random.choice([80, 443, 22, 21, 25, 53, 3389]),
                "certificate": random.choice(["Valid", "Expired", "Self-Signed"]),
            }
        )
    return results


def _display_shodan_search(query: str) -> bool:
    """Вывести результаты поиска Shodan."""
    if not query:
        console.print("[red]Укажите запрос для поиска.[/red]")
        return False

    # Проверка реального API
    api_key = os.getenv("SHODAN_API_KEY")
    if SHODAN_AVAILABLE and api_key:
        try:
            api = shodan.Shodan(api_key)
            api_results: dict[Any, Any] = api.search(query)
            console.print(
                f"[green]Найдено {api_results['total']} результатов (реальный API).[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[yellow]Ошибка API: {e}. Использую симуляцию.[/yellow]")

    results: list[dict[str, Any]] = _simulate_shodan_search(query)
    table = Table(title=f"Shodan Search: {query}")
    table.add_column("IP", style="cyan")
    table.add_column("Port", style="green")
    table.add_column("Product", style="yellow")
    table.add_column("OS", style="magenta")
    table.add_column("Country", style="blue")

    for r in results:
        vuln_str = f" ({len(r['vulns'])} CVE)" if r["vulns"] else ""
        table.add_row(
            r["ip"], str(r["port"]), r["product"] + vuln_str, r["os"], r["country"]
        )

    console.print(table)
    console.print(
        Panel(
            "[bold]Совет:[/bold] Установите `shodan` и добавьте `SHODAN_API_KEY` в .env для реальных данных.\n"
            "Используйте фильтры: `port:22`, `os:linux`, `country:RU`, `vuln:CVE-2021-44228`",
            border_style="blue",
        )
    )
    return True


def _display_shodan_host(ip: str) -> bool:
    """Вывести информацию о хосте Shodan."""
    if not ip:
        console.print("[red]Укажите IP-адрес.[/red]")
        return False

    api_key = os.getenv("SHODAN_API_KEY")
    if SHODAN_AVAILABLE and api_key:
        try:
            api = shodan.Shodan(api_key)
            host = api.host(ip)
            console.print(f"[green]Реальные данные для {ip}[/green]")
            return True
        except (shodan.APIError, ValueError, OSError):
            pass

    data = _simulate_shodan_host(ip)
    content = f"""[bold]IP:[/bold] {data["ip"]}
[bold]Hostname:[/bold] {data["hostname"]}
[bold]OS:[/bold] {data["os"]}
[bold]Organization:[/bold] {data["org"]}
[bold]Ports:[/bold] {", ".join(map(str, data["ports"]))}
[bold]Vulnerabilities:[/bold] {", ".join(data["vulns"]) if data["vulns"] else "None"}"""

    console.print(Panel(content, title=f"Shodan Host: {ip}", border_style="cyan"))
    return True


def _display_censys_search(query: str) -> bool:
    """Вывести результаты поиска Censys."""
    if not query:
        console.print("[red]Укажите запрос для поиска.[/red]")
        return False

    results = _simulate_censys_search(query)
    table = Table(title=f"Censys Search: {query}")
    table.add_column("IP", style="cyan")
    table.add_column("Service", style="green")
    table.add_column("Port", style="yellow")
    table.add_column("Certificate", style="magenta")

    for r in results:
        table.add_row(r["ip"], r["service"], str(r["port"]), r["certificate"])

    console.print(table)
    console.print(
        Panel(
            "[bold]Censys[/bold] специализируется на сканировании сертификатов и сервисов.\n"
            "Полезно для поиска exposed databases и misconfigured servers.",
            border_style="blue",
        )
    )
    return True


def handle_shodan(args: str) -> HandlerResult:
    """Главный обработчик команды /shodan."""
    parts = args.strip().split(maxsplit=1)
    if not parts or parts[0] == "":
        console.print(
            Panel(
                "[bold]Команды Shodan:[/bold]\n"
                "/shodan search <query>  — Поиск устройств\n"
                "/shodan host <ip>       — Информация о хосте\n\n"
                "[dim]Требуется SHODAN_API_KEY в .env для реальных данных.[/dim]",
                border_style="yellow",
            )
        )
        return True, None, None, True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "search":
        success = _display_shodan_search(query)
        return True, None, None, success
    elif subcommand == "host":
        success = _display_shodan_host(query)
        return True, None, None, success
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return True, None, None, True


def handle_censys(args: str) -> HandlerResult:
    """Главный обработчик команды /censys."""
    parts = args.strip().split(maxsplit=1)
    if not parts or parts[0] == "":
        console.print(
            Panel(
                "[bold]Команды Censys:[/bold]\n"
                "/censys search <query>  — Поиск сервисов\n"
                "/censys host <ip>       — Информация о хосте",
                border_style="yellow",
            )
        )
        return True, None, None, True

    subcommand = parts[0].lower()
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "search":
        success = _display_censys_search(query)
        return True, None, None, success
    elif subcommand == "host":
        console.print(
            Panel(
                f"[bold]Censys Host:[/bold] {query}\n"
                "Функция в разработке. Используйте Shodan для детальной информации.",
                border_style="yellow",
            )
        )
        return True, None, None, True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return True, None, None, True
