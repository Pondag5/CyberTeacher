"""Doctor command — LLM health check and onboarding.

Usage:
    /doctor              — show status of all LLM providers
    /doctor test         — test all providers with actual API calls
    /doctor setup ollama — guide through Ollama installation
    /doctor setup groq   — guide through Groq API key setup
"""

import os
from typing import Any, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from handlers.types import HandlerResult


console = Console()

OLLAMA_URL = "https://ollama.com/download"
GROQ_URL = "https://console.groq.com/keys"
OPENROUTER_URL = "https://openrouter.ai/keys"


def handle_doctor(action: str = "doctor") -> HandlerResult:
    """Handle /doctor command — show LLM provider status."""
    parts = action.split(maxsplit=2)
    subcmd = parts[1].strip().lower() if len(parts) > 1 else ""

    if subcmd == "setup":
        return _setup_wizard(parts[2].strip() if len(parts) > 2 else "")
    elif subcmd == "mock":
        return _set_mock_mode()
    elif subcmd == "test":
        return _test_all_providers()

    return _show_status()


def _show_status() -> HandlerResult:
    """Show health status of all LLM providers."""
    import config as _cfg

    table = Table(title="LLM Provider Status", border_style="cyan")
    table.add_column("Provider", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Details")

    # Check Ollama
    ollama_status, ollama_detail = _check_ollama()
    table.add_row("Ollama", ollama_status, ollama_detail)

    # Check Groq
    groq_key = _cfg.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
    if groq_key:
        table.add_row(
            "Groq",
            "[green]✅ Ключ задан[/green]",
            f"Модель: {_cfg.GROQ_MODEL}",
        )
    else:
        table.add_row("Groq", "[red]❌ Ключ не задан[/red]", f"/doctor setup groq")

    # Check OpenRouter
    or_key = _cfg.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
    if or_key:
        table.add_row(
            "OpenRouter",
            "[green]✅ Ключ задан[/green]",
            f"Модель: {_cfg.OPENROUTER_MODEL}",
        )
    else:
        table.add_row(
            "OpenRouter", "[red]❌ Ключ не задан[/red]", f"/doctor setup openrouter"
        )

    # Check HuggingFace
    hf_key = _cfg.HUGGINGFACE_API_KEY or os.getenv("HUGGINGFACE_API_KEY", "")
    if hf_key:
        table.add_row(
            "HuggingFace",
            "[green]✅ Ключ задан[/green]",
            f"Модель: {_cfg.HUGGINGFACE_MODEL}",
        )
    else:
        table.add_row("HuggingFace", "[red]❌ Ключ не задан[/red]", "Необязательно")

    # MockLLM — always available
    table.add_row("MockLLM", "[green]✅ Доступен[/green]", "Оффлайн-режим (заглушка)")

    console.print(table)

    # Current active provider
    from config import LazyLoader

    console.print(f"\n[bold]Текущий провайдер:[/bold] {_cfg.LLM_PROVIDER}")
    console.print(
        f"[bold]Fallback цепочка:[/bold] [dim]{' → '.join(_cfg.FALLBACK_ORDER)}[/dim]"
    )

    # Check if ResilientLLM is active
    try:
        llm = LazyLoader._llm
        if llm is not None:
            from resilient_llm import ResilientLLM

            if isinstance(llm, ResilientLLM):
                status = llm.get_status()
                for p in status["providers"]:
                    icon = "🟢" if p["circuit_state"] == "closed" else "🔴"
                    if p["is_current"]:
                        icon = "⭐"
                    console.print(
                        f"  {icon} [dim]{p['model']} — {p['circuit_state']}, errors: {p['failures']}[/dim]"
                    )
            elif hasattr(llm, "model") and llm.model == "mock-llm":
                console.print(
                    "[yellow]⚠️ Активен MockLLM — AI-ответы недоступны[/yellow]"
                )
    except (AttributeError, ValueError, RuntimeError):
        pass

    console.print("\n[dim]Команды:[/dim]")
    console.print("  /doctor test            — протестировать все провайдеры")
    console.print("  /doctor setup ollama    — установить Ollama")
    console.print("  /doctor setup groq      — настроить Groq API")
    console.print("  /doctor setup openrouter — настроить OpenRouter API")
    console.print("  /doctor mock            — переключиться на MockLLM")
    console.print("  /provider <name>        — сменить провайдер")
    console.print("  /provider test          — тест с таймаутом и fallback")

    return True, None, None, True


def _test_all_providers() -> HandlerResult:
    """Test all configured providers with actual API calls."""
    import config as _cfg
    from config import get_llm as _get_single_llm
    from resilient_llm import ResilientLLM

    console.print("[bold]🧪 Тестирование всех провайдеров API...[/bold]\n")

    results = []
    for provider in _cfg.FALLBACK_ORDER:
        if provider == "mock":
            results.append(("mock", "mock-llm", True, "Всегда доступен"))
            continue

        original = _cfg.LLM_PROVIDER
        _cfg.LLM_PROVIDER = provider
        llm_instance = _get_single_llm()
        _cfg.LLM_PROVIDER = original

        if llm_instance is None:
            results.append((provider, "?", False, "Не удалось инициализировать"))
            continue

        model = getattr(llm_instance, "model", "?")
        success, msg = ResilientLLM.test_provider(provider, llm_instance, timeout=10)
        results.append((provider, model, success, msg))

    table = Table(title="Результаты тестирования API", border_style="cyan")
    table.add_column("Провайдер", style="bold")
    table.add_column("Модель")
    table.add_column("Статус", justify="center")
    table.add_column("Детали")

    for provider, model, success, msg in results:
        icon = "[green]✅[/green]" if success else "[red]❌[/red]"
        table.add_row(provider, model, icon, msg[:80])

    console.print(table)
    console.print(
        "[dim]Тест отправляет 'ping' каждому провайдеру с таймаутом 10с[/dim]"
    )
    return True, None, None, True


def _check_ollama() -> Tuple[str, str]:
    """Check if Ollama is running and model is available."""
    import subprocess

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW
            if hasattr(subprocess, "CREATE_NO_WINDOW")
            else 0,
        )
        if result.returncode == 0:
            model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
            lines = result.stdout.strip().split("\n")
            models = [l.split()[0] for l in lines[1:] if l.strip()]
            if model in models:
                return "[green]✅ Работает[/green]", f"Модель {model} загружена"
            elif models:
                return (
                    "[yellow]⚠️ Модель не найдена[/yellow]",
                    f"Загружены: {', '.join(models[:3])}. Нужна: {model}",
                )
            else:
                return (
                    "[yellow]⚠️ Модели не загружены[/yellow]",
                    f"Запустите: ollama pull {model}",
                )
        return "[red]❌ Не найден[/red]", f"Установите: /doctor setup ollama"
    except FileNotFoundError:
        return "[red]❌ Не установлен[/red]", f"Установите: /doctor setup ollama"
    except Exception as e:
        return "[yellow]⚠️ Ошибка[/yellow]", str(e)[:50]


