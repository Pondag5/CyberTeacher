"""Practice module with Docker labs and practice tasks."""

import os
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple

from rich.table import Table

from state import get_state
from ui import console

# Docker labs configuration
DOCKER_LABS: Dict[str, Dict[str, Any]] = {
    "dvwa": {
        "name": "DVWA",
        "desc": "Damn Vulnerable Web Application (требуется init MySQL)",
        "image": "vulnerables/web-dvwa:latest",
        "ports": {"8080": "80"},
        "tags": ["web", "beginner", "sqli", "xss"],
        "category": "web",
        "post_start": "sleep 3 && /etc/init.d/mysql start 2>/dev/null; /etc/init.d/apache2 restart 2>/dev/null",
    },
    "juice": {
        "name": "OWASP Juice Shop",
        "desc": "Modern vulnerable web app",
        "image": "bkimminich/juice-shop:latest",
        "ports": {"3000": "3000"},
        "tags": ["web", "api", "jwt"],
        "category": "web",
    },
    "webgoat": {
        "name": "OWASP WebGoat",
        "desc": "WebGoat training environment",
        "image": "webgoat/webgoat:latest",
        "ports": {"8080": "8080", "9090": "9090"},
        "tags": ["web", "training"],
        "category": "web",
    },
    "metasploitable2": {
        "name": "Metasploitable 2",
        "desc": "Intentionally vulnerable Linux VM (Docker)",
        "image": "tleemcjr/metasploitable2:latest",
        "ports": {"2121": "21", "2222": "22", "8081": "80"},
        "tags": ["network", "linux", "privesc"],
        "category": "network",
    },
    "metasploitable3": {
        "name": "Metasploitable 3",
        "desc": "Windows + Linux vulnerable environment",
        "image": "metasploitable3-ubuntu1404",
        "ports": {"8585": "8585"},
        "tags": ["windows", "network", "advanced"],
        "category": "network",
    },
    "sqlilabs": {
        "name": "SQLi Labs",
        "desc": "SQL injection training",
        "image": "acgpiano/sqli-labs:latest",
        "ports": {"8082": "80"},
        "tags": ["web", "sqli"],
        "category": "web",
    },
    "vulnapi": {
        "name": "Vulnerable REST API",
        "desc": "REST API with common vulnerabilities",
        "image": "hmajid2301/vulnerable-rest-api:latest",
        "ports": {"5000": "5000"},
        "tags": ["api", "rest"],
        "category": "api",
    },
    "crapi": {
        "name": "CRAPI",
        "desc": "Completely Ridiculous API",
        "image": "crapi/crapi:latest",
        "ports": {"8888": "8888"},
        "tags": ["api", "graphql"],
        "category": "api",
    },
    "dvna": {
        "name": "DVNA",
        "desc": "Damn Vulnerable Node.js Application",
        "image": "appsecco/dvna:latest",
        "ports": {"9090": "9090"},
        "tags": ["nodejs", "web"],
        "category": "web",
    },
    "picklerick": {
        "name": "Pickle Rick",
        "desc": "Rick and Morty themed CTF",
        "image": "jesusgoku/picklerick:latest",
        "ports": {"8000": "8000"},
        "tags": ["ctf", "web"],
        "category": "ctf",
    },
}

# Categories for grouping labs
categories: Dict[str, Dict[str, Any]] = {
    "web": {"name": "Веб-безопасность", "icon": "🌐"},
    "network": {"name": "Сеть", "icon": "🔌"},
    "api": {"name": "API", "icon": "🔗"},
    "ctf": {"name": "CTF", "icon": "🏆"},
}


def get_all_running_labs() -> Dict[str, Dict[str, Any]]:
    """Get all currently running labs from state."""
    state = get_state()
    running = getattr(state, "running_labs", [])
    result = {}
    for lab_id in running:
        lab = DOCKER_LABS.get(lab_id)
        if lab:
            result[lab_id] = {
                "name": lab.get("name", lab_id),
                "status": "running",
                "ports": lab.get("ports", {}),
            }
    return result


def get_container_logs(container_name: str, lines: int = 10) -> str:
    """Fetch logs from a container."""
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(lines), container_name],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "Логов нет"
    except (subprocess.TimeoutExpired, OSError):
        return "Ошибка получения логов"


