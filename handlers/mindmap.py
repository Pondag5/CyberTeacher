"""Модуль Mind Map — ASCII-визуализация структуры тем.

Команды:
    /mindmap               — Карта всех тем
    /mindmap <topic>       — Карта конкретной темы
    /mindmap help          — Справка
"""

from typing import Dict, List, Tuple

from rich.panel import Panel

from ui import console

TOPIC_TREE: dict[str, list[str]] = {
    "CyberSecurity": [
        "Network Security",
        "Web Security",
        "Cryptography",
        "Malware Analysis",
        "Forensics",
        "OSINT",
        "Social Engineering",
    ],
    "Network Security": [
        "Firewalls",
        "IDS/IPS",
        "VPN",
        "DNS Security",
        "DDoS Protection",
        "Network Scanning",
    ],
    "Web Security": [
        "SQL Injection",
        "XSS",
        "CSRF",
        "Authentication",
        "Session Management",
        "API Security",
    ],
    "Cryptography": [
        "Symmetric (AES, DES)",
        "Asymmetric (RSA, ECC)",
        "Hashing (SHA, MD5)",
        "Digital Signatures",
        "PKI & Certificates",
        "Key Management",
    ],
    "Malware Analysis": [
        "Static Analysis",
        "Dynamic Analysis",
        "Reverse Engineering",
        "Sandboxing",
        "IOC Extraction",
        "YARA Rules",
    ],
    "Forensics": [
        "Disk Forensics",
        "Memory Forensics",
        "Network Forensics",
        "Log Analysis",
        "Timeline Reconstruction",
        "Evidence Handling",
    ],
    "OSINT": [
        "Search Engines",
        "Social Media",
        "Domain Recon",
        "Email Lookup",
        "Metadata Analysis",
        "Shodan/Censys",
    ],
    "Social Engineering": [
        "Phishing",
        "Pretexting",
        "Baiting",
        "Tailgating",
        "Vishing",
        "Defense Training",
    ],
}


def _build_ascii_tree(topic: str, visited: set = None, prefix: str = "", is_last: bool = True) -> str:
    """Рекурсивное построение ASCII-дерева."""
    if visited is None:
        visited = set()

    if topic in visited:
        return ""
    visited.add(topic)

    connector = "└── " if is_last else "├── "
    line = f"{prefix}{connector}{topic}\n" if prefix else f"{topic}\n"

    children = TOPIC_TREE.get(topic, [])
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        if prefix:
            extension = "    " if is_last else "│   "
        else:
            extension = ""
        line += _build_ascii_tree(child, visited, prefix + extension, is_last_child)

    return line


def _display_mindmap(topic: str = None) -> None:
    """Вывести mind map."""
    if topic:
        tree = _build_ascii_tree(topic)
        console.print(Panel(tree, title=f"🧠 Mind Map: {topic}", border_style="cyan"))
    else:
        tree = _build_ascii_tree("CyberSecurity")
        console.print(Panel(tree, title="🧠 CyberSecurity Mind Map", border_style="cyan"))

    console.print("\n[dim]Используйте /mindmap <тема> для детализации.[/dim]")


def handle_mindmap(args: str) -> tuple[str, bool]:
    """Главный обработчик команды /mindmap."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "help":
        console.print(Panel(
            "[bold]Команды mind map:[/bold]\n"
            "/mindmap               — Карта всех тем\n"
            "/mindmap <topic>       — Карта конкретной темы",
            border_style="yellow",
        ))
        return "", True
    elif subcommand and subcommand != "mindmap":
        _display_mindmap(subcommand)
        return "", True
    else:
        _display_mindmap(query if query else None)
        return "", True