def _setup_wizard(provider: str) -> HandlerResult:
    """Interactive setup wizard for a specific provider."""
    if provider == "ollama":
        console.print(
            Panel(
                "[bold]Установка Ollama[/bold]\n\n"
                "[cyan]Шаг 1:[/cyan] Скачайте Ollama:\n"
                f"  {OLLAMA_URL}\n\n"
                "[cyan]Шаг 2:[/cyan] Установите модель:\n"
                "  ollama pull qwen2.5:7b\n\n"
                "[cyan]Шаг 3:[/cyan] Проверьте:\n"
                "  /doctor\n\n"
                "[dim]Для CPU: модель работает медленнее.\n"
                "Для GPU: нужен NVIDIA с 8+ GB VRAM.[/dim]",
                title="Установка Ollama",
                border_style="green",
            )
        )
    elif provider == "groq":
        console.print(
            Panel(
                "[bold]Настройка Groq[/bold]\n\n"
                "[cyan]Шаг 1:[/cyan] Зарегистрируйтесь:\n"
                f"  {GROQ_URL}\n\n"
                "[cyan]Шаг 2:[/cyan] Создайте API-ключ\n\n"
                "[cyan]Шаг 3:[/cyan] Установите:\n"
                "  /set-api-key groq YOUR_API_KEY\n\n"
                "[dim]Groq бесплатен для тестирования, быстрые ответы.[/dim]",
                title="Настройка Groq",
                border_style="green",
            )
        )
    elif provider == "openrouter":
        console.print(
            Panel(
                "[bold]Настройка OpenRouter[/bold]\n\n"
                "[cyan]Шаг 1:[/cyan] Зарегистрируйтесь:\n"
                f"  {OPENROUTER_URL}\n\n"
                "[cyan]Шаг 2:[/cyan] Создайте API-ключ\n\n"
                "[cyan]Шаг 3:[/cyan] Установите:\n"
                "  /set-api-key openrouter YOUR_API_KEY\n\n"
                "[dim]OpenRouter даёт доступ к 100+ моделям.[/dim]",
                title="Настройка OpenRouter",
                border_style="green",
            )
        )
    else:
        console.print(
            "[yellow]Используйте: /doctor setup <ollama|groq|openrouter>[/yellow]"
        )

    return True, None, None, True


