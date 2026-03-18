"""
🎓 Учебные траектории - курсы от учителя
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Topic:
    name: str
    description: str
    labs: list[str]
    quiz_topics: list[str]
    kali_tools: list[str] | None = None


# Команды Kali Linux для каждой уязвимости
KALI_COMMANDS = {
    "sql": {
        "name": "SQL Инъекция",
        "tools": ["sqlmap", "burpsuite", "ffuf"],
        "commands": {
            "sqlmap": [
                "sqlmap -u 'http://localhost:8080/vulnerabilities/sqli/?id=1' --dbs",
                "sqlmap -u 'http://localhost:8080/vulnerabilities/sqli/?id=1' -D dvwa --tables",
                "sqlmap -u 'http://localhost:8080/vulnerabilities/sqli/?id=1' -D dvwa -T users --dump",
            ],
            "burp": [
                "Запусти Burp Suite",
                "Перехвати запрос",
                "Измени параметр id=1' OR '1'='1",
            ],
        },
        "tutorial": "SQL инъекция позволяет читать/модифицировать базу данных. На DVWA введи: 1' OR '1'='1",
    },
    "xss": {
        "name": "XSS",
        "tools": ["burpsuite", "xsstrike", "beef"],
        "commands": {
            "basic": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert(1)>",
                "<svg onload=alert(1)>",
            ],
            "xsstrike": [
                "xsstrike -u 'http://localhost:8080/vulnerabilities/xss_r/?name=test'"
            ],
        },
        "tutorial": "XSS - выполнение JS в браузере жертвы. На DVWA введи: <script>alert(1)</script>",
    },
    "network": {
        "name": "Сетевая разведка",
        "tools": ["nmap", "netdiscover", "zenmap"],
        "commands": {
            "nmap": [
                "nmap -sV -p- 192.168.1.1       # Сканирование портов",
                "nmap -A 192.168.1.1            # Агрессивное сканирование",
                "nmap -sV --script=vuln 192.168.1.1  # С уязвимостями",
            ],
            "netdiscover": ["netdiscover -r 192.168.1.0/24  # ARP сканирование"],
        },
        "tutorial": "Nmap - основной инструмент сканирования. Используй для поиска открытых портов и сервисов.",
    },
    "burp": {
        "name": "Burp Suite",
        "tools": ["burpsuite"],
        "commands": {
            "proxy": [
                "Настрой прокси в браузере: 127.0.0.1:8080",
                "Включи Intercept",
                "Изменяй запросы!",
            ],
            "repeater": ["Отправь запрос в Repeater", "Экспериментируй с параметрами"],
        },
        "tutorial": "Burp Suite - основной инструмент веб-аудита. Перехватывай и модифицируй HTTP запросы.",
    },
    "hash": {
        "name": "Взлом паролей",
        "tools": ["hashcat", "john", "hydra"],
        "commands": {
            "hashcat": [
                "hashcat -m 0 hash.txt wordlist.txt     # MD5",
                "hashcat -m 1000 hash.txt wordlist.txt   # NTLM",
            ],
            "john": [
                "john --format=raw-md5 hash.txt",
                "john --wordlist=rockyou.txt hash.txt",
            ],
            "hydra": [
                "hydra -L users.txt -P passwords.txt 192.168.1.1 ssh",
                "hydra -l admin -P rockyou.txt localhost http-post-form '/login:user=^USER^&pass=^PASS^:F=incorrect'",
            ],
        },
        "tutorial": "Hashcat/John - для взлома хешей. Hydra - для брутфорса сервисов.",
    },
    "privesc": {
        "name": "Privilege Escalation",
        "tools": ["linPEAS", "linenum", "linux-exploit-suggester"],
        "commands": {
            "linPEAS": [
                "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"
            ],
            "check": [
                "sudo -l                              # Что можешь запускать от root",
                "find / -writable -type f 2>/dev/null  # Записываемые файлы",
                "cat /etc/passwd                      # Пользователи",
            ],
        },
        "tutorial": "linPEAS автоматически ищет пути к root. Запусти на целевой машине.",
    },
    "CTF": {
        "name": "CTF инструменты",
        "tools": ["gobuster", "dirb", "steghide", "zsteg"],
        "commands": {
            "dirb": [
                "gobuster dir -u http://localhost:8080 -w /usr/share/wordlists/dirb/common.txt",
                "dirb http://localhost:8080/",
            ],
            "steghide": ["steghide extract -sf image.jpg", "zsteg image.png -a"],
        },
        "tutorial": "gobuster/dirb - для поиска скрытых директорий. steghide - для стеганографии.",
    },
}

# Учебные траектории
COURSES = {
    "web-basics": {
        "name": "Основы веб-безопасности",
        "desc": "Базовые уязвимости веб-приложений",
        "level": "beginner",
        "topics": [
            Topic(
                name="SQL Injection",
                description="Инъекции в базу данных",
                labs=["dvwa", "sqlilab"],
                quiz_topics=["sql"],
            ),
            Topic(
                name="XSS",
                description="Cross-Site Scripting",
                labs=["dvwa", "juice"],
                quiz_topics=["xss"],
            ),
            Topic(
                name="CSRF",
                description="Подделка межсайтовых запросов",
                labs=["dvwa"],
                quiz_topics=["web"],
            ),
        ],
    },
    "web-advanced": {
        "name": "Продвинутая веб-безопасность",
        "desc": "Сложные уязвимости",
        "level": "intermediate",
        "topics": [
            Topic(
                name="JWT уязвимости",
                description="Атаки на JSON Web Tokens",
                labs=["juice", "jwt-lab"],
                quiz_topics=["jwt", "auth"],
            ),
            Topic(
                name="IDOR",
                description="Insecure Direct Object Reference",
                labs=["juice", "dvna"],
                quiz_topics=["web"],
            ),
            Topic(
                name="NoSQL Injection",
                description="Инъекции в NoSQL базы",
                labs=["juice"],
                quiz_topics=["nosql", "db"],
            ),
        ],
    },
    "network": {
        "name": "Сетевая безопасность",
        "desc": "Сканирование и эксплуатация сетей",
        "level": "intermediate",
        "topics": [
            Topic(
                name="Сканирование",
                description="Nmap, анализ портов",
                labs=["metasploitable2"],
                quiz_topics=["network"],
            ),
            Topic(
                name="SMB эксплуатация",
                description="Атаки на SMB",
                labs=["metasploitable2"],
                quiz_topics=["network", "windows"],
            ),
            Topic(
                name="FTP/SSH",
                description="Брутфорс и эксплуатация",
                labs=["metasploitable2"],
                quiz_topics=["network", "linux"],
            ),
        ],
    },
    "api": {
        "name": "Безопасность API",
        "desc": "Уязвимости REST API",
        "level": "intermediate",
        "topics": [
            Topic(
                name="REST API уязвимости",
                description="Атаки на API",
                labs=["vulnapi", "crapi"],
                quiz_topics=["api", "rest"],
            ),
            Topic(
                name="Authentication bypass",
                description="Обход аутентификации",
                labs=["vulnapi", "dvna"],
                quiz_topics=["auth", "jwt"],
            ),
        ],
    },
    "privesc": {
        "name": "Privilege Escalation",
        "desc": "Повышение привилегий",
        "level": "advanced",
        "topics": [
            Topic(
                name="Linux Privilege Escalation",
                description="От user до root",
                labs=["metasploitable2", "metasploitable3"],
                quiz_topics=["linux", "privesc"],
            ),
        ],
    },
    "ctf-starter": {
        "name": "CTF Starter",
        "desc": "Подготовка к CTF",
        "level": "beginner",
        "topics": [
            Topic(
                name="Основы веба",
                description="Базовые уязвимости",
                labs=["dvwa", "picklerick"],
                quiz_topics=["web", "sql", "xss"],
            ),
            Topic(
                name="Энumeration",
                description="Разведка и сканирование",
                labs=["metasploitable2"],
                quiz_topics=["network"],
            ),
        ],
    },
}

LEVELS = {
    "beginner": {
        "name": "Новичок",
        "emoji": "🌱",
        "description": "Только начинаешь - учим основы",
    },
    "intermediate": {
        "name": "Средний",
        "emoji": "🌿",
        "description": "Есть база - углубляемся",
    },
    "advanced": {
        "name": "Продвинутый",
        "emoji": "🌳",
        "description": "Сложные техники",
    },
}


def get_course(course_id: str) -> dict | None:
    """Получить курс по ID"""
    return COURSES.get(course_id)


# Сохраняем маппинг номеров для handle_course
COURSE_MAP = {str(i): cid for i, (cid, _) in enumerate(list(COURSES.items()), 1)}


def list_courses() -> str:
    """Список всех курсов"""
    # Создаем нумерованный список
    course_list = list(COURSES.items())

    result = "📚 УЧЕБНЫЕ КУРСЫ:\n\n"

    for i, (course_id, course) in enumerate(course_list, 1):
        level = LEVELS.get(course["level"], {})
        emoji = level.get("emoji", "📖")
        result += f"{i}. {emoji} {course['name']} [{course['level']}]\n"
        result += f"   {course['desc']}\n"
        result += f"   Тем: {len(course['topics'])}\n\n"

    result += "📝 Использование:\n"
    result += "   /course <номер> - начать курс\n"
    result += "   /courses       - показать список\n\n"
    result += "Пример: /course 1"

    return result


def start_course(course_id: str) -> str:
    """Начать курс - показать первое задание"""
    course = get_course(course_id)

    if not course:
        return f"❌ Курс '{course_id}' не найден. Напиши /courses для списка."

    level = LEVELS.get(course["level"], {})
    emoji = level.get("emoji", "📖")

    result = f"""
