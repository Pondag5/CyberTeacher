# handlers/news.py
from typing import Any, Optional, Tuple

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()


def handle_security_news(
    action: str, LLM: Any
) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка команды /news"""
    console.print("[cyan]Загружаю новости...[/cyan]")
    try:
        from news_fetcher import fetch_news

        news = fetch_news(force=(action == "cve"))

        if not news:
            console.print("[yellow]Новостей нет.[/yellow]")
            return True, None, None, True

        # Формируем для LLM
        news_for_llm = "\n".join([f"- {n.get('title', '')}" for n in news[:5]])

        # Если LLM доступен - обрабатываем
        llm_obj = LLM() if callable(LLM) else LLM
        if llm_obj:
            console.print("[cyan]Обрабатываю новости...[/cyan]")
            prompt = f"""Кратко переведи на русский и опиши каждую новость в 1-2 предложениях:

{news_for_llm}

Формат:
1. [Название] - Краткое описание"""
            try:
                processed = llm_obj.invoke(prompt)  # type: ignore
                news_text = processed
            except:
                news_text = news_for_llm
        else:
            news_text = news_for_llm

        # Сохраняем в state и отмечаем проверку новостей
        get_state().last_news = news_text
        get_state().check_news()
        newly_earned = get_state().check_achievements()
        if newly_earned:
            for ach in newly_earned:
                console.print(
                    f"[bold magenta]🏆 Достижение: {ach['name']} ({ach['icon']}) +{ach.get('points', 0)} XP[/bold magenta]"
                )
        console.print(Panel(news_text[:800], title="НОВОСТИ"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def get_last_news() -> str | None:
    """Получить последние новости для промта"""
    return get_state().last_news
