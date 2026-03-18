"""
🔐 Практика - CTF, HTB, Docker лабы
"""

import json
import random
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional

# Проверка доступности Docker при импорте
DOCKER_AVAILABLE = shutil.which("docker") is not None
if not DOCKER_AVAILABLE:
    print(
        "[yellow]⚠️ Docker не найден в системе. Практические лаборатории будут недоступны.[/yellow]"
    )

DOCKER_LABS = {
    # Web уязвимости
    "dvwa": {
        "name": "DVWA",
        "desc": "Damn Vulnerable Web App - SQLi, XSS, CSRF, File Inc, Command Inj",
        "image": "ghcr.io/digininja/dvwa:latest",
        "ports": {"8080": "80"},
        "env": {"DB_HOST": "dvwa-db"},
        "db": "mariadb:10.10",
        "tags": ["web", "sqli", "xss", "beginner"],
    },
    "bwapp": {
        "name": "bWAPP",
        "desc": "Buggy Web App - 100+ уязвимостей (SQLi, XSS, CSRF, XML, LDAP)",
        "image": "raesene/bwapp",
        "ports": {"8088": "80"},
        "tags": ["web", "beginner", "intermediate"],
    },
    "juice": {
        "name": "OWASP Juice Shop",
        "desc": "Современные уязвимости - XSS, IDOR, RCE, JWT, NoSQL",
        "image": "bkimminich/juice-shop",
        "ports": {"3000": "3000"},
        "tags": ["web", "intermediate", "jwt", "nosql"],
    },
    "webgoat": {
        "name": "WebGoat",
        "desc": "OWASP WebGoat - обучающая платформа",
        "image": "webgoat/webgoat",
        "ports": {"8080": "8080"},
        "tags": ["web", "beginner", "education"],
    },
    "dvna": {
        "name": "DVNA",
        "desc": "Damn Vulnerable Node App - Node.js уязвимости",
        "image": "securityunion/dvna",
        "ports": {"9090": "3000"},
        "tags": ["web", "nodejs", "intermediate"],
    },
    "ninja": {
        "name": "Dodgy Ninja",
        "desc": "Уязвимый Node.js - IDOR, XSS, SSRF, SQLi",
        "image": "citizenstig/dodgy-ninja",
        "ports": {"8085": "80"},
        "tags": ["web", "nodejs", "intermediate"],
    },
    # SQL Injection
    "sqlilab": {
        "name": "SQLi Labs",
        "desc": "SQL Injection практика - 32 уровня",
        "image": "citizenstig/nowasp",
        "ports": {"8000": "8000"},
        "tags": ["sqli", "beginner"],
    },
    "sqlmap": {
        "name": "SQLMap Demo",
        "desc": "Тест SQLMap на уязвимой БД",
        "image": "paoloo/sqlmap-lab",
        "ports": {"8888": "80"},
        "tags": ["sqli", "tools"],
    },
    # Linux/Network
    "metasploitable2": {
        "name": "Metasploitable 2",
        "desc": "Уязвимый Linux - SMB, FTP, Telnet, SSH, MySQL",
        "image": "tleemcjr/metasploitable2",
        "ports": {
            "2222": "22",
            "4444": "4444",
            "8000": "8000",
            "8080": "80",
            "21": "21",
            "23": "23",
        },
        "tags": ["linux", "network", "intermediate", "privesc"],
    },
    "metasploitable3": {
        "name": "Metasploitable 3 (Linux)",
        "desc": "Metasploitable 3 - Linux версия",
        "image": "rapid7/metasploitable3-amd64",
        "ports": {"2200": "22", "4444": "4444"},
        "tags": ["linux", "network", "advanced"],
    },
    # Windows
    "metasploitable3-win": {
        "name": "Metasploitable 3 (Windows)",
        "desc": "Metasploitable 3 - Windows версия",
        "image": "rapid7/metasploitable3-eve-ng",
        "ports": {"3389": "3389", "8080": "80"},
        "tags": ["windows", "network", "advanced"],
    },
    # CTF
    "ctfd": {
        "name": "CTFd",
        "desc": "Платформа для CTF соревнований",
        "image": "ctfd/ctfd",
        "ports": {"8000": "8000"},
        "tags": ["ctf", "platform"],
    },
    "rootthebox": {
        "name": "Root The Box",
        "desc": "CTF платформа с банковскими кейсами",
        "image": "misterch0c/rootthebox",
        "ports": {"8000": "80"},
        "tags": ["ctf", "platform"],
    },
    # Vulnerable APIs
    "vulnapi": {
        "name": "Vulnerable REST API",
        "desc": "Уязвимое API - NoSQL, IDOR, Auth Bypass",
        "image": "incredibleindishell/vulnerable-rest-api",
        "ports": {"8080": "80"},
        "tags": ["api", "rest", "intermediate"],
    },
    "crapi": {
        "name": "CRAPI",
        "desc": "Completely Ridiculous API - JWT, SSRF, Race Condition",
        "image": "doublebin/crapi",
        "ports": {"8888": "80"},
        "tags": ["api", "jwt", "ssrf"],
    },
    # Auth & JWT
    "jwt-lab": {
        "name": "JWT Lab",
        "desc": "Лаборатория JWT токенов",
        "image": "shyiko/jwt-lab",
        "ports": {"8080": "8080"},
        "tags": ["jwt", "auth", "beginner"],
    },
    # Mobile
    "dvma": {
        "name": "DVMA",
        "desc": "Damn Vulnerable Mobile App (Android)",
        "image": "securityunion/dvma",
        "ports": {"8080": "80"},
        "tags": ["mobile", "android"],
    },
    # Cloud
    "cloudgoat": {
        "name": "CloudGoat",
        "desc": "Уязвимый AWS/GCP - IAM, S3, Lambda",
        "image": "rhinosecuritylabs/cloudgoat",
        "ports": {"8000": "8000"},
        "tags": ["cloud", "aws", "advanced"],
    },
    # Misc
    "vulnserver": {
        "name": "VulnServer",
        "desc": "Уязвимый Windows TCP сервер",
        "image": "zeroq/vulnserver",
        "ports": {"9999": "9999"},
        "tags": ["windows", "buffer", "intermediate"],
    },
    "holinow": {
        "name": "Holi-Now",
        "desc": "Уязвимости Holiday API",
        "image": "sandh0li/holinow",
        "ports": {"5000": "5000"},
        "tags": ["api", "intermediate"],
    },
    "picklerick": {
        "name": "Pickle Rick",
        "desc": "Web CTF - RCE, SQLi, Command Injection",
        "image": "blark/rick:latest",
        "ports": {"80": "80"},
        "tags": ["web", "ctf", "beginner"],
    },
}


