"""
🔐 Code Review v3 — Продвинутый анализатор кода с OWASP Top 10

Поддерживает:
- Отдельные файлы, директории, git-репозитории
- Semgrep с кастомными OWASP-правилами (SQLi, XSS, cmd injection, SSRF, etc.)
- Bandit (Python), ESLint (JS) как дополнительные инструменты
- OWASP Top 10 mapping для всех находок
- CI/CD mode с exit codes по severity
- SARIF output для IDE интеграции
- LLM-ревью с генерацией отчёта
"""

import contextlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Путь к кастомным semgrep правилам
RULES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "semgrep_rules")

# Поддерживаемые языки и расширения
LANGUAGE_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".php": "php",
    ".java": "java",
    ".sh": "bash",
    ".bash": "bash",
    ".go": "go",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".rb": "ruby",
    ".rs": "rust",
    ".sql": "sql",
    ".html": "html",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".env": "env",
}

# OWASP Top 10 2021 mapping
OWASP_CATEGORIES = {
    "A01": {"name": "Broken Access Control", "items": ["Path Traversal", "Open Redirect", "IDOR", "CORS Misconfiguration"]},
    "A02": {"name": "Cryptographic Failures", "items": ["Weak Crypto", "Hardcoded Secrets", "Insecure Random"]},
    "A03": {"name": "Injection", "items": ["SQL Injection", "XSS", "Command Injection", "LDAP Injection", "XXE"]},
    "A04": {"name": "Insecure Design", "items": ["Missing Rate Limit", "Weak Password Policy"]},
    "A05": {"name": "Security Misconfiguration", "items": ["Debug Enabled", "Default Credentials", "Verbose Errors"]},
    "A06": {"name": "Vulnerable and Outdated Components", "items": ["Known CVE", "Outdated Dependency"]},
    "A07": {"name": "Identification and Authentication Failures", "items": ["Hardcoded Credentials", "Weak Session", "Brute Force"]},
    "A08": {"name": "Software and Data Integrity Failures", "items": ["Insecure Deserialization", "CI/CD Tampering"]},
    "A09": {"name": "Security Logging and Monitoring Failures", "items": ["Missing Logging", "Insufficient Monitoring"]},
    "A10": {"name": "Server-Side Request Forgery", "items": ["SSRF", "URL Redirect"]},
}

# Паттерны для поиска секретов
SECRET_PATTERNS = [
    ("AWS Access Key", r"AKIA[0-9A-Z]{16}", "A07"),
    ("AWS Secret Key", r"(?i)aws_secret_access_key\s*[:=]\s*[\"']?[A-Za-z0-9/+=]{40}", "A07"),
    ("GitHub Token", r"ghp_[0-9a-zA-Z]{36}", "A07"),
    ("Slack Token", r"xox[baprs]-[0-9a-zA-Z-]+", "A07"),
    ("OpenAI Key", r"sk-[a-zA-Z0-9]{48}", "A07"),
    ("Generic API Key", r"(?i)(api_key|apikey|api-key)\s*[:=]\s*[\"']?[^\s\"'`]{16,}", "A07"),
    ("Generic Password", r"(?i)(password|passwd|pwd|secret|token)\s*[:=]\s*[\"']?[^\s\"'`]{8,}", "A07"),
    ("Private Key", r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "A02"),
    ("JWT Secret", r"(?i)jwt_secret\s*[:=]\s*[\"']?[^\s\"'`]{16,}", "A02"),
    ("Database URL", r"(?i)(database_url|db_url|connection_string)\s*[:=]\s*[\"']?(postgres|mysql|mongodb)://[^\s\"'`]+", "A07"),
]


def detect_language(file_path: str) -> str | None:
    """Определить язык программирования по расширению файла."""
    ext = os.path.splitext(file_path)[1].lower()
    return LANGUAGE_EXTENSIONS.get(ext)


