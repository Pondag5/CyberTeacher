"""
🔐 Менеджер загрузки знаний (Updated)
"""
import os
import requests
from ui import console, print_panel

# Библиотека бесплатных ресурсов (Проверенные ссылки)
LIBRARY_CATALOG = {
    "1": {
        "name": "OWASP Top 10 (Overview)",
        "url": "https://raw.githubusercontent.com/OWASP/Top10/master/README.md",
        "filename": "owasp_top10.md",
        "desc": "Обзор топ-10 уязвимостей (Англ)."
    },
    "2": {
        "name": "SQL Injection Payloads",
        "url": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/README.md",
        "filename": "payloads_sqli.md",
        "desc": "Огромный список пэйлоадов для SQL Injection."
    },
    "3": {
        "name": "XSS Payloads",
        "url": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/README.md",
        "filename": "payloads_xss.md",
        "desc": "Пэйлоады для XSS атак."
    },
    "4": {
        "name": "Reverse Shell Cheatsheet",
        "url": "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md",
        "filename": "reverse_shells.md",
        "desc": "Шпаргалка по Reverse Shells."
    },
    "5": {
        "name": "Penetration Testing Guide",
        "url": "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Penetration_Testing_Cheat_Sheet.md",
        "filename": "pentest_guide.md",
        "desc": "Гайд по пентестингу от OWASP."
    }
}

def download_resource(url: str, save_path: str):
    """Скачивает файл по URL"""
    try:
        # Добавляем заголовок User-Agent, чтобы GitHub не блокировал
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=15, headers=headers)
        response.raise_for_status()
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        return True, len(response.text)
    except Exception as e:
        return False, str(e)

def show_library_menu():
    """Показывает меню библиотеки"""
    text = ""
    for key, item in LIBRARY_CATALOG.items():
        text += f"[{key}] {item['name']}\n    [dim]{item['desc']}[/dim]\n"
    
    print_panel(text, title="📚 Библиотека Знаний", border_style="cyan")

def update_knowledge_base():
    """Принудительное обновление базы знаний"""
    from knowledge import load_knowledge_base
    console.print("[cyan]🔄 Обновление базы знаний...[/cyan]")
    load_knowledge_base()
    console.print("[green]✅ База знаний обновлена![/green]")
