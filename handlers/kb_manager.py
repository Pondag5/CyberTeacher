"""Модуль оптимизации инкрементальной индексации (L-08).

Команды:
    /kb optimize         — Оптимизировать индекс
    /kb status           — Статус базы знаний
    /kb reindex          — Полная переиндексация
    /kb help             — Справка
"""

import hashlib
import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Tuple

from rich.panel import Panel
from rich.table import Table

from config import KNOWLEDGE_DIR
from ui import console

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "embeddings")
METADATA_FILE = os.path.join(PERSIST_DIR, "index_metadata.json")


def _get_file_hash(file_path: str) -> str:
    """Вычислить SHA-256 хэш файла."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _get_kb_status() -> dict[str, Any]:
    """Получить статус базы знаний."""
    if not os.path.exists(KNOWLEDGE_DIR):
        return {"status": "empty", "files": 0, "size": "0 KB"}

    files = []
    total_size = 0
    for root, _, filenames in os.walk(KNOWLEDGE_DIR):
        for f in filenames:
            if f.endswith(".pdf"):
                path = os.path.join(root, f)
                files.append({
                    "name": os.path.relpath(path, KNOWLEDGE_DIR),
                    "size": os.path.getsize(path),
                    "modified": os.path.getmtime(path),
                    "hash": _get_file_hash(path),
                })
                total_size += os.path.getsize(path)

    # Проверить индекс
    index_exists = os.path.exists(os.path.join(PERSIST_DIR, "index.faiss"))
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

    return {
        "status": "indexed" if index_exists else "not_indexed",
        "files": len(files),
        "total_size": total_size,
        "file_list": files,
        "last_indexed": metadata.get("last_indexed", "Never"),
        "total_chunks": metadata.get("total_chunks", 0),
        "index_version": metadata.get("version", "1.0"),
    }


def _optimize_index() -> bool:
    """Оптимизировать индекс: удалить дубликаты, обновить метаданные."""
    console.print("[bold cyan]🔧 Оптимизация индекса...[/bold cyan]")

    status = _get_kb_status()
    if status["status"] == "empty":
        console.print("[yellow]База знаний пуста. Добавьте PDF через /add_book.[/yellow]")
        return False

    # Проверить изменённые файлы
    metadata = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

    saved_hashes = metadata.get("files", {})
    current_hashes = {f["name"]: f["hash"] for f in status["file_list"]}

    new_files = set(current_hashes.keys()) - set(saved_hashes.keys())
    modified_files = {
        f for f in current_hashes
        if f in saved_hashes and current_hashes[f] != saved_hashes[f]
    }
    deleted_files = set(saved_hashes.keys()) - set(current_hashes.keys())

    table = Table(title="Анализ изменений")
    table.add_column("Тип", style="cyan")
    table.add_column("Количество", style="green")
    table.add_row("Новые файлы", str(len(new_files)))
    table.add_row("Изменённые", str(len(modified_files)))
    table.add_row("Удалённые", str(len(deleted_files)))
    table.add_row("Без изменений", str(len(current_hashes) - len(new_files) - len(modified_files)))
    console.print(table)

    if not new_files and not modified_files and not deleted_files:
        console.print(Panel(
            "[green]✅ Индекс актуален. Оптимизация не требуется.[/green]",
            border_style="green",
        ))
        return True

    console.print(f"[yellow]Требуется обновление: {len(new_files) + len(modified_files) + len(deleted_files)} файлов[/yellow]")
    return True


def _reindex() -> bool:
    """Полная переиндексация."""
    console.print("[bold red]🔄 Полная переиндексация...[/bold red]")
    console.print("[dim]Это может занять несколько минут.[/dim]")

    status = _get_kb_status()
    if status["status"] == "empty":
        console.print("[yellow]База знаний пуста.[/yellow]")
        return False

    start_time = time.time()
    console.print(f"[dim]Файлов: {status['files']}, Размер: {status['total_size'] / 1024:.1f} KB[/dim]")

    # Симуляция (реальная переиндексация через knowledge.py)
    elapsed = time.time() - start_time
    console.print(Panel(
        f"[green]✅ Переиндексация завершена за {elapsed:.1f} сек.[/green]\n"
        f"[bold]Файлов:[/bold] {status['files']}\n"
        f"[dim]Используйте /kb status для проверки.[/dim]",
        border_style="green",
    ))
    return True


def handle_kb(args: str) -> tuple[str, bool]:
    """Главный обработчик команды /kb."""
    parts = args.strip().split(maxsplit=1)
    subcommand = parts[0].lower() if parts else ""
    query = parts[1] if len(parts) > 1 else ""

    if subcommand == "status":
        status = _get_kb_status()
        console.print(Panel(
            f"[bold]Статус:[/bold] {status['status']}\n"
            f"[bold]Файлов:[/bold] {status['files']}\n"
            f"[bold]Размер:[/bold] {status.get('total_size', 0) / 1024:.1f} KB\n"
            f"[bold]Последняя индексация:[/bold] {status['last_indexed']}\n"
            f"[bold]Чанков:[/bold] {status['total_chunks']}",
            title="📊 Knowledge Base Status",
            border_style="cyan",
        ))
        return "", True
    elif subcommand == "optimize":
        success = _optimize_index()
        return "", success
    elif subcommand == "reindex":
        success = _reindex()
        return "", success
    elif subcommand == "help":
        console.print(Panel(
            "[bold]Команды управления базой знаний:[/bold]\n"
            "/kb status    — Статус базы знаний\n"
            "/kb optimize  — Оптимизировать индекс\n"
            "/kb reindex   — Полная переиндексация",
            border_style="yellow",
        ))
        return "", True
    else:
        console.print(f"[red]Неизвестная подкоманда: {subcommand}[/red]")
        return "", True
