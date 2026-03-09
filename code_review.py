"""
🔐 Анализ кода на уязвимости (Bandit + AI + Fix Generation)
"""

import json
import re
import tempfile
import subprocess

from config import LLM
from ui import console

def run_bandit_scan(code: str):
    """Запуск Bandit для статического анализа"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        result = subprocess.run(
            ['bandit', '-f', 'json', '-r', temp_path],
            capture_output=True, text=True
        )
        
        if result.stdout:
            return json.loads(result.stdout)
    except FileNotFoundError:
        console.print("[yellow]⚠️ Bandit не установлен. Пропускаю статический анализ.[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка Bandit: {e}[/red]")
    return None

def code_review_function(code: str, language: str = "python"):
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
        response = LLM.invoke(prompt)
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")

    return None
