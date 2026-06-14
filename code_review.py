"""
🔐 Анализ кода на уязвимости (Bandit + AI + Fix Generation)
"""

import json
import re
import subprocess
import tempfile

from ui import console


def run_bandit_scan(code: str):
    """Запуск Bandit для статического анализа"""
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            temp_path = f.name

        result = subprocess.run(
            ["bandit", "-f", "json", "-r", temp_path],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.stdout:
            return json.loads(result.stdout)
    except FileNotFoundError:
        console.print(
            "[yellow]⚠️ Bandit не установлен. Пропускаю статический анализ.[/yellow]"
        )
    except Exception as e:
        console.print(f"[red]Ошибка Bandit: {e}[/red]")
    return None


def code_review_function(code: str, language: str = "python") -> dict[str, Any] | None:
    """Анализ кода: Bandit + LLM + Исправления"""

    scan_results = ""

    if language == "python":
        bandit_report = run_bandit_scan(code)
        if bandit_report and bandit_report.get("results"):
            scan_results = "\n⚠️ Найдены проблемы (Bandit):\n"
            for res in bandit_report["results"]:
                scan_results += f"- [Line {res['line_number']}] {res['issue_text']} (Severity: {res['issue_severity']})\n"

    json_template = """
{
    "vulnerabilities": [
        {
            "line": 5,
            "type": "Тип уязвимости",
            "severity": "high|medium|low",
            "description": "Описание",
            "fix": "Как исправить"
        }
    ],
    "overall_score": "A|B|C|D|F",
    "summary": "Общее заключение",
    "fixed_code": "Исправленный вариант кода здесь (строка)"
}
"""

    # Добавили требование fixed_code
    prompt = (
        f"Проанализируй код на уязвимости.\n\n"
        f"Язык: {language}\n\n"
        f"Код:\n```\n{code}\n```\n\n"
        f"{scan_results}\n\n"
        f"Задача:\n"
        f"1. Объясни найденные уязвимости.\n"
        f"2. Предложи исправления.\n"
        f"3. Напиши ИСПРАВЛЕННУЮ ВЕРСИЮ КОДА.\n\n"
        f"Верни JSON в формате:\n{json_template}\n\n"
        f"Верни только JSON."
    )

    try:
        from config import LazyLoader as _LL

        llm = _LL.get_llm()
        if llm is None:
            return None
        response = llm.invoke(prompt)
        json_match = re.search(r"\{[\s\S]*\}", response)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")

    return None


def generate_secure_code(code: str, language: str = "python") -> str | None:
    """Сгенерировать безопасную версию кода (L-09)."""
    from config import LazyLoader

    llm = LazyLoader.get_llm()
    if llm is None:
        return None

    lang_desc = {
        "python": "Python (используй prepared statements, input validation, secure defaults)",
        "javascript": "JavaScript/Node.js (используй parameterized queries, escape output, helmet)",
        "php": "PHP (используй PDO prepared statements, htmlspecialchars, password_hash)",
        "java": "Java (используй PreparedStatement, OWASP ESAPI, input validation)",
        "bash": "Bash (используй quoting, set -euo pipefail, validation)",
    }.get(language, language)

    prompt = f"""Ты — эксперт по кибербезопасности. Перепиши следующий код, устранив ВСЕ уязвимости.

Язык: {lang_desc}

Исходный код:
```{language}
{code}
```

Требования к безопасной версии:
1. Устрани все уязвимости (SQLi, XSS, command injection, path traversal, etc.)
2. Добавь валидацию входных данных
3. Используй безопасные функции и библиотеки
4. Добавь комментарии, объясняющие изменения
5. Сохрани функциональность исходного кода

Верни ТОЛЬКО исправленный код в markdown блоке, без пояснений."""

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        return content
    except Exception as e:
        console.print(f"[red]Ошибка генерации безопасного кода: {e}[/red]")
        return None
