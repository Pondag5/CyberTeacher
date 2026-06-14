"""Backdoors — скрытые бэкдоры в скомпрометированных системах (Глава 5)."""

import json
import os
import random
from typing import List, Dict, Any, Optional

from state import get_state

BACKDOORS_FILE = "./memory/backdoors.json"

DEFAULT_BACKDOORS = [
    {
        "id": "bd_001",
        "name": "DVWA Shell",
        "target": "dvwa.local",
        "type": "web_shell",
        "access": "www-data",
        "persistence": "cron",
        "discovered_chapter": 3,
        "risk": "medium",
        "flags": ["flag{bd_dvwa_root}"],
        "description": "Загружен через уязвимость загрузки файлов. Даёт доступ к БД DVWA.",
        "active": True,
    },
    {
        "id": "bd_002",
        "name": "Juice Shop Admin",
        "target": "juice-shop.local",
        "type": "jwt_forgery",
        "access": "admin",
        "persistence": "token",
        "discovered_chapter": 4,
        "risk": "high",
        "flags": ["flag{bd_juice_admin}"],
        "description": "Подделан JWT с алгоритмом none. Полный доступ к админке.",
        "active": True,
    },
    {
        "id": "bd_003",
        "name": "Metasploitable SSH",
        "target": "metasploitable.local",
        "type": "ssh_key",
        "access": "root",
        "persistence": "authorized_keys",
        "discovered_chapter": 5,
        "risk": "critical",
        "flags": ["flag{bd_msf_root}"],
        "description": "Скомпрометирован приватный ключ. Прямой root доступ.",
        "active": True,
    },
    {
        "id": "bd_004",
        "name": "WebGoat DB",
        "target": "webgoat.local",
        "type": "sql_injection",
        "access": "postgres",
        "persistence": "trigger",
        "discovered_chapter": 5,
        "risk": "high",
        "flags": ["flag{bd_webgoat_db}"],
        "description": "Blind SQLi в поиске. Триггер на INSERT даёт постоянный доступ к БД.",
        "active": True,
    },
    {
        "id": "bd_005",
        "name": "SQLi Labs Backdoor",
        "target": "sqli-labs.local",
        "type": "webshell",
        "access": "www-data",
        "persistence": "file_upload",
        "discovered_chapter": 4,
        "risk": "medium",
        "flags": ["flag{bd_sqli_shell}"],
        "description": "Загрузка шелла через UNION-based инъекцию в Less-9.",
        "active": True,
    },
    {
        "id": "bd_006",
        "name": "DVWA Command Injection",
        "target": "dvwa.local",
        "type": "reverse_shell",
        "access": "www-data",
        "persistence": "systemd",
        "discovered_chapter": 5,
        "risk": "critical",
        "flags": ["flag{bd_dvwa_rev}"],
        "description": "Reverse shell через ping-инъекцию. Установлен systemd-сервис для персистентности.",
        "active": True,
    },
    {
        "id": "bd_007",
        "name": "Hidden FTP",
        "target": "archive.local",
        "type": "ftp_anonymous",
        "access": "ftp",
        "persistence": "config",
        "discovered_chapter": 6,
        "risk": "low",
        "flags": ["flag{bd_ftp_hidden}"],
        "description": "Анонимный FTP с write-доступом. Спрятан на нестандартном порту 2121.",
        "active": True,
    },
    {
        "id": "bd_008",
        "name": "Ghost DB",
        "target": "ghost-sector.local",
        "type": "mongodb_exposed",
        "access": "admin",
        "persistence": "none",
        "discovered_chapter": 6,
        "risk": "critical",
        "flags": ["flag{bd_ghost_db}"],
        "description": "MongoDB без авторизации на 27017. Полная база фракции Ghost.",
        "active": True,
    },
]