╔══════════════════════════════════════════════════════╗
║  {emoji} КУРС: {course["name"]}                      ║
╠══════════════════════════════════════════════════════╣
║  Уровень: {course["level"]}                                    ║
║  Описание: {course["desc"]}                        ║
║  Тем в курсе: {len(course["topics"])}                              ║
╚══════════════════════════════════════════════════════╝

🎯 ПЕРВОЕ ЗАДАНИЕ:

"""

    # Первая тема
    if course["topics"]:
        topic = course["topics"][0]
        result += f"""
📌 Тема: {topic.name}
   {topic.description}

🔧 Лаборатории для практики:
"""
        for lab_id in topic.labs:
            result += f"   - {lab_id}\n"

        result += f"""
📝 Когда запустишь лабу - спроси меня "что делать?" и я дам тебе квест!

💡 Начни с: /lab start {topic.labs[0]}
"""

    return result


def get_course_progress(course_id: str, current_topic: int) -> str:
    """Показать прогресс по курсу"""
    course = get_course(course_id)
    if not course:
        return "Курс не найден"

    topics = course["topics"]
    if current_topic >= len(topics):
        return f"""
🎉 ПОЗДРАВЛЯЮ! Курс '{course["name"]}' пройден!

Ты изучил:
"""

    topic = topics[current_topic]
    return f"""
📚 Курс: {course["name"]}
📍 Прогресс: {current_topic + 1}/{len(topics)}

📌 ТЕКУЩАЯ ТЕМА: {topic.name}
   {topic.description}

🔧 Лабы: {", ".join(topic.labs)}
📝 Квизы: {", ".join(topic.quiz_topics)}

Команды:
   /lab start <name> - запустить лабу
   /quiz {topic.quiz_topics[0]} - пройти квиз
   /next - следующая тема
"""
