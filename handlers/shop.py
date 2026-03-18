# -*- coding: utf-8 -*-
"""Магазин достижений и улучшений (C-14)"""

from typing import Any, Dict, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from state import get_state
import json
import os

console = Console()

SHOP_ITEMS_FILE = "data/shop_items.json"


def load_shop_items() -> list[dict]:
    if not os.path.exists(SHOP_ITEMS_FILE):
        return []
    try:
        with open(SHOP_ITEMS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("items", [])
    except Exception:
        return []


def handle_shop(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Обработка команды /shop [item_id]

    Без аргументов — показать список товаров.
    С item_id — попытаться купить.
    """
    state = get_state()
    parts = action.split(maxsplit=1)
    item_id = parts[1].strip() if len(parts) > 1 else None

    if item_id is None:
        # Показать витрину
        items = load_shop_items()
        if not items:
            console.print("[yellow]Магазин временно недоступен[/yellow]")
            return True, None, None, True

        console.print("[bold cyan]🏪 Магазин[/bold cyan]\n")
        for item in items:
            console.print(
                f"[bold]{item['name']}[/bold] (ID: {item['id']}) — {item['cost']} XP\n"
                f"  {item['description']}\n"
            )
        console.print(f"[italic]У вас: {state.points} XP[/italic]")
        console.print("Использование: /shop <item_id> для покупки")
        return True, None, None, True

    # Покупка предмета
    items = load_shop_items()
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        console.print(f"[red]Товар с ID '{item_id}' не найден[/red]")
        return True, None, None, True

    cost = item["cost"]
    if state.points < cost:
        console.print(f"[red]Недостаточно XP. Нужно {cost}, у вас {state.points}[/red]")
        return True, None, None, True

    # Проверка, если это тема — уже ли владеет?
    if item["type"] == "theme":
        if item_id in state.owned_themes:
            console.print(f"[yellow]Вы уже владеете тему '{item['name']}'[/yellow]")
            return True, None, None, True
    # Для topic_unlock можно проверять, уже ли разблокирован
    if item["type"] == "unlock_topic":
        topic_value = item.get("value")
        if topic_value in state.unlocked_topics:
            console.print(f"[yellow]Тема '{topic_value}' уже разблокирована[/yellow]")
            return True, None, None, True

    # Выполняем покупку
    state.points -= cost
    state.apply_item_effect(item)
    state.save_to_file()

    console.print(f"[green]✅ Куплено: {item['name']}![/green]")
    if item["type"] == "theme":
        console.print("Активировать тему командой /theme ID (например /theme matrix)")
    elif item["type"] == "unlock_topic":
        console.print(
            f"Тема '{item.get('value')}' добавлена в доступные для quiz/adaptive"
        )
    elif item["type"] == "consumable":
        console.print(f"Добавлено: {item.get('quantity', 1)} x {item['name']}")
    elif item["type"] == "xp_boost":
        import time

        expiry = state.xp_boost_expiry
        console.print(
            f"XP буст активен до {time.ctime(expiry)} (x{state.xp_boost_multiplier})"
        )

    return True, None, None, True
