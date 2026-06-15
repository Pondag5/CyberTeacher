# handlers/docker_gen.py — Генерация docker-compose для заданий (L-06)
"""Автоматическое создание docker-compose.yml для практических заданий."""

import os
from typing import Any, Dict, TypedDict

import yaml
from rich.console import Console
from rich.panel import Panel
from handlers.types import HandlerResult


console = Console()


# Определяем TypedDict для описания образа лаборатории
class LabImageTypedDict(TypedDict, total=False):
    image: str
    ports: Dict[str, str]
    description: str
    category: str


LAB_IMAGES: Dict[str, LabImageTypedDict] = {
    "dvwa": {
        "image": "vulnerables/web-dvwa:latest",
        "ports": {"8080": "80"},
        "description": "Damn Vulnerable Web Application",
        "category": "web",
    },
    "juice_shop": {
        "image": "bkimminich/juice-shop:latest",
        "ports": {"3000": "3000"},
        "description": "OWASP Juice Shop",
        "category": "web",
    },
    "webgoat": {
        "image": "webgoat/webgoat:latest",
        "ports": {"8080": "8080", "9090": "9090"},
        "description": "OWASP WebGoat",
        "category": "web",
    },
    "metasploitable": {
        "image": "tleemcjr/metasploitable2:latest",
        "ports": {"2121": "21", "2222": "22", "8081": "80"},
        "description": "Metasploitable 2",
        "category": "network",
    },
    "sqlilabs": {
        "image": "acgpiano/sqli-labs:latest",
        "ports": {"8082": "80"},
        "description": "SQLi Labs",
        "category": "sqli",
    },
    "vulnerable_api": {
        "image": "hmajid2301/vulnerable-rest-api:latest",
        "ports": {"5000": "5000"},
        "description": "Vulnerable REST API",
        "category": "api",
    },
    "cve_searchsploit": {
        "image": "offensivesecurity/exploitdb:latest",
        "description": "Exploit Database",
        "category": "tools",
        "ports": {},
    },
    "nginx_vuln": {
        "image": "nginx:1.14.0",
        "ports": {"8083": "80"},
        "description": "Nginx с известными уязвимостями",
        "category": "network",
    },
}


def handle_docker_gen(action: str) -> HandlerResult:
    """Генерация docker-compose для заданий."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        console.print(
            Panel(
                "[bold cyan]🐳 Генератор Docker Compose[/bold cyan]\n\n"
                "Использование:\n"
                "  /dockergen list              — доступные образы\n"
                "  /dockergen create <лабы...>  — создать docker-compose\n"
                "  /dockergen sqli              — лаба для SQLi\n"
                "  /dockergen web               — веб-лаборатории\n"
                "  /dockergen network           — сетевые лаборатории\n"
                "  /dockergen custom <имя>  \\[ports] — кастомный",
                title="DOCKER GEN",
                border_style="cyan",
            )
        )
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "list":
        return _list_images()

    if subcommand == "create" and len(parts) >= 3:
        labs = parts[2].split()
        return _create_compose(labs)

    if subcommand in ("sqli", "web", "network", "api", "all"):
        preset_map = {
            "sqli": ["dvwa", "sqlilabs"],
            "web": ["dvwa", "juice_shop", "webgoat"],
            "network": ["metasploitable", "nginx_vuln"],
            "api": ["vulnerable_api", "juice_shop"],
            "all": list(LAB_IMAGES.keys()),
        }
        return _create_compose(preset_map[subcommand])

    if subcommand == "custom" and len(parts) >= 4:
        subparts = parts[2].split(maxsplit=2)
        name = subparts[0]
        image = subparts[1]
        ports_str = subparts[2] if len(subparts) > 2 else None
        return _create_custom(name, image, ports_str)

    console.print("[yellow]Неизвестная подкоманда. /dockergen для справки.[/yellow]")
    return True, None, None, True


def _list_images() -> HandlerResult:
    """Показать доступные образы."""
    console.print("[bold cyan]📦 Доступные Docker образы[/bold cyan]\n")
    for lid, lab in LAB_IMAGES.items():
        console.print(f"  [cyan]{lid:<18}[/cyan] — {lab.get('description', '')}")
        console.print(f"  [dim]{' ' * 20}Image: {lab.get('image', '')}[/dim]")
        ports = lab.get("ports")
        if ports:
            ports_str = ", ".join(f"{host}:{cont}" for host, cont in ports.items())
            console.print(f"  [dim]{' ' * 20}Ports: {ports_str}[/dim]")
        console.print()
    return True, None, None, True


def _create_compose(labs: list[str]) -> HandlerResult:
    """Создать docker-compose.yml для списка лаб."""
    services: Dict[str, Any] = {}

    for lab_name in labs:
        lab = LAB_IMAGES.get(lab_name)
        if not lab:
            console.print(f"[yellow]⚠️ Лаба '{lab_name}' не найдена, пропускаю[/yellow]")
            continue

        service: Dict[str, Any] = {
            "image": lab["image"],
            "container_name": f"ct_{lab_name}",
            "restart": "unless-stopped",
            "networks": ["ct_lab_net"],
        }

        ports = lab.get("ports")
        if ports:
            service["ports"] = [f"{host}:{cont}" for host, cont in ports.items()]

        services[lab_name] = service

    if not services:
        console.print("[red]❌ Нет валидных лаб для создания[/red]")
        return True, None, None, True

    compose: Dict[str, Any] = {
        "version": "3.8",
        "services": services,
        "networks": {"ct_lab_net": {"driver": "bridge"}},
    }

    output_dir = "./lab_configs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"lab_{'_'.join(labs[:3])}.yml"
    if len(labs) > 3:
        filename = f"lab_custom_{len(labs)}_services.yml"

    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(compose, f, default_flow_style=False, allow_unicode=True)

    console.print(
        Panel(
            f"[green]✅ Docker Compose создан![/green]\n\n"
            f"Файл: {filepath}\n"
            f"Сервисов: {len(services)}\n\n"
            f"[bold]Запуск:[/bold]\n"
            f"  docker-compose -f {filepath} up -d\n\n"
            f"[bold]Остановка:[/bold]\n"
            f"  docker-compose -f {filepath} down",
            title="🐳 DOCKER COMPOSE",
            border_style="green",
        )
    )
    return True, None, None, True


def _create_custom(
    name: str, image: str, ports_str: str | None
) -> HandlerResult:
    """Создать кастомный docker-compose."""
    service: Dict[str, Any] = {
        "image": image,
        "container_name": f"ct_{name}",
        "restart": "unless-stopped",
        "ports": [],
    }

    if ports_str:
        service["ports"] = [p.strip() for p in ports_str.split(",")]

    compose: Dict[str, Any] = {
        "version": "3.8",
        "services": {name: service},
    }

    output_dir = "./lab_configs"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"custom_{name}.yml")

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(compose, f, default_flow_style=False, allow_unicode=True)

    console.print(f"[green]✅ Кастомный docker-compose создан: {filepath}[/green]")
    return True, None, None, True