def find_source_files(directory: str, max_files: int = 50) -> list[str]:
    """Найти все файлы с исходным кодом в директории."""
    source_files = []
    extensions = set(LANGUAGE_EXTENSIONS.keys())

    for root, _, files in os.walk(directory):
        if any(part.startswith(".") or part in ("node_modules", "vendor", ".git") for part in root.split(os.sep)):
            continue

        for fname in files:
            if os.path.splitext(fname)[1].lower() in extensions:
                fpath = os.path.join(root, fname)
                source_files.append(fpath)
                if len(source_files) >= max_files:
                    return source_files

    return source_files


def scan_file_secrets(file_path: str) -> list[dict[str, Any]]:
    """Просканировать файл на наличие секретов."""
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, start=1):
            for name, pattern, owasp_id in SECRET_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append({
                        "file": file_path,
                        "line": i,
                        "type": name,
                        "severity": "critical",
                        "snippet": line.strip()[:100],
                        "owasp": owasp_id,
                        "tool": "secrets-scan",
                    })
    except Exception:
        pass

    return findings


def run_bandit(file_path: str) -> list[dict[str, Any]]:
    """Запуск Bandit для Python файлов."""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-r", file_path],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        if result.stdout:
            data = json.loads(result.stdout)
            findings = []
            for res in data.get("results", []):
                findings.append({
                    "file": res.get("filename", file_path),
                    "line": res.get("line_number", 0),
                    "type": res.get("test_name", "Unknown"),
                    "severity": res.get("issue_severity", "medium"),
                    "description": res.get("issue_text", ""),
                    "tool": "bandit",
                })
            return findings
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return []