def get_doctor_status() -> dict[str, Any]:
    """Return provider/system status as JSON dict for API endpoint."""
    import config as _cfg
    from config import LazyLoader

    providers: list[dict[str, Any]] = []

    providers.append(_check_ollama_json())
    groq_key = bool(_cfg.GROQ_API_KEY or os.getenv("GROQ_API_KEY", ""))
    providers.append(
        {
            "name": "Groq",
            "key_set": groq_key,
            "model": _cfg.GROQ_MODEL,
            "available": groq_key,
        }
    )
    or_key = bool(_cfg.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", ""))
    providers.append(
        {
            "name": "OpenRouter",
            "key_set": or_key,
            "model": _cfg.OPENROUTER_MODEL,
            "available": or_key,
        }
    )
    hf_key = bool(_cfg.HUGGINGFACE_API_KEY or os.getenv("HUGGINGFACE_API_KEY", ""))
    providers.append(
        {
            "name": "HuggingFace",
            "key_set": hf_key,
            "model": _cfg.HUGGINGFACE_MODEL,
            "available": hf_key,
        }
    )
    lm_key = bool(
        getattr(_cfg, "LMSTUDIO_API_KEY", None) or os.getenv("LMSTUDIO_API_KEY", "")
    )
    providers.append(
        {
            "name": "LMStudio",
            "key_set": lm_key,
            "model": _cfg.LMSTUDIO_MODEL,
            "available": True,
        }
    )
    providers.append(
        {"name": "MockLLM", "key_set": True, "model": "mock-llm", "available": True}
    )

    circuit: list[dict[str, Any]] = []
    try:
        llm = LazyLoader._llm
        if llm is not None:
            from resilient_llm import ResilientLLM

            if isinstance(llm, ResilientLLM):
                status = llm.get_status()
                circuit = status.get("providers", [])
    except (AttributeError, ValueError, RuntimeError):
        pass

    return {
        "current_provider": _cfg.LLM_PROVIDER,
        "fallback_order": list(getattr(_cfg, "FALLBACK_ORDER", [])),
        "providers": providers,
        "circuit_breakers": circuit,
        "mock_active": _cfg.LLM_PROVIDER == "mock",
    }


def _check_ollama_json() -> dict[str, Any]:
    """Check Ollama status and return JSON dict."""
    import subprocess

    model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW
            if hasattr(subprocess, "CREATE_NO_WINDOW")
            else 0,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            models = [l.split()[0] for l in lines[1:] if l.strip()]
            if model in models:
                return {
                    "name": "Ollama",
                    "running": True,
                    "model_loaded": True,
                    "model": model,
                    "key_set": True,
                    "available": True,
                }
            return {
                "name": "Ollama",
                "running": True,
                "model_loaded": False,
                "model": model,
                "loaded_models": models[:3],
                "key_set": True,
                "available": False,
            }
        return {
            "name": "Ollama",
            "running": False,
            "model_loaded": False,
            "model": model,
            "key_set": True,
            "available": False,
        }
    except FileNotFoundError:
        return {
            "name": "Ollama",
            "running": False,
            "model_loaded": False,
            "model": model,
            "key_set": True,
            "available": False,
        }
    except Exception as e:
        return {
            "name": "Ollama",
            "running": False,
            "model_loaded": False,
            "model": model,
            "error": str(e)[:80],
            "key_set": True,
            "available": False,
        }


def _set_mock_mode() -> HandlerResult:
    """Switch to MockLLM mode."""
    import config
    from config import LazyLoader

    config.LLM_PROVIDER = "mock"
    LazyLoader.invalidate()
    console.print(
        "[green]✅ Переключено на MockLLM (оффлайн-режим).[/green]\n"
        "[dim]AI-ответы будут заглушками. /doctor для настройки реального LLM.[/dim]"
    )
    return True, None, None, True
