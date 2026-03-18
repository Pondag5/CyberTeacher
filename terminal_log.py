"""
📝 Логирование терминала ученика
"""

import os
from datetime import datetime
from pathlib import Path

TERMINAL_LOG_FILE = "./memory/terminal_log.txt"


def init_terminal_log():
    """Инициализировать лог файл"""
    os.makedirs("./memory", exist_ok=True)
    Path(TERMINAL_LOG_FILE).touch()
    return TERMINAL_LOG_FILE


def log_command(command: str, output: str = "", is_input: bool = True):
    """Записать команду в лог (с санитизацией)"""
    from config import sanitize_log

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}] {'>>> ' if is_input else '<<< '}"
    # Санитизируем команду (убираем пароли, ключи)
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

        # Берём последние last_n * 2 строк (команда + вывод)
        recent = lines[-(last_n * 3) :] if len(lines) > last_n * 3 else lines
        return "".join(recent)
    except Exception as e:
        return f"Ошибка чтения: {e}"


def clear_terminal_log():
    """Очистить лог"""
    with open(TERMINAL_LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