def run_semgrep(file_path: str, custom_rules: bool = True) -> list[dict[str, Any]]:
    """Запуск semgrep с кастомными OWASP-правилами."""
    findings = []

    # 1. Кастомные правила (приоритет)
    if custom_rules and os.path.isdir(RULES_DIR):
        try:
            result = subprocess.run(
                ["semgrep", "--json", "--config", RULES_DIR, file_path],
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for res in data.get("results", []):
                    extra = res.get("extra", {})
                    metadata = extra.get("metadata", {})
                    owasp = metadata.get("owasp", "Unknown")
                    findings.append({
                        "file": res.get("path", file_path),
                        "line": res.get("start", {}).get("line", 0),
                        "type": res.get("rule_id", "Unknown"),
                        "severity": _map_semgrep_severity(extra.get("severity", "medium")),
                        "description": extra.get("message", ""),
                        "owasp": owasp,
                        "tool": "semgrep-custom",
                        "cwe": metadata.get("cwe", ""),
                    })
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

    # 2. Fallback на auto-правила если кастомные не нашли ничего
    if not findings:
        try:
            result = subprocess.run(
                ["semgrep", "--json", "--config", "auto", file_path],
                capture_output=True,
                text=True,
                check=False,
                timeout=60,
            )
            if result.stdout:
                data = json.loads(result.stdout)
                for res in data.get("results", []):
                    extra = res.get("extra", {})
                    metadata = extra.get("metadata", {})
                    findings.append({
                        "file": res.get("path", file_path),
                        "line": res.get("start", {}).get("line", 0),
                        "type": res.get("rule_id", "Unknown"),
                        "severity": _map_semgrep_severity(extra.get("severity", "medium")),
                        "description": extra.get("message", ""),
                        "owasp": metadata.get("owasp", _guess_owasp(extra.get("message", ""))),
                        "tool": "semgrep-auto",
                        "cwe": metadata.get("cwe", ""),
                    })
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

    return findings


def _map_semgrep_severity(severity: str) -> str:
    """Маппинг semgrep severity на внутреннюю шкалу."""
    mapping = {
        "ERROR": "critical",
        "WARNING": "high",
        "INFO": "medium",
    }
    return mapping.get(severity.upper(), severity.lower())


def _guess_owasp(message: str) -> str:
    """Предположить OWASP категорию по сообщению."""
    msg_lower = message.lower()
    if any(kw in msg_lower for kw in ["sql", "query", "injection"]):
        return "A03:2021 – Injection"
    if any(kw in msg_lower for kw in ["xss", "cross-site", "script"]):
        return "A03:2021 – Injection"
    if any(kw in msg_lower for kw in ["password", "secret", "credential", "hardcod"]):
        return "A07:2021 – Identification and Authentication Failures"
    if any(kw in msg_lower for kw in ["crypto", "hash", "md5", "sha1", "encrypt"]):
        return "A02:2021 – Cryptographic Failures"
    if any(kw in msg_lower for kw in ["path", "traversal", "file"]):
        return "A01:2021 – Broken Access Control"
    if any(kw in msg_lower for kw in ["deserial", "pickle", "yaml.load"]):
        return "A08:2021 – Software and Data Integrity Failures"
    if any(kw in msg_lower for kw in ["ssrf", "request forgery", "url"]):
        return "A10:2021 – Server-Side Request Forgery"
    return "A05:2021 – Security Misconfiguration"


def scan_file(file_path: str, use_semgrep: bool = True) -> dict[str, Any]:
    """Полный анализ одного файла."""
    language = detect_language(file_path)
    findings = []

    # 1. Сканирование на секреты (все языки)
    findings.extend(scan_file_secrets(file_path))

    # 2. Semgrep — primary tool для всех языков
    if use_semgrep:
        findings.extend(run_semgrep(file_path))

    # 3. Bandit как дополнительный инструмент для Python
    if language == "python":
        findings.extend(run_bandit(file_path))

    return {
        "file": file_path,
        "language": language or "unknown",
        "findings": findings,
        "severity_counts": _count_severities(findings),
        "owasp_summary": _count_owasp(findings),
    }


def scan_directory(directory: str, max_files: int = 50, use_semgrep: bool = True) -> dict[str, Any]:
    """Рекурсивный анализ директории."""
    source_files = find_source_files(directory, max_files)
    results = []
    total_findings = []

    for fpath in source_files:
        result = scan_file(fpath, use_semgrep)
        results.append(result)
        total_findings.extend(result["findings"])

    return {
        "directory": directory,
        "files_scanned": len(source_files),
        "results": results,
        "total_findings": len(total_findings),
        "findings": total_findings,
        "severity_counts": _count_severities(total_findings),
        "owasp_summary": _count_owasp(total_findings),
    }


def clone_repo(url: str, branch: str = "main") -> str | None:
    """Клонировать репозиторий во временную директорию."""
    if not shutil.which("git"):
        return None

    tmpdir = tempfile.mkdtemp(prefix="cyberteacher_review_")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", "-b", branch, url, tmpdir],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return tmpdir
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        with contextlib.suppress(Exception):
            shutil.rmtree(tmpdir)
        return None


def _count_severities(findings: list[dict]) -> dict[str, int]:
    """Подсчитать находки по уровням критичности."""
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.get("severity", "medium").lower()
        if sev in counts:
            counts[sev] += 1
    return counts


def _count_owasp(findings: list[dict]) -> dict[str, int]:
    """Подсчитать находки по OWASP категориям."""
    counts: dict[str, int] = {}
    for f in findings:
        owasp = f.get("owasp", "Unknown")
        # Извлекаем ID (A01, A02, etc.)
        match = re.match(r"(A\d{2})", owasp)
        if match:
            key = match.group(1)
        else:
            key = "Unknown"
        counts[key] = counts.get(key, 0) + 1
    return counts


def generate_sarif(results: dict[str, Any], version: str = "2.1.0") -> dict[str, Any]:
    """Генерация SARIF отчёта для IDE интеграции."""
    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": version,
        "runs": [{
            "tool": {
                "driver": {
                    "name": "CyberTeacher Code Review",
                    "version": "3.0",
                    "informationUri": "https://github.com/cyberteacher",
                    "rules": _build_sarif_rules(results),
                }
            },
            "results": _build_sarif_results(results),
        }]
    }
    return sarif