def _load_backdoors() -> List[Dict[str, Any]]:
    if not os.path.exists(BACKDOORS_FILE):
        _save_backdoors(DEFAULT_BACKDOORS)
        return DEFAULT_BACKDOORS[:]
    try:
        with open(BACKDOORS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else DEFAULT_BACKDOORS[:]
    except (json.JSONDecodeError, OSError):
        return DEFAULT_BACKDOORS[:]


def _save_backdoors(backdoors: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(BACKDOORS_FILE), exist_ok=True)
    with open(BACKDOORS_FILE, "w", encoding="utf-8") as f:
        json.dump(backdoors, f, indent=2, ensure_ascii=False)


def get_available_backdoors() -> List[Dict[str, Any]]:
    """Вернуть бэкдоры, доступные для текущей главы."""
    state = get_state()
    all_bd = _load_backdoors()
    available = []
    for bd in all_bd:
        if state.current_chapter >= bd["discovered_chapter"] and bd.get("active", True):
            available.append(bd)
    return available


def format_backdoor(bd: Dict[str, Any], verbose: bool = False) -> str:
    risk_colors = {"low": "green", "medium": "yellow", "high": "red", "critical": "bold red"}
    color = risk_colors.get(bd.get("risk", "medium"), "white")

    lines = [
        f"\n{'='*60}",
        f"[BACKDOOR] {bd['name']} ({bd['id']})",
        f"{'='*60}",
        f"  Target:    {bd['target']}",
        f"  Type:      {bd['type']}",
        f"  Access:    {bd['access']}",
        f"  Persistence: {bd['persistence']}",
        f"  Risk:      [{color}]{bd['risk'].upper()}[/{color}]",
        f"  Chapter:   {bd['discovered_chapter']}",
        f"  Status:    {'ACTIVE' if bd.get('active') else 'REMOVED'}",
        f"  Desc:      {bd['description']}",
    ]
    if verbose and bd.get("flags"):
        lines.append(f"  Flags:     {', '.join(bd['flags'])}")
    lines.append("="*60)
    return "\n".join(lines)


def handle_backdoor(args: str = "") -> str:
    """CLI: /backdoor [list|remove <id>|info <id>|random]."""
    state = get_state()
    available = get_available_backdoors()

    if not available:
        return "[Backdoors] Пока недоступно. Пройди Главу 3+."

    parts = args.strip().split()
    sub = parts[0].lower() if parts else "list"

    if sub == "list":
        lines = ["[Backdoors] Доступные точки входа:"]
        for bd in available:
            risk_tag = bd['risk'].upper()
            lines.append(f"  {bd['id']} — {bd['name']} ({bd['target']}) [RISK: {risk_tag}]")
        lines.append(f"\nВсего: {len(available)}. /backdoor info <id> | remove <id> | random")
        return "\n".join(lines)

    if sub == "random":
        bd = random.choice(available)
        return format_backdoor(bd, verbose=True)

    if sub == "info" and len(parts) > 1:
        bid = parts[1]
        for bd in available:
            if bd["id"] == bid:
                return format_backdoor(bd, verbose=True)
        return f"[Backdoors] Бэкдор '{bid}' не найден."

    if sub == "remove" and len(parts) > 1:
        bid = parts[1]
        return remove_backdoor(bid)

    return "[Backdoors] Использование: /backdoor [list|info <id>|remove <id>|random]"


def remove_backdoor(bid: str) -> str:
    """Удалить/деактивировать бэкдор."""
    all_bd = _load_backdoors()
    found = False
    for bd in all_bd:
        if bd["id"] == bid:
            if not bd.get("active", True):
                return f"[Backdoors] '{bid}' уже удалён."
            bd["active"] = False
            found = True
            break

    if not found:
        return f"[Backdoors] Бэкдор '{bid}' не найден."

    _save_backdoors(all_bd)

    # Эффекты удаления
    state = get_state()
    state.noise_level = max(0, state.noise_level - 5)
    flags_gained = 0

    for bd in all_bd:
        if bd["id"] == bid and bd.get("flags"):
            for flag in bd["flags"]:
                if flag not in getattr(state, "collected_flags", []):
                    state.collected_flags = getattr(state, "collected_flags", [])
                    state.collected_flags.append(flag)
                    flags_gained += 1

    msg = f"[Backdoors] '{bid}' деактивирован. Noise -5."
    if flags_gained:
        msg += f" Получен флаг(и): {flags_gained}."
    return msg