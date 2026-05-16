# handlers/config.py — Interactive configuration wizard (M-28)
"""Step-by-step wizard for provider, model, API key setup."""

import os
from typing import Any

from rich.console import Console
from rich.panel import Panel

from di import get_context

console = Console()


def handle_config(action: str) -> tuple[bool, Any | None, Any | None, bool]:
    """Interactive configuration wizard."""
    import config

    ctx = get_context()
    state = ctx.state

    if action == "config":
        console.print(Panel(
            "[bold cyan]⚙️ Мастер настройки CyberTeacher[/bold cyan]\n\n"
            "Выберите действие:\n"
            "  [cyan]1[/cyan] — Настроить LLM провайдер (wizard)\n"
            "  [cyan]2[/cyan] — Показать текущую конфигурацию\n"
            "  [cyan]3[/cyan] — Сбросить настройки к дефолтным\n"
            "  [cyan]4[/cyan] — Настроить тему оформления (/theme)\n"
            "  [cyan]5[/cyan] — Управление модулями (/features)\n",
            title="НАСТРОЙКА",
            border_style="cyan",
        ))
        choice = input("Выбор: ").strip()

        if choice == "1":
            return _wizard_llm()
        elif choice == "2":
            return _show_config()
        elif choice == "3":
            return _reset_config()
        elif choice == "4":
            from handlers.theme import handle_theme
            return handle_theme("theme")
        elif choice == "5":
            from handlers.features import handle_features
            return handle_features("features")
        else:
            console.print("[yellow]Отмена[/yellow]")

    return True, None, None, True


def _wizard_llm() -> tuple[bool, Any | None, Any | None, bool]:
    """Пошаговая настройка LLM провайдера."""
    import config

    console.print("\n[bold green]🔧 Настройка LLM провайдера[/bold green]\n")

    # Шаг 1: Выбор провайдера
    console.print("[bold]Шаг 1/3: Выберите провайдер[/bold]")
    console.print("  [cyan]1[/cyan] — Ollama (локально, бесплатно)")
    console.print("  [cyan]2[/cyan] — OpenRouter (облако, API ключ)")
    console.print("  [cyan]3[/cyan] — HuggingFace (облако, HF token)")
    provider_choice = input("\nВыбор: ").strip()

    provider_map = {"1": "ollama", "2": "openrouter", "3": "huggingface"}
    provider = provider_map.get(provider_choice, "ollama")

    console.print(f"[green]✓ Провайдер: {provider}[/green]\n")

    # Шаг 2: Выбор модели
    console.print("[bold]Шаг 2/3: Выберите модель[/bold]")

    model_choices = {
        "ollama": [
            ("1", "qwen2.5:7b", "Рекомендуемая, баланс скорость/качество"),
            ("2", "llama3.2:3b", "Быстрая, меньше ресурсов"),
            ("3", "mistral:7b", "Хорошая для кода"),
        ],
        "openrouter": [
            ("1", "qwen/qwen-2.5-72b-instruct", "Мощная, ~$0.0003/1K tokens"),
            ("2", "meta-llama/llama-3.3-70b-instruct:free", "Бесплатная"),
            ("3", "google/gemma-3-27b-it:free", "Бесплатная, Google"),
        ],
        "huggingface": [
            ("1", "mistralai/Mixtral-8x7B-Instruct-v0.1", "Хорошая мультиязычная"),
            ("2", "meta-llama/Llama-2-70b-chat-hf", "Мощная, требуется доступ"),
        ],
    }

    models = model_choices.get(provider, model_choices["ollama"])
    for num, name, desc in models:
        console.print(f"  [cyan]{num}[/cyan] — {name} [dim]({desc})[/dim]")

    model_choice = input("\nВыбор: ").strip()
    model = None
    for num, name, _ in models:
        if num == model_choice:
            model = name
            break

    if not model:
        model_name = input("Введите название модели вручную: ").strip()
        model = model_name if model_name else models[0][1]

    console.print(f"[green]✓ Модель: {model}[/green]\n")

    # Шаг 3: API ключ (если нужен)
    api_key = None
    if provider in ("openrouter", "huggingface"):
        console.print("[bold]Шаг 3/3: API ключ[/bold]")
        console.print(f"[dim]Получите ключ на {'openrouter.ai/keys' if provider == 'openrouter' else 'huggingface.co/settings/tokens'}[/dim]")
        api_key = input("API ключ (или Enter для пропуска): ").strip()
        if api_key:
            if provider == "openrouter":
                os.environ["OPENROUTER_API_KEY"] = api_key
                console.print("[green]✓ OPENROUTER_API_KEY установлен[/green]")
            elif provider == "huggingface":
                os.environ["HF_TOKEN"] = api_key
                console.print("[green]✓ HF_TOKEN установлен[/green]")
        else:
            console.print("[yellow]⚠ Ключ не установлен — некоторые функции могут не работать[/yellow]")

    # Применяем настройки
    config.LLM_PROVIDER = provider
    if provider == "ollama":
        config.OLLAMA_MODEL = model
    elif provider == "openrouter":
        config.OPENROUTER_MODEL = model
    elif provider == "huggingface":
        config.HF_MODEL = model

    # Сброс кэша LLM
    config.LazyLoader._llm = None

    console.print(Panel(
        f"[bold green]✅ Настройка завершена![/bold green]\n\n"
        f"Провайдер: [cyan]{provider}[/cyan]\n"
        f"Модель: [cyan]{model}[/cyan]\n"
        f"API ключ: [cyan]{'установлен' if api_key else 'не требуется / пропущен'}[/cyan]\n\n"
        "[dim]Следующий запрос загрузит модель с новыми настройками.[/dim]",
        title="ГОТОВО",
        border_style="green",
    ))

    return True, None, None, True