def _build_sarif_rules(results: dict[str, Any]) -> list[dict]:
    """Построить список правил для SARIF."""
    rules = {}
    for f in results.get("findings", []):
        rule_id = f.get("type", "unknown")
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "name": f.get("type", "Unknown"),
                "shortDescription": {"text": f.get("description", "")[:100]},
                "defaultConfiguration": {"level": _severity_to_sarif_level(f.get("severity", "medium"))},
                "properties": {
                    "owasp": f.get("owasp", ""),
                    "cwe": f.get("cwe", ""),
                    "tags": ["security", "vulnerability"],
                }
            }
    return list(rules.values())


def _build_sarif_results(results: dict[str, Any]) -> list[dict]:
    """Построить список результатов для SARIF."""
    sarif_results = []
    for f in results.get("findings", []):
        sarif_results.append({
            "ruleId": f.get("type", "unknown"),
            "level": _severity_to_sarif_level(f.get("severity", "medium")),
            "message": {"text": f.get("description", f.get("snippet", ""))},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": f.get("file", "")},
                    "region": {
                        "startLine": f.get("line", 1),
                    }
                }
            }],
            "properties": {
                "owasp": f.get("owasp", ""),
                "cwe": f.get("cwe", ""),
                "tool": f.get("tool", ""),
            }
        })
    return sarif_results


def _severity_to_sarif_level(severity: str) -> str:
    """Маппинг severity на SARIF level."""
    mapping = {"critical": "error", "high": "error", "medium": "warning", "low": "note"}
    return mapping.get(severity.lower(), "warning")


def calculate_ci_exit_code(results: dict[str, Any], fail_on: str = "high") -> int:
    """Рассчитать exit code для CI/CD mode.
    
    fail_on: "critical" | "high" | "medium" | "low"
    Возвращает 0 если нет находок >= fail_on, иначе 1.
    """
    sev_counts = results.get("severity_counts", {})
    threshold_order = ["critical", "high", "medium", "low"]
    fail_index = threshold_order.index(fail_on) if fail_on in threshold_order else 1

    for i in range(fail_index + 1):
        if sev_counts.get(threshold_order[i], 0) > 0:
            return 1
    return 0


def generate_llm_report(code: str, language: str, findings: list[dict]) -> dict[str, Any] | None:
    """Сгенерировать LLM-отчёт с рекомендациями."""
    from config import LazyLoader
    from state import get_state

    if get_state().offline_mode:
        return None

    llm = LazyLoader.get_llm()
    if llm is None:
        return None

    findings_text = ""
    if findings:
        findings_text = "\nСтатический анализ нашёл:\n"
        for f in findings[:20]:
            findings_text += f"- [{f.get('severity', 'medium').upper()}]"
            if f.get("owasp"):
                findings_text += f" OWASP:{f['owasp']}"
            findings_text += f" {f.get('type', 'Unknown')}"
            if f.get("line"):
                findings_text += f" (line {f['line']})"
            findings_text += "\n"

    prompt = f"""Ты — эксперт по кибербезопасности и code review. Проанализируй код и найди уязвимости.

Язык: {language}

Код:
```{language}
{code[:8000]}
```

{findings_text}

Верни JSON в формате:
{{
    "overall_score": "A|B|C|D|F",
    "vulnerability_count": число,
    "critical_issues": ["критичная проблема 1", ...],
    "recommendations": ["рекомендация 1", ...],
    "summary": "Общее заключение (2-3 предложения)",
    "secure_code_example": "Пример безопасной версии (если применимо)"
}}

Верни ТОЛЬКО JSON."""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        json_match = re.search(r"\{[\s\S]*\}", content)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass

    return None