def handle_practice(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Handler for /practice and /lab commands."""
    parts = action.split()
    if not parts:
        console.print(
            "[cyan]Использование: /lab list | start <id> | stop <id> | status[/cyan]"
        )
        return True, None, None, True

    cmd = parts[0].lower()
    if cmd == "list" or cmd == "labs":
        return _list_labs()
    elif cmd == "start" and len(parts) >= 2:
        lab_id = parts[1]
        return _start_lab(lab_id)
    elif cmd == "stop" and len(parts) >= 2:
        lab_id = parts[1]
        return _stop_lab(lab_id)
    elif cmd == "status":
        return _lab_status()
    else:
        console.print(
            "[yellow]Неизвестная команда. /lab list - список лабораторий[/yellow]"
        )
        return True, None, None, True


def _list_labs() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Display list of available labs."""
    table = Table(title="[DOCKER] Docker лаборатории")
    table.add_column("ID", style="cyan")
    table.add_column("Название", style="green")
    table.add_column("Описание", style="yellow")
    table.add_column("Порты", style="magenta")
    table.add_column("Теги", style="blue")

    for lid, lab in DOCKER_LABS.items():
        ports = lab.get("ports", {})
        ports_str = ", ".join(f"{host}:{cont}" for host, cont in ports.items())
        tags = lab.get("tags", [])
        tags_str = ", ".join(tags[:3])
        table.add_row(
            lid,
            lab.get("name", lid),
            lab.get("desc", "")[:40],
            ports_str,
            tags_str,
        )

    console.print(table)
    console.print("\n[dim]/lab start <id> - запустить лабораторию[/dim]")
    console.print("[dim]/lab stop <id> - остановить[/dim]")
    return True, None, None, True


def _start_lab(lab_id: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Start a Docker lab."""
    lab = DOCKER_LABS.get(lab_id)
    if not lab:
        console.print(f"[red]Лаборатория '{lab_id}' не найдена[/red]")
        return True, None, None, True

    image = lab.get("image", "")
    if not image:
        console.print("[red]Образ Docker не указан[/red]")
        return True, None, None, True

    container_name = f"cyberteacher-{lab_id}"
    ports = lab.get("ports", {})
    port_args = []
    port_list = []
    for host_port, container_port in ports.items():
        port_args.extend(["-p", f"{host_port}:{container_port}"])
        port_list.append(f"http://localhost:{host_port}")

    cmd = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name,
        *port_args,
        image,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, check=False
        )
        if result.returncode != 0:
            if "already in use" in result.stderr:
                start_cmd = ["docker", "start", container_name]
                start_result = subprocess.run(
                    start_cmd, capture_output=True, text=True, timeout=30, check=False
                )
                if start_result.returncode == 0:
                    state = get_state()
                    running = getattr(state, "running_labs", [])
                    if lab_id not in running:
                        running.append(lab_id)
                        state.running_labs = running
                    console.print(
                        f"[green]✅ Лаборатория {lab.get('name', lab_id)} перезапущена[/green]"
                    )
                    console.print(f"[dim]Порты: {', '.join(port_list)}[/dim]")
                    return True, None, None, True
            console.print(f"[red]Ошибка: {result.stderr}[/red]")
            return True, None, None, True

        container_id = result.stdout.strip()[:12]
        state = get_state()
        running = getattr(state, "running_labs", [])
        if lab_id not in running:
            running.append(lab_id)
            state.running_labs = running
            from handlers.debt import add_debt

            add_debt(f"Лаба: {lab_id}")

        # Post-start hooks (e.g., MySQL init for DVWA)
        post_start = lab.get("post_start", "")
        if post_start:
            try:
                subprocess.run(
                    ["docker", "exec", container_name, "/bin/bash", "-c", post_start],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
            except (subprocess.TimeoutExpired, OSError):
                pass

        console.print(
            f"[green]✅ Лаборатория {lab.get('name', lab_id)} запущена![/green]"
        )
        console.print(f"[dim]Container ID: {container_id}[/dim]")
        if port_list:
            console.print(f"[dim]Порты: {', '.join(port_list)}[/dim]")
        return True, None, None, True
    except (subprocess.TimeoutExpired, OSError, ValueError) as e:
        console.print(f"[red]Ошибка запуска: {e}[/red]")
        return True, None, None, True


def _stop_lab(lab_id: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Stop a Docker lab."""
    container_name = f"cyberteacher-{lab_id}"
    cmd = ["docker", "stop", container_name]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, check=False
        )
        if result.returncode == 0:
            state = get_state()
            running = getattr(state, "running_labs", [])
            if lab_id in running:
                running.remove(lab_id)
                state.running_labs = running
                from handlers.debt import clear_debt

                clear_debt("", count=1, prefix=f"Лаба: {lab_id}")
            console.print(f"[green]✅ Лаборатория {lab_id} остановлена[/green]")
        else:
            console.print(
                f"[yellow]Лаборатория не была запущена или уже остановлена[/yellow]"
            )
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def _lab_status() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Show status of running labs."""
    state = get_state()
    running = getattr(state, "running_labs", [])
    if not running:
        console.print("[yellow]Нет запущенных лабораторий[/yellow]")
        return True, None, None, True

    table = Table(title="📊 Запущенные лаборатории")
    table.add_column("ID", style="cyan")
    table.add_column("Название", style="green")
    table.add_column("Порты", style="magenta")

    for lab_id in running:
        lab = DOCKER_LABS.get(lab_id, {})
        ports = lab.get("ports", {})
        ports_str = ", ".join(f"{host}:{cont}" for host, cont in ports.items())
        table.add_row(lab_id, lab.get("name", lab_id), ports_str)

    console.print(table)
    return True, None, None, True


def handle_container_check(
    action: str,
) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Check Docker containers status."""
    return _lab_status()


def run_docker_cmd(args: List[str], timeout: int = 60) -> Tuple[int, str, str]:
    """Run a docker command and return (returncode, stdout, stderr)."""
    cmd = ["docker"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Docker command timed out"
    except FileNotFoundError:
        return -1, "", "Docker not found"
    except Exception as e:
        return -1, "", str(e)
