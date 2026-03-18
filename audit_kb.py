#!/usr/bin/env python3
"""
🔍 Аудит базы знаний CyberTeacher

Анализирует, какие темы из courses.py покрыты PDF в knowledge_base/
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Директории
KB_DIR = Path("knowledge_base")

# Топики из курсов (основные темы для обучения)
COURSE_TOPICS = {
    # Web Basics
    "SQL Injection": [
        "sql injection",
        "sqli",
        "sqlmap",
        "database injection",
        "mysql injection",
        "postgresql injection",
        "oracle injection",
    ],
    "XSS": [
        "xss",
        "cross site scripting",
        "xsstrike",
        "beef",
        "dom xss",
        "reflected xss",
        "stored xss",
        "dom-based xss",
    ],
    "CSRF": [
        "csrf",
        "cross site request forgery",
        "xsrf",
        "request forgery",
        "double submit",
    ],
    # Web Advanced
    "JWT": [
        "jwt",
        "json web token",
        "jwt attacks",
        "jwt vulnerability",
        "token bypass",
        "none algorithm",
        "jwt none",
    ],
    "IDOR": [
        "idor",
        "insecure direct object reference",
        "direct object reference",
        "object reference",
        "insecure direct object",
    ],
    "NoSQL Injection": [
        "nosql injection",
        "nosql",
        "mongodb injection",
        "mongodb",
        "couchdb injection",
    ],
    # Network
    "Сканирование": [
        "nmap",
        "scanning",
        "port scan",
        "service detection",
        "vulnerability scan",
        "enumeration",
        "network discovery",
    ],
    "SMB": [
        "smb",
        "smbclient",
        "psexec",
        "eternalblue",
        "ms17-010",
        "smb exploitation",
        "windows file sharing",
    ],
    "FTP/SSH": [
        "ftp",
        "ftp brute",
        "ssh",
        "ssh brute",
        "brute force",
        "hydra",
        "medusa",
        "password cracking",
        "telnet",
    ],
    # API
    "REST API": [
        "rest api",
        "graphql",
        "api security",
        "api vulnerability",
        "endpoint security",
        "soap",
        "restful",
    ],
    "Authentication bypass": [
        "auth bypass",
        "authentication bypass",
        "bypass authentication",
        "login bypass",
        "session hijacking",
    ],
    # Privilege Escalation
    "Privilege Escalation": [
        "privilege escalation",
        "privesc",
        "sudo",
        "setuid",
        "capabilities",
        "root",
        "windows privilege escalation",
        "linux privesc",
    ],
    # General
    "Social Engineering": [
        "social engineering",
        "phishing",
        "spear phishing",
        "vishing",
        "pretexting",
        "tailgating",
        "whaling",
    ],
    "Cryptography": [
        "cryptography",
        "encryption",
        "aes",
        "rsa",
        "crypto",
        "tls",
        "ssl",
        "certificate",
        "public key",
        "private key",
    ],
    "Steganography": [
        "steganography",
        "steghide",
        "zsteg",
        "hidden data",
        "covert channel",
        "lsb steganography",
        "image steganography",
    ],
    "Malware Analysis": [
        "malware analysis",
        "reverse engineering",
        "static analysis",
        "dynamic analysis",
        "sandbox",
        "virus",
        "trojan",
        "ransomware",
    ],
    "Forensics": [
        "forensics",
        "digital forensics",
        "incident response",
        "dfir",
        "memory forensics",
        "disk forensics",
        "log analysis",
    ],
    "Cloud Security": [
        "cloud security",
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "s3 bucket",
        "cloud misconfiguration",
        "iac security",
    ],
    "Container Security": [
        "docker security",
        "kubernetes security",
        "container escape",
        "cve docker",
        "container hardening",
    ],
    "Mobile Security": [
        "mobile security",
        "android security",
        "ios security",
        "apk",
        "ipa",
        "mobile app security",
        "ios pentesting",
    ],
    "IoT Security": [
        "iot security",
        "embedded",
        "firmware",
        "router security",
        "smart device",
        "iot pentesting",
        "embedded security",
    ],
    "Blockchain": [
        "blockchain",
        "smart contract",
        "ethereum",
        "solidity",
        "web3",
        "defi",
        "cryptocurrency security",
    ],
    "Reverse Engineering": [
        "reverse engineering",
        "ida",
        "ghidra",
        "disassembly",
        "decompilation",
        "x64dbg",
        "radare2",
    ],
    "Blue Team": [
        "blue team",
        "defense",
        "siem",
        "soc",
        "detection",
        "monitoring",
        "incident response",
        "threat hunting",
    ],
    "Red Team": [
        "red team",
        "adversary",
        "attack simulation",
        "ttp",
        "mitre att&ck",
        "apt simulation",
        "penetration testing",
    ],
    "OSINT": [
        "osint",
        "open source intelligence",
        "shodan",
        "censys",
        "theharvester",
        "maltego",
        "osint framework",
    ],
    "Wireless Security": [
        "wireless",
        "wifi",
        "wpa2",
        "wep",
        "aircrack",
        "kismet",
        "evil twin",
        "rogue access point",
        "rf security",
    ],
    "Exploit Development": [
        "exploit development",
        "fuzzing",
        "buffer overflow",
        "rop",
        "shellcode",
        "exploit writing",
        "vulnerability research",
    ],
}

# Сопоставление тематических ключевых слов с конкретными курсами/лабами
TOPIC_TO_COURSE = {
    "SQL Injection": "web-basics",
    "XSS": "web-basics",
    "CSRF": "web-basics",
    "JWT": "web-advanced",
    "IDOR": "web-advanced",
    "NoSQL Injection": "web-advanced",
    "Сканирование": "network",
    "SMB": "network",
    "FTP/SSH": "network",
    "REST API": "api",
    "Authentication bypass": "api",
    "Privilege Escalation": "privesc",
}

# Ключевые слова для определения темы
TOPIC_KEYWORDS = {}
for topic, keywords in COURSE_TOPICS.items():
    for kw in keywords:
        TOPIC_KEYWORDS[kw.lower()] = topic


def get_pdf_files() -> list[Path]:
    """Получить все PDF файлы из knowledge_base"""
    pdfs = list(KB_DIR.glob("*.pdf"))
    # Исключаем служебные файлы
    pdfs = [
        p
        for p in pdfs
        if p.name not in ["news", "news_cache.json"] and not p.name.startswith(".")
    ]
    return pdfs


def extract_text_from_filename(filename: str) -> str:
    """Извлечь текстовые части из имени файла"""
    # Убираем расширение
    name = Path(filename).stem.lower()
    # Заменяем небуквы на пробелы
    name = re.sub(r"[^a-z0-9а-яё]", " ", name)
    return name


def determine_topics(text: str) -> set[str]:
    """Определить, к каким темам относится текст"""
    text_lower = text.lower()
    found = set()
    for keyword, topic in TOPIC_KEYWORDS.items():
        if keyword in text_lower:
            found.add(topic)
    return found


def analyze_coverage() -> tuple[dict[str, list[str]], dict[str, int]]:
    """Анализ покрытия тем"""
    pdfs = get_pdf_files()
    coverage: dict[str, list[str]] = {topic: [] for topic in COURSE_TOPICS}
    topic_counts: dict[str, int] = dict.fromkeys(COURSE_TOPICS.keys(), 0)

    for pdf in pdfs:
        text = extract_text_from_filename(pdf.name)
        topics = determine_topics(text)
        for topic in topics:
            coverage[topic].append(pdf.name)
            topic_counts[topic] += 1

    return coverage, topic_counts


def audit_file_sizes() -> tuple[list, list, list]:
    """Проверка размеров файлов (старая функциональность)"""
    pdfs = get_pdf_files()
    good = []
    issues = []
    small = []

    for pdf in pdfs:
        size = pdf.stat().st_size
        if size < 10000:  # Менее 10KB
            small.append((pdf.name, size))
        elif size < 50000:  # Менее 50KB
            issues.append((pdf.name, size, "Маленький файл"))
        else:
            good.append((pdf.name, size))

    return good, issues, small


def generate_report():
    """Сгенерировать полный отчёт по покрытию"""
    coverage, counts = analyze_coverage()
    good, issues, small = audit_file_sizes()

    print("=" * 80)
    print("[+] АУДИТ БАЗЫ ЗНАНИЙ CYBERTEACHER")
    print("=" * 80)
    print()

    total_topics = len(COURSE_TOPICS)
    covered_topics = sum(1 for c in coverage.values() if c)
    print("[+] Статистика:")
    print(f"   Всего тем: {total_topics}")
    print(f"   Покрыто тем: {covered_topics}")
    print(f"   Нет покрытия: {total_topics - covered_topics}")
    print(f"   Всего PDF: {len(get_pdf_files())}")
    print(f"   Хороших (>50KB): {len(good)}")
    print(f"   Маленьких (<50KB): {len(issues)}")
    print(f"   Криво маленьких (<10KB): {len(small)}")
    print()

    # Сводка по курсам
    print("[+] ПОКРЫТИЕ ПО КУРСАМ:")
    print("-" * 80)
    course_coverage = {}
    for topic, files in coverage.items():
        if topic in TOPIC_TO_COURSE:
            course_id = TOPIC_TO_COURSE[topic]
            course_coverage.setdefault(course_id, []).append((topic, len(files)))

    for course_id, topics in sorted(course_coverage.items()):
        print(f"\n[+] Курс: {course_id}")
        for topic, count in sorted(topics, key=lambda x: x[1], reverse=True):
            status = "[OK]" if count > 0 else "[MISS]"
            print(f"   {status} {topic}: {count} файл{'ов' if count != 1 else ''}")

    # Детали по покрытию
    print("\n" + "=" * 80)
    print("[+] Покрытые темы (рекомендации по которым ЕСТЬ материалы):")
    print("-" * 80)
    for topic in sorted(COURSE_TOPICS.keys()):
        files = coverage[topic]
        if files:
            print(f"\n[-] {topic} ({len(files)} файл{'ов' if len(files) > 1 else ''}):")
            for f in sorted(files)[:5]:
                print(f"   - {f}")
            if len(files) > 5:
                print(f"   ... и еще {len(files) - 5}")

    print("\n" + "=" * 80)
    print("[-] Темы БЕЗ покрытия (требует добавления книг):")
    print("-" * 80)
    missing = []
    for topic in sorted(COURSE_TOPICS.keys()):
        if not coverage[topic]:
            missing.append(topic)
            print(f"   - {topic}")

    print("\n" + "=" * 80)
    print("[+] КОНКРЕТНЫЕ РЕКОМЕНДАЦИИ ПО ДОБАВЛЕНИЮ:")
    print("-" * 80)

    recommendations = {
        "CSRF": [
            "OWASP CSRF Prevention Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)",
            "Web Application Security: A Beginner's Guide (часть про CSRF)",
            "The Web Application Hacker's Handbook (глава о CSRF)",
        ],
        "JWT": [
            "JSON Web Token (JWT) RFC 7519 (бесплатно)",
            "OWASP JWT Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet_for_Java.html)",
            "Hacker's Guide to JWT Attacks (online article, PortSwigger)",
        ],
        "NoSQL Injection": [
            "NoSQL Injection Attacks and Defense (бесплатные главы)",
            "MongoDB Security Best Practices (официальная документация)",
            "OWASP NoSQL Injection Prevention (cheatsheet)",
        ],
        "REST API": [
            "OWASP API Security Top 10 (https://owasp.org/www-project-api-security/)",
            "REST API Security: From Design to Deployment (бесплатные ресурсы)",
            "Hacking REST APIs (PortSwigger Academy, online)",
        ],
        "Authentication bypass": [
            "The Web Application Hacker's Handbook (глава об аутентификации)",
            "OWASP Authentication Cheat Sheet",
            "Common Authentication Flaws (PortSwigger, Web Security Academy)",
        ],
        "SMB exploitation": [
            "SMB (Server Message Block) Protocol Security (Microsoft Docs)",
            "Metasploit Guide: SMB attacks (официальный guide)",
            "Hacking Windows with SMB (Null Byte guide, WonderHowTo)",
        ],
        "FTP/SSH": [
            "FTP Security Best Practices (RFC, OWASP)",
            "SSH, The Secure Shell: The Definitive Guide (бесплатные главы)",
            "Brute Force Attacks: Techniques and Prevention (SANS)",
        ],
        "Cloud Security": [
            "AWS Security Best Practices (бесплатно от AWS, Security Pillar Well-Architected)",
            "Azure Security Documentation (Microsoft Docs)",
            "Cloud Security Alliance (CSA) Guidance (бесплатно)",
        ],
        "Container Security": [
            "Docker Security Cheatsheet (OWASP)",
            "Kubernetes Security (K8S) Official Docs (Kubernetes.io)",
            "Container Security: From Docker to Kubernetes (free resources)",
        ],
        "Mobile Security": [
            "OWASP Mobile Security Testing Guide (MSTG)",
            "Android Security Fundamentals (Google Developer Documentation)",
            "iOS Security Guide (Apple Platform Security)",
        ],
        "IoT Security": [
            "OWASP IoT Security Project (Top 10 IoT)",
            "IoT Security Foundation Guidelines",
            "Hacking IoT Devices: A Practical Guide (online tutorials)",
        ],
        "Blockchain": [
            "Smart Contract Security Best Practices (Consensys)",
            "Ethereum Smart Contract Security (documentation)",
            "Blockchain Security: A Practical Guide (free resources)",
        ],
        "Reverse Engineering": [
            "Reverse Engineering for Beginners (демо-версия, доступна частично)",
            "Practical Reverse Engineering (ogmentioned, части)",
            "Ghidra Official Documentation and Tutorials",
        ],
        "Blue Team": [
            "Blue Team Handbook (SOC)",
            "Incident Response and Computer Forensics (贯穿)",
            "Defensive Security Handbook (SANS)",
        ],
        "Red Team": [
            "Red Team Field Manual (RTFM)",
            "MITRE ATT&CK Framework Documentation (бесплатно)",
            "Adversary Emulation Guide (MITRE, lol)",
        ],
        "Steganography": [
            "Steganography Techniques and Applications (IEEE papers)",
            "Practical Steganography (online tutorials, CTF resources)",
            "CTF Steganography Guide (странная книга)",
        ],
        "Exploit Development": [
            "Shellcoder's Handbook (free chapters available)",
            "Exploit Development for Beginners (tutorial series online)",
            "Fuzzing: Brute Force Vulnerability Discovery (book excerpts)",
        ],
        "Privilege Escalation (Windows)": [
            "Windows Privilege Escalation Guide (SANS)",
            "Awesome Windows Privilege Escalation (GitHub repo)",
            "Privilege Escalation in Windows (online course)",
        ],
    }

    # Добавляем рекомендации для недостающих тем
    for topic in missing:
        if topic in recommendations:
            print(f"\n[+] {topic}:")
            for rec in recommendations[topic]:
                print(f"   -> {rec}")
        else:
            print(f"\n[+] {topic}:")
            print("   -> Общие учебники по теме: поискать на O'Reilly, Packt, SANS")

    print("\n" + "=" * 80)
    print("[+] ГДЕ ИСКАТЬ БЕСПЛАТНЫЕ КНИГИ:")
    print("-" * 80)
    print("""