def display_scan_results(results: dict[str, Any], llm_report: dict | None = None, ci_mode: bool = False):
    """Отобразить результаты сканирования в CLI."""
    # Заголовок
    console.print(Panel(
        f"📁 Файлов: {results.get('files_scanned', 1)} | "
        f"Находок: {results.get('total_findings', len(results.get('findings', [])))}",
        title="🔐 CODE REVIEW v3",
        border_style="cyan",
    ))

    # OWASP Summary
    owasp_summary = results.get("owasp_summary", {})
    if owasp_summary:
        owasp_text = ""
        for owasp_id, count in sorted(owasp_summary.items()):
            category = OWASP_CATEGORIES.get(owasp_id, {})
            name = category.get("name", owasp_id)
            owasp_text += f"  {owasp_id} ({name}): {count}\n"
        if owasp_text:
            console.print(Panel(owasp_text.strip(), title="📋 OWASP Top 10", border_style="yellow"))

    # Таблица находок
    findings = results.get("findings", [])
    if findings:
        table = Table(title="Найденные проблемы")
        table.add_column("Severity", style="bold")
        table.add_column("OWASP", style="magenta")
        table.add_column("File", style="cyan")
        table.add_column("Line", justify="right")
        table.add_column("Type")
        table.add_column("Description")

        for f in findings[:30]:
            sev = f.get("severity", "medium").lower()
            sev_style = {"critical": "red", "high": "yellow", "medium": "blue", "low": "green"}.get(sev, "white")
            owasp = f.get("owasp", "")
            owasp_id = owasp[:3] if owasp else ""
            table.add_row(
                f"[{sev_style}]{sev.upper()}[/{sev_style}]",
                owasp_id,
                os.path.basename(f.get("file", "")),
                str(f.get("line", "")),
                f.get("type", ""),
                f.get("description", f.get("snippet", ""))[:60],
            )

        console.print(table)

        if len(findings) > 30:
            console.print(f"[dim]...и ещё {len(findings) - 30} находок[/dim]")

    # LLM отчёт
    if llm_report:
        console.print(Panel(
            f"[bold]Оценка:[/bold] {llm_report.get('overall_score', 'N/A')}\n\n"
            f"[bold]Summary:[/bold] {llm_report.get('summary', '')}\n\n"
            f"[bold]Critical Issues:[/bold]\n" +
            "\n".join(f"• {i}" for i in llm_report.get("critical_issues", [])) +
            "\n\n[bold]Recommendations:[/bold]\n" +
            "\n".join(f"• {r}" for r in llm_report.get("recommendations", [])),
            title="🤖 LLM Analysis",
            border_style="yellow",
        ))

    # Сводка
    sev_counts = results.get("severity_counts", {})
    if sev_counts.get("critical", 0) > 0:
        console.print(f"[red]🔴 CRITICAL: {sev_counts['critical']}[/red]")
    if sev_counts.get("high", 0) > 0:
        console.print(f"[yellow]🟡 HIGH: {sev_counts['high']}[/yellow]")
    if sev_counts.get("medium", 0) > 0:
        console.print(f"[blue]🔵 MEDIUM: {sev_counts['medium']}[/blue]")
    if sev_counts.get("low", 0) > 0:
        console.print(f"[green]🟢 LOW: {sev_counts['low']}[/green]")

    # CI mode summary
    if ci_mode:
        exit_code = calculate_ci_exit_code(results, fail_on="high")
        status = "❌ FAIL" if exit_code else "✅ PASS"
        console.print(Panel(f"CI/CD Result: {status} (exit code: {exit_code})", border_style="red" if exit_code else "green"))