def run_docker_cmd(args: list[str]) -> tuple:
    """Выполнить docker команду"""
    try:
        result = subprocess.run(
            ["docker"] + args, capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def get_container_status(name: str) -> dict:
    """Проверить статус контейнера"""
    code, stdout, _ = run_docker_cmd(
        ["ps", "-a", "--filter", f"name={name}", "--format", "{{.Status}}"]
    )
    if code == 0 and stdout.strip():
        return {"running": "Up" in stdout, "status": stdout.strip()}
    return {"running": False, "status": "not found"}


def get_container_logs(name: str, lines: int = 50) -> str:
    """Получить логи контейнера"""
    code, stdout, stderr = run_docker_cmd(["logs", "--tail", str(lines), name])
    if code == 0:
        return stdout if stdout else "Логов нет"
    return f"Ошибка: {stderr}"


import shlex


def exec_in_container(name: str, command: str) -> str:
    """Выполнить команду в контейнере (БЕЗОПАСНО)"""
    # Валидация: только alphanumeric и базовые символы
    import re

    if not re.match(r"^[a-zA-Z0-9_\-./\s]+$", command):
        return "❌ Команда содержит запрещённые символы"

    # Запускаем без shell - прямой exec
    code, stdout, stderr = run_docker_cmd(["exec", name] + shlex.split(command))
    if code == 0:
        return stdout if stdout else "Команда выполнена (нет вывода)"
    return f"Ошибка: {stderr}"


def get_all_running_labs() -> dict[str, dict]:
    """Получить статус всех запущенных лаб"""
    result = {}
    for lab_key in DOCKER_LABS:
        web_name = f"{lab_key}-web"
        status = get_container_status(web_name)
        if status["running"]:
            result[lab_key] = {
                "name": DOCKER_LABS[lab_key]["name"],
                "status": status["status"],
                "ports": DOCKER_LABS[lab_key].get("ports", {}),
            }
    return result


def start_lab(lab_name: str) -> str:
    """Запустить лабораторию"""
    if lab_name not in DOCKER_LABS:
        return f"❌ Лаборатория '{lab_name}' не найдена. Доступные: {', '.join(DOCKER_LABS.keys())}"

    lab = DOCKER_LABS[lab_name]
    net_name = f"{lab_name}-net"

    # Проверим сеть
    run_docker_cmd(["network", "create", "-d", "bridge", net_name])

    # Запустим БД если нужна
    if "db" in lab:
        db_name = f"{lab_name}-db"
        status = get_container_status(db_name)
        if not status["running"]:
            db_image = lab["db"]
            run_docker_cmd(
                [
                    "run",
                    "-d",
                    "--name",
                    db_name,
                    "--network",
                    net_name,
                    "-e",
                    "MYSQL_ROOT_PASSWORD=root",
                    "-e",
                    "MYSQL_DATABASE=dvwa",
                    db_image,
                ]
            )

    # Запустим основной контейнер
    web_name = f"{lab_name}-web"
    status = get_container_status(web_name)

    if status["running"]:
        return f"✅ {lab['name']} уже запущен!"

    # Собираем порты
    port_args = []
    for host_port, container_port in lab["ports"].items():
        port_args.extend(["-p", f"{host_port}:{container_port}"])

    # Собираем env
    env_args = []
    if "env" in lab:
        for k, v in lab["env"].items():
            env_args.extend(["-e", f"{k}={v}"])

    run_docker_cmd(
        ["run", "-d", "--name", web_name, "--network", net_name]
        + port_args
        + env_args
        + [lab["image"]]
    )

    return f"""
✅ {lab["name"]} ЗАПУЩЕН!

📖 {lab["desc"]}

🔗 Доступ:
""" + "\n".join([f"   http://localhost:{p}" for p in lab["ports"].keys()])


def stop_lab(lab_name: str) -> str:
    """Остановить лабораторию"""
    if lab_name not in DOCKER_LABS:
        return f"❌ Лаборатория '{lab_name}' не найдена."

    web_name = f"{lab_name}-web"
    db_name = f"{lab_name}-db"

    run_docker_cmd(["rm", "-f", web_name])
    run_docker_cmd(["rm", "-f", db_name])

    return f"🛑 {lab_name} остановлен"


def list_labs() -> str:
    """Список доступных лаб"""
    # Группировка по тегам
    categories = {}
    for key, lab in DOCKER_LABS.items():
        tags = lab.get("tags", ["other"])
        cat = tags[0] if tags else "other"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, lab))

    result = f"🐳 DOCKER ЛАБЫ ({len(DOCKER_LABS)} штук):\n\n"

    # Сортировка категорий
    cat_order = [
        "web",
        "sqli",
        "api",
        "jwt",
        "linux",
        "windows",
        "network",
        "mobile",
        "cloud",
        "ctf",
        "api",
    ]
    sorted_cats = sorted(
        categories.keys(), key=lambda x: cat_order.index(x) if x in cat_order else 99
    )

    for cat in sorted_cats:
        result += f"━━━ {cat.upper()} ━━━\n"
        for key, lab in categories[cat]:
            status = get_container_status(f"{key}-web")
            emoji = "🟢" if status["running"] else "⚪"
            ports = ", ".join([f":{p}" for p in lab["ports"].keys()])
            tags_str = " ".join([f"[{t}]" for t in lab.get("tags", [])])
            result += f"{emoji} {lab['name']} {tags_str}\n"
            result += f"  Ports: {ports}\n"
            result += f"   {lab['desc']}\n"
        result += "\n"

    result += "📝 Команды:\n"
    result += "   /lab          - показать список\n"
    result += "   /lab start <name> - запустить\n"
    result += "   /lab stop <name>  - остановить\n"
    result += "   /lab status      - проверить статус\n"

    return result