1. O'Reilly — бесплатные книги по промо (раз в месяц, нужна подписка или trial)
2. Packt Publishing — ежедневная бесплатная книга (нужен аккаунт)
3. Springer Open Access — учебники по информатике (бесплатно)
4. SANS Reading Room — white papers по безопасности (бесплатно)
5. OWASP — все руководства бесплатно (cheatsheets, проект)
6. NIST — стандарты и Special Publications (бесплатно)
7. MITRE — ATT&CK, CAPEC, CWE (бесплатно)
8. GitHub — Many репозитории с учебными материалами, UNC1553
9. Null Byte (WonderHowTo) — статьи и гайды по хакинг
10. PortSwigger Web Security Academy — бесплатные лабы и гайды

👉 Рекомендуется: скачивать легально, проверять лицензии (Creative Commons, MIT, BSD).
    """)

    # Плохие файлы (маленькие)
    if small:
        print("\n" + "=" * 80)
        print("[-] СЛИШКОМ МАЛЕНЬКИЕ ФАЙЛЫ (<10KB):")
        print("-" * 80)
        for f, s in small:
            print(f"   • {f} ({s} bytes) — возможно, пустой или повреждённый")

    print("\n" + "=" * 80)
    print("[+] КОНЕЦ ОТЧЁТА")
    print("=" * 80)


if __name__ == "__main__":
    generate_report()