def handle_code_review_v2(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """
    Обработка /scanv2 <path|url> [branch] [--ci] [--sarif] [--no-semgrep]

    Поддерживает:
    - /scanv2 file.py — анализ одного файла
    - /scanv2 ./src — анализ директории
    - /scanv2 https://github.com/user/repo.git [branch] — анализ git-репозитория
    - /scanv2 <target> --ci — CI/CD mode с exit code
    - /scanv2 <target> --sarif — вывод в SARIF формате
    - /scanv2 <target> --no-semgrep — без semgrep (только secrets + bandit)
    """
    parts = action.split()
    if len(parts) < 2:
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /scanv2 <file>          — анализ файла")
        console.print("  /scanv2 <directory>     — анализ директории")
        console.print("  /scanv2 <git_url> [branch] — анализ git-репозитория")
        console.print("  /scanv2 <target> --ci   — CI/CD mode")
        console.print("  /scanv2 <target> --sarif — SARIF output")
        console.print("  /scanv2 <target> --no-semgrep — без semgrep")
        console.print("[dim]Примеры:[/dim]")
        console.print("  /scanv2 main.py")
        console.print("  /scanv2 ./src")
        console.print("  /scanv2 https://github.com/user/repo.git main")
        console.print("  /scanv2 ./src --ci")
        console.print("  /scanv2 ./src --sarif --output results.sarif")
        return True, None, None, True

    # Парсинг флагов
    target = None
    branch = "main"
    ci_mode = False
    sarif_output = False
    use_semgrep = True
    output_file = None

    i = 1
    while i < len(parts):
        part = parts[i]
        if part == "--ci":
            ci_mode = True
        elif part == "--sarif":
            sarif_output = True
        elif part == "--no-semgrep":
            use_semgrep = False
        elif part == "--output" and i + 1 < len(parts):
            output_file = parts[i + 1]
            i += 1
        elif target is None:
            target = part
        elif target.startswith(("http://", "https://", "git@")):
            branch = part
        i += 1

    if target is None:
        console.print("[red]Укажите цель для сканирования.[/red]")
        return True, None, None, True

    tmpdir = None

    try:
        # Определяем тип цели
        if target.startswith(("http://", "https://", "git@")):
            console.print(f"[bold]Клонирую {target} (branch: {branch})...[/bold]")
            tmpdir = clone_repo(target, branch)
            if tmpdir is None:
                console.print("[red]Не удалось клонировать репозиторий.[/red]")
                return True, None, None, True
            console.print("[bold]Сканирую репозиторий...[/bold]")
            results = scan_directory(tmpdir, use_semgrep=use_semgrep)

        elif os.path.isfile(target):
            console.print(f"[bold]Сканирую файл: {target}[/bold]")
            file_result = scan_file(target, use_semgrep=use_semgrep)
            results = {
                "directory": os.path.dirname(target),
                "files_scanned": 1,
                "results": [file_result],
                "total_findings": len(file_result.get("findings", [])),
                "findings": file_result.get("findings", []),
                "severity_counts": file_result.get("severity_counts", {}),
                "owasp_summary": file_result.get("owasp_summary", {}),
            }

        elif os.path.isdir(target):
            console.print(f"[bold]Сканирую директорию: {target}[/bold]")
            results = scan_directory(target, use_semgrep=use_semgrep)

        else:
            console.print(f"[red]Файл или директория не найдены: {target}[/red]")
            return True, None, None, True

        # SARIF output
        if sarif_output:
            sarif = generate_sarif(results)
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(sarif, f, indent=2, ensure_ascii=False)
                console.print(f"[green]SARIF отчёт сохранён: {output_file}[/green]")
            else:
                console.print(json.dumps(sarif, indent=2, ensure_ascii=False))
            return True, None, None, True

        # LLM-анализ первого файла с находками
        llm_report = None
        if not ci_mode:
            for r in results.get("results", []):
                if r.get("findings"):
                    try:
                        with open(r["file"], "r", encoding="utf-8", errors="ignore") as f:
                            code = f.read()
                        llm_report = generate_llm_report(code, r.get("language", "unknown"), r.get("findings", []))
                    except Exception:
                        pass
                    break

        # Отображение
        display_scan_results(results, llm_report, ci_mode)

        # CI mode exit
        if ci_mode:
            exit_code = calculate_ci_exit_code(results, fail_on="high")
            return True, None, exit_code, True

        return True, None, None, True

    finally:
        if tmpdir:
            with contextlib.suppress(Exception):
                shutil.rmtree(tmpdir)