@dataclass
class Challenge:
    id: str
    name: str
    category: str
    difficulty: str
    description: str
    technique: str
    tools: list[str]


class PracticeHub:
    """Хаб практических заданий"""

    # Встроенные мини-лабы
    MINI_LABS = [
        Challenge(
            id="lab1",
            name="SQL Injection Lab",
            category="web",
            difficulty="easy",
            description="Найди уязвимость в форме логина",
            technique="UNION-based SQLi",
            tools=["sqlmap", "burp", "curl"],
        ),
        Challenge(
            id="lab2",
            name="Buffer Overflow",
            category="pwn",
            difficulty="medium",
            description="Переполни буфер и получи shell",
            technique="Stack-based BOF",
            tools=["gdb", "python", "objdump"],
        ),
        Challenge(
            id="lab3",
            name="Network Sniffing",
            category="network",
            difficulty="easy",
            description="Анализируй PCAP файл, найди пароль",
            technique="Packet analysis",
            tools=["wireshark", "tshark"],
        ),
        Challenge(
            id="lab4",
            name="Hash Cracking",
            category="crypto",
            difficulty="easy",
            description="Восстанови пароль из хеша",
            technique="Hash cracking",
            tools=["hashcat", "john"],
        ),
        Challenge(
            id="lab5",
            name="XSS Reflected",
            category="web",
            difficulty="easy",
            description="Найди и эксплуатируй XSS",
            technique="DOM XSS",
            tools=["browser", "burp"],
        ),
        Challenge(
            id="lab6",
            name="Privilege Escalation",
            category="os",
            difficulty="medium",
            description="Получи root на Linux машине",
            technique="Linux privesc",
            tools=["linPEAS", "find", "sudo"],
        ),
    ]

    # Категории по сложности
    DIFFICULTY_MAP = {
        "easy": "★☆☆☆☆",
        "medium": "★★☆☆☆",
        "hard": "★★★☆☆",
        "insane": "★★★★★",
    }

    @classmethod
    def get_lab(cls, lab_id: str = None) -> Challenge:
        if lab_id:
            for lab in cls.MINI_LABS:
                if lab.id == lab_id:
                    return lab
        return random.choice(cls.MINI_LABS)

    @classmethod
    def get_by_category(cls, category: str) -> list[Challenge]:
        return [c for c in cls.MINI_LABS if c.category == category]

    @classmethod
    def get_all_categories(cls) -> list[str]:
        return list(set(c.category for c in cls.MINI_LABS))

    @classmethod
    def generate_writeup_template(cls, lab: Challenge) -> str:
        return f"""
# Write-up: {lab.name}

## Информация
- **Категория:** {lab.category}
- **Сложность:** {cls.DIFFICULTY_MAP[lab.difficulty]}
- **Инструменты:** {", ".join(lab.tools)}

## Описание
{lab.description}

## Решение

### 1. Разведка
Опиши здесь твои шаги по разведке...

### 2. Эксплуатация
Как ты использовал {lab.technique}?

### 3. Получение доступа
Что в итоге получилось?

## Выводы
Чему ты научился?
"""


