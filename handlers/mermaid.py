# handlers/mermaid.py — Mermaid-инфографика (M-09)
"""Генерация Mermaid-диаграмм для mindmap и схем."""

from typing import Any

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()

DIAGRAM_TYPES = {
    "mindmap": "Интеллект-карта (иерархическая структура)",
    "flowchart": "Блок-схема процесса",
    "sequence": "Диаграмма последовательности",
    "graph": "Граф связей",
    "pie": "Круговая диаграмма",
}

MERMAID_TOPICS = {
    "sqli": {
        "type": "flowchart",
        "title": "SQL Injection Attack Flow",
        "diagram": """flowchart TD
    A[Атака SQL Injection] --> B{Тип атаки}
    B -->|In-Band| C[Error-based]
    B -->|In-Band| D[Union-based]
    B -->|Blind| E[Boolean-based]
    B -->|Blind| F[Time-based]
    B -->|OOB| G[DNS exfiltration]
    C --> H[Получение данных]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I[Защита: Prepared Statements]""",
    },
    "xss": {
        "type": "flowchart",
        "title": "XSS Attack Vectors",
        "diagram": """flowchart LR
    A[XSS Атака] --> B[Stored XSS]
    A --> C[Reflected XSS]
    A --> D[DOM-based XSS]
    B --> E[База данных]
    C --> F[URL параметр]
    D --> G[JavaScript DOM]
    E --> H[Выполнение в браузере]
    F --> H
    G --> H
    H --> I[Защита: CSP + Encoding]""",
    },
    "network": {
        "type": "graph",
        "title": "Network Security Layers",
        "diagram": """graph TD
    A[Network Security] --> B[Firewall]
    A --> C[IDS/IPS]
    A --> D[VPN]
    A --> E[Segmentation]
    B --> F[Packet Filter]
    B --> G[Stateful]
    C --> H[Signature-based]
    C --> I[Anomaly-based]
    D --> J[IPSec]
    D --> K[SSL/TLS]
    E --> L[VLAN]
    E --> M[Zero Trust]""",
    },
    "kill_chain": {
        "type": "flowchart",
        "title": "Cyber Kill Chain",
        "diagram": """flowchart LR
    A[Reconnaissance] --> B[Weaponization]
    B --> C[Delivery]
    C --> D[Exploitation]
    D --> E[Installation]
    E --> F[Command & Control]
    F --> G[Actions on Objectives]
    style A fill:#ff9999
    style G fill:#99ff99""",
    },
    "mitre": {
        "type": "mindmap",
        "title": "MITRE ATT&CK Framework",
        "diagram": """mindmap
  root((MITRE ATT&CK))
    Initial Access
      Phishing
      Exploit Public App
      Valid Accounts
    Execution
      PowerShell
      Scripting
    Persistence
      Registry Run Keys
      Scheduled Task
    Privilege Escalation
      Exploitation
      Access Token Manipulation
    Defense Evasion
      Obfuscation
      Rootkit
    Credential Access
      Brute Force
      OS Credential Dumping
    Lateral Movement
      Remote Services
      Internal Spearphishing""",
    },
    "owasp": {
        "type": "pie",
        "title": "OWASP Top 10 Distribution",
        "diagram": """pie title OWASP Top 10 2021
    "Broken Access Control" : 25
    "Cryptographic Failures" : 15
    "Injection" : 20
    "Insecure Design" : 10
    "Security Misconfiguration" : 12
    "Vulnerable Components" : 8
    "Auth Failures" : 5
    "Data Integrity" : 3
    "Logging Failures" : 1
    "SSRF" : 1""",
    },
}


def handle_mermaid(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Генерация Mermaid-диаграмм."""
    parts = action.split(maxsplit=2)

    if len(parts) == 1:
        console.print(Panel(
            "[bold cyan]📊 Mermaid-инфографика[/bold cyan]\n\n"
            "Использование:\n"
            "  /mermaid list               — доступные диаграммы\n"
            "  /mermaid show <тема>        — показать диаграмму\n"
            "  /mermaid generate <тема>    — сгенерировать через LLM\n\n"
            "Темы: sqli, xss, network, kill_chain, mitre, owasp",
            title="MERMAID",
            border_style="cyan",
        ))
        return True, None, None, True

    subcommand = parts[1].lower()

    if subcommand == "list":
        console.print("[bold cyan]📋 Доступные диаграммы[/bold cyan]\n")
        for tid, t in MERMAID_TOPICS.items():
            console.print(f"  [cyan]{tid:<15}[/cyan] [{t['type']}] {t['title']}")
        console.print()
        return True, None, None, True

    if subcommand == "show":
        if len(parts) < 3:
            console.print("[yellow]Укажите тему: /mermaid show <тема>[/yellow]")
            return True, None, None, True
        topic = parts[2].strip().lower()
        return _show_diagram(topic)

    if subcommand == "generate":
        if len(parts) < 3:
            console.print("[yellow]Укажите тему: /mermaid generate <тема>[/yellow]")
            return True, None, None, True
        topic = parts[2].strip()
        return _generate_diagram(topic)

    console.print("[yellow]Неизвестная подкоманда. /mermaid для справки.[/yellow]")
    return True, None, None, True


def _show_diagram(topic: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Показать готовую диаграмму."""
    if topic not in MERMAID_TOPICS:
        console.print(f"[red]❌ Тема '{topic}' не найдена[/red]")
        console.print("[dim]Доступные: " + ", ".join(MERMAID_TOPICS.keys()) + "[/dim]")
        return True, None, None, True

    d = MERMAID_TOPICS[topic]
    console.print(Panel(
        f"[bold]{d['title']}[/bold]\n\n"
        f"[dim]Тип: {d['type']}[/dim]\n\n"
        f"[yellow]```mermaid\n{d['diagram']}\n```[/yellow]\n\n"
        "[dim]Скопируйте код в https://mermaid.live для визуализации[/dim]",
        title=f"📊 {d['title']}",
        border_style="cyan",
    ))

    state = get_state()
    state.mermaid_views = getattr(state, "mermaid_views", 0) + 1
    state.save_to_file()

    return True, None, None, True


def _generate_diagram(topic: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Сгенерировать диаграмму через LLM."""
    from config import LazyLoader

    llm = LazyLoader.get_llm()
    if llm is None:
        console.print("[red]❌ LLM недоступна[/red]")
        return True, None, None, True

    prompt = f"""Создай Mermaid-диаграмму для темы кибербезопасности: {topic}

Правила:
1. Используй только валидный Mermaid синтаксис
2. Тип: mindmap, flowchart, graph, sequence или pie
3. Начни с указания типа (например: flowchart TD)
4. Не используй markdown code blocks — только чистый Mermaid код
5. Добавь комментарии на русском внутри диаграммы если возможно

Верни ТОЛЬКО Mermaid код, без пояснений."""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        console.print(Panel(
            f"[yellow]```mermaid\n{content.strip()}\n```[/yellow]\n\n"
            "[dim]Визуализация: https://mermaid.live[/dim]",
            title=f"📊 Сгенерировано: {topic}",
            border_style="cyan",
        ))
    except Exception as e:
        console.print(f"[red]Ошибка генерации: {e}[/red]")

    return True, None, None, True
