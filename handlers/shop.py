"""Магазин достижений и улучшений (C-14)"""

import json
import os
import time
from datetime import datetime
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel

from di import get_context

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


def get_dynamic_price(item: dict, reputation: int) -> int:
    """SHOP-03: Рассчитать цену с учётом репутации."""
    base_cost = item["cost"]
    if reputation >= 500:
        return int(base_cost * 0.75)  # 25% скидка
    elif reputation >= 200:
        return int(base_cost * 0.85)  # 15% скидка
    elif reputation >= 100:
        return int(base_cost * 0.90)  # 10% скидка
    return base_cost


def handle_shop(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка команды /shop [item_id|history]

    Без аргументов — показать список товаров.
    С item_id — попытаться купить.
    history — показать историю покупок.
    """
    ctx = get_context()
    state = ctx.state
    parts = action.split(maxsplit=1)
    subcmd = parts[1].strip() if len(parts) > 1 else None

    # SHOP-02: Purchase history
    if subcmd == "history":
        history = getattr(state, "purchase_history", [])
        if not history:
            console.print("[yellow]История покупок пуста[/yellow]")
        else:
            console.print("[bold cyan]🛒 История покупок[/bold cyan]")
            console.print(f"[dim]Всего: {len(history)}[/dim]\n")
            total_spent = 0
            for entry in history[-15:]:
                dt = datetime.fromtimestamp(entry.get("timestamp", 0)).strftime("%Y-%m-%d %H:%M")
                name = entry.get("item_name", "?")
                cost = entry.get("cost", 0)
                total_spent += cost
                console.print(f"  [{dt}] {name} — {cost} XP")
            console.print(f"\n[dim]Всего потрачено: {total_spent} XP[/dim]")
        return True, None, None, True

    if subcmd is None:
        # Показать витрину
        items = load_shop_items()
        if not items:
            console.print("[yellow]Магазин временно недоступен[/yellow]")
            return True, None, None, True

        console.print("[bold cyan]🏪 Магазин[/bold cyan]\n")
        rep = state.reputation
        for item in items:
            # SHOP-03: Show dynamic price if applicable
            actual_cost = get_dynamic_price(item, rep)
            price_display = f"{actual_cost} XP"
            if actual_cost < item["cost"]:
                discount = int((1 - actual_cost / item["cost"]) * 100)
                price_display = f"[green]{actual_cost} XP[/green] [dim]({discount}% скидка, было {item['cost']})[/dim]"
            console.print(
                f"[bold]{item['name']}[/bold] (ID: {item['id']}) — {price_display}\n"
                f"  {item['description']}\n"
            )
        console.print(f"[italic]У вас: {state.points} XP | Репутация: {rep}[/italic]")
        if rep >= 100:
            discount = 10 if rep < 200 else (15 if rep < 500 else 25)
            console.print(f"[dim]Ваша скидка: {discount}% (репутация {rep})[/dim]")
        console.print("Использование: /shop <item_id> для покупки | /shop history")
        return True, None, None, True

    # Покупка предмета
    items = load_shop_items()
    item = next((i for i in items if i["id"] == subcmd), None)
    if not item:
        console.print(f"[red]Товар с ID '{subcmd}' не найден[/red]")
        return True, None, None, True

    # SHOP-03: Dynamic pricing
    actual_cost = get_dynamic_price(item, state.reputation)
    if state.points < actual_cost:
        console.print(f"[red]Недостаточно XP. Нужно {actual_cost}, у вас {state.points}[/red]")
        return True, None, None, True

    # Проверка, если это тема — уже ли владеет?
    if item["type"] == "theme":
        theme_value = item.get("value")
        if theme_value and theme_value in state.owned_themes:
            console.print(f"[yellow]Вы уже владеете тему '{item['name']}'[/yellow]")
            return True, None, None, True
    # Для topic_unlock можно проверять, уже ли разблокирован
    if item["type"] == "unlock_topic":
        topic_value = item.get("value")
        if topic_value in state.unlocked_topics:
            console.print(f"[yellow]Тема '{topic_value}' уже разблокирована[/yellow]")
            return True, None, None, True

    # Выполняем покупку
    state.points -= actual_cost
    state.apply_item_effect(item)

    # SHOP-02: Record purchase
    if not hasattr(state, "purchase_history"):
        state.purchase_history = []
    state.purchase_history.append({
        "timestamp": time.time(),
        "item_id": item["id"],
        "item_name": item["name"],
        "cost": actual_cost,
        "base_cost": item["cost"],
    })

    ctx.save_state()

    console.print(f"[green]✅ Куплено: {item['name']}![/green]")
    if actual_cost < item["cost"]:
        saved = item["cost"] - actual_cost
        console.print(f"[dim]Скидка: сэкономили {saved} XP[/dim]")
    if item["type"] == "theme":
        console.print("Активировать тему командой /theme ID (например /theme matrix)")
    elif item["type"] == "unlock_topic":
        console.print(
            f"Тема '{item.get('value')}' добавлена в доступные для quiz/adaptive"
        )
    elif item["type"] == "consumable":
        console.print(f"Добавлено: {item.get('quantity', 1)} x {item['name']}")
    elif item["type"] == "xp_boost":
        expiry = state.xp_boost_expiry
        console.print(
            f"XP буст активен до {time.ctime(expiry)} (x{state.xp_boost_multiplier})"
        )

    return True, None, None, True