def start_practice(category: str = None, difficulty: str = None) -> str:
    """Начать практику"""
    labs = PracticeHub.MINI_LABS

    if category:
        labs = [l for l in labs if l.category == category]
    if difficulty:
        labs = [l for l in labs if l.difficulty == difficulty]

    if not labs:
        labs = PracticeHub.MINI_LABS

    lab = random.choice(labs)

    return f"""
🔬 ПРАКТИЧЕСКАЯ ЛАБОРАТОРИЯ

🏷️ {lab.name}
📂 {lab.category} | {PracticeHub.DIFFICULTY_MAP[lab.difficulty]}

📖 Описание:
{lab.description}

🎯 Техника: {lab.technique}

🔧 Инструменты: {", ".join(lab.tools)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Подсказка: Начни с разведки!

Когда решишь - запроси /writeup для шаблона
"""


def list_practices() -> str:
    """Список доступных практик"""
    result = "🔬 ДОСТУПНЫЕ ЛАБОРАТОРИИ:\n\n"

    categories = PracticeHub.get_all_categories()
    for cat in categories:
        labs = PracticeHub.get_by_category(cat)
        result += f"📂 {cat.upper()}:\n"
        for lab in labs:
            result += (
                f"  #{lab.id} {lab.name} {PracticeHub.DIFFICULTY_MAP[lab.difficulty]}\n"
            )
        result += "\n"

    return result


# HTB-подобные машины (упрощённо)
HTB_MACHINES = [
    {
        "name": "Blue",
        "os": "Windows",
        "difficulty": "easy",
        "skills": ["SMB", "MS17-010"],
    },
    {
        "name": "Legacy",
        "os": "Windows",
        "difficulty": "easy",
        "skills": ["SMB", "Windows"],
    },
    {"name": "Lame", "os": "Linux", "difficulty": "easy", "skills": ["SMB", "vsftpd"]},
    {"name": "Meow", "os": "Linux", "difficulty": "easy", "skills": ["Telnet"]},
    {"name": "Dawn", "os": "Linux", "difficulty": "easy", "skills": ["FTP", "Web"]},
]


def get_htb_recommendation(user_level: str = "beginner") -> str:
    """Рекомендации HTB машин по уровню"""

    if user_level == "beginner":
        machines = [m for m in HTB_MACHINES if m["difficulty"] == "easy"]
    else:
        machines = HTB_MACHINES

    result = "🎯 РЕКОМЕНДУЕМЫЕ МАШИНЫ HTB:\n\n"
    for m in machines[:5]:
        result += f"💻 {m['name']} ({m['os']}) - {m['difficulty']}\n"
        result += f"   Навыки: {', '.join(m['skills'])}\n\n"

    result += "\n📝 Как начать:\n"
    result += "1. Зарегистрируйся на hackthebox.eu\n"
    result += "2. Скачай VPN из Access\n"
    result += "3. Запусти_machine\n"
    result += "4. Найди флаг в /root/root.txt или /home/user/user.txt\n"

    return result
