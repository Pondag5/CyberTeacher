# handlers/news.py
from typing import Any, List, Dict, Union, Tuple

from rich.console import Console
from rich.panel import Panel

from di import get_context
from handlers.types import HandlerResult


console = Console()


def handle_security_news(action: str, llm: Any) -> HandlerResult:
    """Handle /news command."""
    parts = action.split(maxsplit=1)

    if len(parts) >= 2 and parts[1].lower() == "analyze":
        return _analyze_news(llm)

    console.print("[cyan]Загружаю новости...[/cyan]")
    try:
        from news_fetcher import fetch_news

        news = fetch_news(force=(action == "cve"))

        if not news:
            console.print("[yellow]Новостей нет.[/yellow]")
            return True, None, None, True

        # Приведение к единому формату списка словарей
        if isinstance(news, str):
            news = [{"title": news, "desc": ""}]
        elif isinstance(news, list) and all(isinstance(item, str) for item in news):
            news = [{"title": item, "desc": ""} for item in news]
        elif not isinstance(news, list):
            news = []

        if not news:
            console.print("[yellow]Новостей нет.[/yellow]")
            return True, None, None, True

        news_for_llm = "\n".join([f"- {n.get('title', '')}" for n in news[:5]])

        llm_obj = llm() if callable(llm) else llm
        if llm_obj:
            console.print("[cyan]Обрабатываю новости...[/cyan]")
            prompt = f"""Кратко переведи на русский и опиши каждую новость в 1-2 предложениях:

{news_for_llm}

Формат:
1. [Название] - Краткое описание"""
            try:
                response = llm_obj.invoke(prompt)
                news_text = (
                    response.content if hasattr(response, "content") else str(response)
                )
            except Exception:
                news_text = news_for_llm
        else:
            news_text = news_for_llm

        ctx = get_context()
        state = ctx.state
        state.last_news = news_text
        state.check_news()
        newly_earned = state.check_achievements()
        if newly_earned:
            for ach in newly_earned:
                console.print(f"[bold magenta]🏆 Достижение: {ach} [/bold magenta]")
        console.print(Panel(news_text[:800], title="НОВОСТИ"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def _analyze_news(llm: Any) -> HandlerResult:
    """News analysis by teacher (M-17) — deep analysis with context."""
    from config import LazyLoader
    from news_fetcher import fetch_news

    console.print("[cyan]Загружаю свежие новости для анализа...[/cyan]")
    news = fetch_news(force=True)

    if not news:
        console.print("[yellow]Новостей нет для анализа.[/yellow]")
        return True, None, None, True

    if isinstance(news, str):
        news = [{"title": news, "desc": ""}]
    elif isinstance(news, list) and all(isinstance(item, str) for item in news):
        news = [{"title": item, "desc": ""} for item in news]
    elif not isinstance(news, list):
        news = []

    if not news:
        console.print("[yellow]Новостей нет.[/yellow]")
        return True, None, None, True

    llm_obj = llm() if callable(llm) else llm
    if llm_obj is None:
        llm_obj = LazyLoader.get_llm()

    if llm_obj is None:
        console.print("[red]❌ LLM недоступна[/red]")
        return True, None, None, True

    news_text = "\n".join(
        [f"- {n.get('title', '')}: {n.get('desc', '')}" for n in news[:5]]
    )

    prompt = f"""Ты — хакер из 90-х, учитель кибербезопасности. Проанализируй свежие новости.

Новости:
{news_text}

Для каждой новости:
1. Кратко опиши суть (1 предложение)
2. Свяжи с историей ("Это напоминает мне случай...")
3. Оцени уровень угрозы (🟢 низкий / 🟡 средний / 🔴 высокий)
4. Дай рекомендацию ученику

В конце — общую сводку: какие тренды видишь, на что обратить внимание."""

    try:
        console.print("[cyan]Учитель анализирует новости...[/cyan]")
        response = llm_obj.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        console.print(
            Panel(content[:1200], title="🔍 АНАЛИЗ НОВОСТЕЙ", border_style="yellow")
        )

        ctx = get_context()
        state = ctx.state
        state.news_analyzed = getattr(state, "news_analyzed", 0) + 1
        ctx.save_state()
    except Exception as e:
        console.print(f"[red]Ошибка анализа: {e}[/red]")

    return True, None, None, True


def get_last_news() -> Union[str, None]:
    """Get last news for prompt."""
    return get_context().state.last_news
