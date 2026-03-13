# handlers/threats.py
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console

console = Console()

def handle_threats(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Показать досье на APT-группу"""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) > 1:
            group_name = parts[1].strip().lower()
            threat_file = os.path.join("threats", f"{group_name}.json")

            if not os.path.exists(threat_file):
                console.print(f"[yellow]Досье '{group_name}' не найдено[/yellow]")
                # Список доступных
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')] if os.path.exists("threats") else []
                if files:
                    console.print("[cyan]Доступные: " + ", ".join(sorted(files)) + "[/cyan]")
                return True, None, None, True

            with open(threat_file, 'r', encoding='utf-8') as f:
                threat = json.load(f)

            console.print(f"\n[bold red]📁 Досье: {threat.get('name', 'Unknown')}[/bold red]")
            console.print(f"Алиасы: {', '.join(threat.get('aliases', []))}")
            console.print(f"Страна: {threat.get('country', 'N/A')}")
            console.print(f"Активность: {threat.get('first_seen', 'N/A')}")
            console.print(f"Цели: {', '.join(threat.get('targets', []))}")
            console.print(f"\n[bold]Тактики MITRE:[/bold]")
            for t in threat.get('tactics', []):
                console.print(f"  • {t}")
            console.print(f"\n[bold]Инструменты:[/bold]")
            for tool in threat.get('tools', []):
                console.print(f"  • {tool}")
            console.print(f"\n[bold]Техники:[/bold]")
            for tech in threat.get('techniques', []):
                console.print(f"  • {tech}")
            console.print(f"\n[bold]Недавняя активность:[/bold] {threat.get('recent_activity', 'N/A')}")
            if threat.get('references'):
                console.print(f"[bold]Ссылки:[/bold] {threat['references'][0]}")
            console.print()
            return True, None, None, True
        else:
            console.print("[cyan]Использование: /threats <имя_группы>[/cyan]")
            if os.path.exists("threats"):
                files = [f[:-5] for f in os.listdir("threats") if f.endswith('.json')]
                console.print("[bold]Доступные группы:[/bold]")
                for f in sorted(files):
                    console.print(f"  • {f}")
            return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_groups(*args, **kwargs) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Группировка APT-групп по странам/тактикам"""
    try:
        if not os.path.exists("threats"):
            console.print("[yellow]Папка threats/ не найдена[/yellow]")
            return True, None, None, True

        # Загружаем все досье
        threats = []
        for f in os.listdir("threats"):
            if f.endswith('.json'):
                with open(os.path.join("threats", f), 'r', encoding='utf-8') as fp:
                    threats.append(json.load(fp))

        if not threats:
            console.print("[yellow]Нет данных об угрозах[/yellow]")
            return True, None, None, True

        console.print("[bold cyan]🌍 APT-группы по странам[/bold cyan]\n")

        # Группируем по стране
        by_country = {}
        for t in threats:
            country = t.get('country', 'Unknown')
            by_country.setdefault(country, []).append(t.get('name', 'Unknown'))

        for country in sorted(by_country.keys()):
            console.print(f"[bold]{country}[/bold]:")
            for name in sorted(by_country[country]):
                console.print(f"  • {name}")
            console.print()

        console.print("[bold]📊 Статистика:[/bold]")
        console.print(f"Всего групп: {len(threats)}")
        console.print(f"Стран: {len(by_country)}")

        # Популярные тактики
        tactic_counts = {}
        for t in threats:
            for tactic in t.get('tactics', []):
                tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1

        if tactic_counts:
            console.print("\n[bold]TOP-5 тактик:[/bold]")
            sorted_tactics = sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for tactic, count in sorted_tactics:
                console.print(f"  • {tactic}: {count} групп")

        console.print()

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_threat_summary(*args, **kwargs) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Краткая сводка по всем угрозам"""
    try:
        if not os.path.exists("threats"):
            console.print("[yellow]Папка threats/ не найдена[/yellow]")
            return True, None, None, True

        # Загружаем все досье
        threats = []
        for f in os.listdir("threats"):
            if f.endswith('.json'):
                with open(os.path.join("threats", f), 'r', encoding='utf-8') as fp:
                    threats.append(json.load(fp))

        if not threats:
            console.print("[yellow]Нет данных об угрозах[/yellow]")
            return True, None, None, True

        console.print("[bold red]📊 Сводка по threat intelligence[/bold red]\n")

        # Статистика по странам
        by_country = {}
        for t in threats:
            country = t.get('country', 'Unknown')
            by_country[country] = by_country.get(country, 0) + 1

        console.print("[bold]🌍 Распределение по странам:[/bold]")
        for country in sorted(by_country.keys()):
            console.print(f"  {country}: {by_country[country]} групп")

        console.print()

        # Top тактики
        tactic_counts = {}
        for t in threats:
            for tactic in t.get('tactics', []):
                tactic_counts[tactic] = tactic_counts.get(tactic, 0) + 1

        console.print("[bold]🎯 Top-10 тактик MITRE ATT&CK:[/bold]")
        for tactic, count in sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {tactic}: {count}")

        console.print()

        # Инструменты
        tool_counts = {}
        for t in threats:
            for tool in t.get('tools', []):
                tool_counts[tool] = tool_counts.get(tool, 0) + 1

        console.print("[bold]🔧 Top-10 инструментов:[/bold]")
        for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {tool}: {count}")

        console.print()

        # Целевые сектора
        target_counts = {}
        for t in threats:
            for target in t.get('targets', []):
                target_counts[target] = target_counts.get(target, 0) + 1

        console.print("[bold]🎯 Целевые сектора:[/bold]")
        for target, count in sorted(target_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            console.print(f"  • {target}: {count}")

        console.print()

        # Исследование
        console.print(f"[bold]📈 Всего досье: {len(threats)}[/bold]")
        console.print(f"[bold]🆕 Первые заметки:[/bold]")
        for t in threats:
            first = t.get('first_seen', 'N/A')
            name = t.get('name', 'Unknown')
            console.print(f"  {name}: {first}")

        console.print("\n[cyan]Используйте '/threats <name>' для подробностей[/cyan]")
        console.print()

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True
