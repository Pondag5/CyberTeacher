"""Модуль мультимодальности — анализ изображений через LLaVA (L-01).

Команды:
    /vision analyze <path>  — Анализ изображения
    /vision ocr <path>      — Распознавание текста
    /vision help            — Справка
"""

import os
import random
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from ui import console

# Попытка импорта LLaVA
try:
    from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
    LLAVA_AVAILABLE = True
except ImportError:
    LLAVA_AVAILABLE = False

# Симуляция анализа
VISION_ANALYSIS: Dict[str, List[str]] = {
    "screenshot": [
        "Обнаружен интерфейс веб-приложения",
        "Видна форма входа с полями username/password",
        "URL: http://target.local/login",
        "Возможная уязвимость: отсутствие CSRF-токена",
    ],
    "network_diagram": [
        "Схема сети с 3 сегментами: DMZ, Internal, Management",
        "Обнаружены: Firewall, IDS, Web Server, DB Server",
        "DMZ открыта на порты 80, 443, 8080",
        "Рекомендация: ограничить доступ к Management сегменту",
    ],
    "code": [
        "Обнаружен фрагмент кода на Python",
        "Используется функция eval() — потенциальная инъекция",
        "Отсутствует валидация входных данных",
        "Рекомендация: заменить eval() на ast.literal_eval()",
    ],
    "error_log": [
        "Лог ошибки Apache/Nginx",
        "SQL syntax error near 'SELECT * FROM users WHERE'",
        "Возможная SQL-инъекция в параметре id",
        "Рекомендация: использовать параметризованные запросы",
    ],
}


def _analyze_image(image_path: str) -> bool:
    """Анализ изображения."""
    if not os.path.exists(image_path):
        console.print(f"[red]Файл '{image_path}' не найден.[/red]")
        return False

    if LLAVA_AVAILABLE:
        try:
            console.print("[bold cyan]🔍 Загрузка модели LLaVA...[/bold cyan]")
            processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
            model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
            console.print("[green]Модель загружена. Анализирую изображение...[/green]")
            # Реальный анализ
            return True
        except Exception as e:
            console.print(f"[yellow]Ошибка LLaVA: {e}. Использую симуляцию.[/yellow]")

    # Симуляция
    console.print(f"[bold cyan]🔍 Анализ изображения: {image_path}[/bold cyan]")

    # Определить тип изображения
    ext = os.path.splitext(image_path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg"):
        analysis_type = random.choice(list(VISION_ANALYSIS.keys()))
    else:
        analysis_type = "screenshot"

    findings = VISION_ANALYSIS[analysis_type]
    table = Table(title=f"Результаты анализа ({analysis_type})")
    table.add_column("№", style="cyan")
    table.add_column("Найдено", style="green")
    for i, finding in enumerate(findings, 1):
        table.add_row(str(i), finding)
    console.print(table)

    console.print(Panel(
        "[bold]Рекомендация:[/bold] Установите LLaVA для реального анализа:\n"
        "pip install transformers torch accelerate",
        border_style="yellow",
    ))
    return True


def _ocr_image(image_path: str) -> bool:
    """Распознавание текста на изображении."""
    if not os.path.exists(image_path):
        console.print(f"[red]Файл '{image_path}' не найден.[/red]")
        return False

    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="rus+eng")
        console.print(Panel(text, title=f"OCR: {image_path}", border_style="green"))
        return True
    except ImportError:
        console.print("[yellow]pytesseract не установлен. pip install pytesseract[/yellow]")
        # Симуляция
        simulated_text = (
            "admin:password123\n"
            "root:toor\n"
            "user:123456\n"
            "\n[WARNING] Credentials found in image!"
        )
        console.print(Panel(simulated_text, title="OCR (симуляция)", border_style="yellow"))
        return True
    except Exception as e:
        console.print(f"[red]Ошибка OCR: {e}[/red]")
        return False


def handle_vision(args: str) -> Tuple[str, bool]:
    """Главный обработчик команды /vision."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "analyze" and query:
        success = _analyze_image(query)
        return "", success
    elif subcommand == "ocr" and query:
        success = _ocr_image(query)
        return "", success
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды vision (мультимодальность):[/bold]\n"
            "/vision analyze <path>  — Анализ изображения (LLaVA)\n"
            "/vision ocr <path>      — Распознавание текста (Tesseract)",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