def _show_config() -> tuple[bool, Any | None, Any | None, bool]:
    """Show current configuration."""
    import config

    provider = config.LLM_PROVIDER
    model = ""
    if provider == "ollama":
        model = config.OLLAMA_MODEL
    elif provider == "openrouter":
        model = config.OPENROUTER_MODEL
    elif provider == "huggingface":
        model = config.HF_MODEL

    has_key = ""
    if provider == "openrouter":
        has_key = "установлен" if os.environ.get("OPENROUTER_API_KEY") or config.OPENROUTER_API_KEY else "не установлен"
    elif provider == "huggingface":
        has_key = "установлен" if os.environ.get("HF_TOKEN") or config.HF_TOKEN else "не установлен"

    ctx = get_context()
    state = ctx.state
    theme = state.current_theme if hasattr(state, "current_theme") else "default"

    console.print(Panel(
        f"[bold]📋 Текущая конфигурация[/bold]\n\n"
        f"Провайдер: [cyan]{provider}[/cyan]\n"
        f"Модель: [cyan]{model}[/cyan]\n"
        f"API ключ: [cyan]{has_key if has_key else 'не требуется'}[/cyan]\n"
        f"Тема: [cyan]{theme}[/cyan]\n"
        f"Голос: [cyan]{'вкл' if state.voice_enabled else 'выкл'}[/cyan]\n"
        f"Подсказки: [cyan]{'вкл' if state.hint_enabled else 'выкл'}[/cyan]",
        title="КОНФИГУРАЦИЯ",
        border_style="cyan",
    ))

    return True, None, None, True


def _reset_config() -> tuple[bool, Any | None, Any | None, bool]:
    """Reset configuration to defaults."""
    import config

    console.print("[bold red]⚠️ Сбросить настройки к дефолтным?[/bold red]")
    confirm = input("Введите 'yes' для подтверждения: ").strip().lower()

    if confirm == "yes":
        config.LLM_PROVIDER = "ollama"
        config.OLLAMA_MODEL = "qwen2.5:7b"
        config.OPENROUTER_MODEL = "mistral-7b"
        config.HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        config.LazyLoader._llm = None

        ctx = get_context()
        state = ctx.state
        state.current_theme = "default"
        state.voice_enabled = False
        state.hint_enabled = True
        ctx.save_state()

        console.print("[green]✅ Настройки сброшены к дефолтным[/green]")
    else:
        console.print("[yellow]Отмена[/yellow]")

    return True, None, None, True
