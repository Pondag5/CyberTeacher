"""
📝 Логирование терминала ученика
"""

import os
from datetime import UTC, datetime
from pathlib import Path

TERMINAL_LOG_FILE = "./memory/terminal_log.txt"
MAX_LOG_SIZE = 512 * 1024  # 512 KB


def init_terminal_log():
    """Инициализировать лог файл"""
    os.makedirs("./memory", exist_ok=True)
    Path(TERMINAL_LOG_FILE).touch()
    return TERMINAL_LOG_FILE


def _rotate_if_needed():
    """Rotate terminal log if it exceeds MAX_LOG_SIZE (keep last 50%)."""
    try:
        size = os.path.getsize(TERMINAL_LOG_FILE)
        if size > MAX_LOG_SIZE:
            with open(TERMINAL_LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            # Keep the second half
            keep = lines[len(lines) // 2 :]
            with open(TERMINAL_LOG_FILE, "w", encoding="utf-8") as f:
                f.writelines(keep)
    except (OSError, IOError, IndexError):
        pass


def log_command(command: str, output: str = "", is_input: bool = True):
    """Записать команду в лог (с санитизацией и ротацией)"""
    from config import sanitize_log

    _rotate_if_needed()
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}] {'>>> ' if is_input else '<<< '}"
    sanitized = sanitize_log(command)
    entry += f" {sanitized}"
    if output:
        entry += f"\n{output}"

    with open(TERMINAL_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def get_terminal_log(last_n: int = 10) -> str:
    """Получить последние N записей из лога"""
    if not os.path.exists(TERMINAL_LOG_FILE):
        return "Лог пуст"

    try:
        with open(TERMINAL_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        recent = lines[-(last_n * 3) :] if len(lines) > last_n * 3 else lines
        return "".join(recent)
    except Exception as e:
        return f"Ошибка чтения: {e}"


def clear_terminal_log():
    """Очистить лог"""
    with open(TERMINAL_LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
