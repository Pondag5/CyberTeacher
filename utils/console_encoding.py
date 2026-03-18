"""Настройка кодировки консоли для Windows"""

import io
import os
import sys


def setup_utf8_console() -> None:
    """Настраивает stdout/stderr на UTF-8 для Windows.

    Решает проблему UnicodeEncodeError при выводе эмодзи и спецсимволов
    в консоли Windows (cp1251/cp437).
    """
    if sys.platform != "win32":
        return

    try:
        # Меняем кодовую страницу консоли на UTF-8 (65001)
        # >nul 2>&1 подавляет вывод команды
        os.system("chcp 65001 >nul 2>&1")
    except Exception:
        pass

    try:
        # Переупаковываем stdout в UTF-8 с заменой недопустимых символов
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer,
                encoding="utf-8",
                errors="replace",  # заменяет недопустимые символы на ?
            )
        if hasattr(sys.stderr, "buffer"):
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, encoding="utf-8", errors="replace"
            )
    except Exception:
        # Если не получилось — просто игнорируем
        pass
