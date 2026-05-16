# handlers/news.py
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel

from state import get_state

console = Console()


def handle_security_news(
    action: str, llm: Any
) -> tuple[bool, Any | None, Any | None, bool]:
    """Обработка команды /news"""
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

        # Формируем для LLM
        news_for_llm = "\n".join([f"- {n.get('title', '')}" for n in news[:5]])

        # Если LLM доступен - обрабатываем
        llm_obj = llm() if callable(llm) else llm
        if llm_obj:
            console.print("[cyan]Обрабатываю новости...[/cyan]")
            prompt = f"""Кратко переведи на русский и опиши каждую новость в 1-2 предложениях:

{news_for_llm}

Формат:
1. [Название] - Краткое описание"""
            try:
                processed = llm_obj.invoke(prompt)  # type: ignore
                news_text = processed
            except Exception:
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


def _analyze_news(llm: Any) -> tuple[bool, Any | None, Any | None, bool]:
    """Анализ новостей учителем (M-17) — глубокий анализ с контекстом."""
    from config import LazyLoader
    from news_fetcher import fetch_news

    console.print("[cyan]Загружаю свежие новости для анализа...[/cyan]")
    news = fetch_news(force=True)

    if not news:
        console.print("[yellow]Новостей нет для анализа.[/yellow]")
        return True, None, None, True

    llm_obj = llm() if callable(llm) else llm
    if llm_obj is None:
        llm_obj = LazyLoader.get_llm()

    if llm_obj is None:
        console.print("[red]❌ LLM недоступна[/red]")
        return True, None, None, True

    news_text = "\n".join([
        f"- {n.get('title', '')}: {n.get('desc', '')}" for n in news[:5]
    ])

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
        console.print(Panel(content[:1200], title="🔍 АНАЛИЗ НОВОСТЕЙ", border_style="yellow"))

        state = get_state()
        state.news_analyzed = getattr(state, "news_analyzed", 0) + 1
        state.save_to_file()
    except Exception as e:
        console.print(f"[red]Ошибка анализа: {e}[/red]")

    return True, None, None, True


def get_last_news() -> str | None:
    """Получить последние новости для промта"""
    return get_state().last_news
