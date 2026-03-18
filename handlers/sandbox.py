"""
🔐 Песочница для выполнения кода
"""

import os
import re
import tempfile
import uuid
import shutil
from typing import Dict, Tuple, Any
from rich.console import Console
from practice import run_docker_cmd

console = Console()


def validate_code(code: str, language: str) -> str:
    """Проверка кода на опасные конструкции.
    Returns: пустая строка если OK, иначе сообщение об ошибке"""
    
    # Поддерживаемые языки
    supported = {'python', 'bash', 'sh'}
    if language not in supported:
        return f"Неподдерживаемый язык: {language}"
    
    # Общие опасные паттерны
    dangerous_patterns = [
        # Python
        (r'import\s+(os|sys|subprocess|socket|shutil|pty|ctypes)', 'запрещённый модуль'),
        (r'__import__\s*\(', 'динамический импорт'),
        (r'exec\s*\(', 'exec()'),
        (r'eval\s*\(', 'eval()'),
        (r'open\s*\(', 'open() - доступ к файлам'),
        (r'with\s+open', 'with open - доступ к файлам'),
        (r'commands\.', 'commands модуль'),
        (r'os\.system', 'os.system()'),
        (r'os\.popen', 'os.popen()'),
        (r'subprocess\.(call|run|Popen|check_output)', 'subprocess вызовы'),
        (r'socket\.', 'socket модуль'),
        (r'pty\.', 'pty модуль'),
        (r'ctypes\.', 'ctypes модуль'),
        (r'pickle\.', 'pickle модуль'),
        (r'compile\s*\(', 'compile()'),
        (r'globals\s*\(', 'globals()'),
        (r'locals\s*\(', 'locals()'),
        (r'getattr\s*\(', 'getattr()'),
        (r'setattr\s*\(', 'setattr()'),
        (r'delattr\s*\(', 'delattr()'),
        # Bash
        (r'rm\s+-rf', 'удаление файлов'),
        (r'mv\s+', 'перемещение файлов'),
        (r'cp\s+', 'копирование файлов'),
        (r'dd\s+', 'dd команда'),
        (r'cat\s+/', 'доступ к /etc'),
        (r'less\s+/', 'less системных файлов'),
        (r':\s*\(\s*\)\s*{', 'блоки функций'),
        (r'\(\(', 'арифметические выражения'),
        (r'\$\(', 'команда подстановки'),
        (r'`', 'backticks'),
        (r'>>', 'перенаправление добавления'),
        (r'>&', 'перенаправление дескрипторов'),
        (r'</dev/', 'чтение из /dev'),
        (r'/etc/', 'доступ к /etc'),
        (r'/home/', 'доступ к /home'),
        (r'/root/', 'доступ к /root'),
        (r'passwd', 'работа с паролями'),
        (r'shadow', 'работа с shadow'),
        (r'ssh', 'работа с ssh'),
        (r'systemctl', 'systemctl'),
        (r'service', 'service'),
        (r'chmod', 'chmod'),
        (r'chown', 'chown'),
        (r'sudo', 'sudo'),
        (r'su\s+', 'su'),
    ]
    
    for pattern, description in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return description
    
    return ""


def run_code_in_sandbox(code: str, language: str = "python", timeout: int = 10) -> Dict[str, Any]:
    """Запуск кода в изолированном Docker-контейнере"""
    
    # Валидация
    error = validate_code(code, language)
    if error:
        return {"success": False, "error": error}
    
    # Создаем временную директорию
    temp_dir = tempfile.mkdtemp(prefix="sandbox_")
    
    try:
        # Сохраняем код
        ext = "py" if language == "python" else "sh"
        code_file = os.path.join(temp_dir, f"code.{ext}")
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
        os.chmod(code_file, 0o644)
        
        # Создаем скрипт-обёртку с таймаутом
        wrapper = os.path.join(temp_dir, "run.sh")
        if language == "python":
            wrapper_content = f"""#!/bin/sh
timeout {timeout} python /tmp/code.py
"""
        else:  # bash
            wrapper_content = f"""#!/bin/sh
timeout {timeout} bash /tmp/code.sh
"""
        with open(wrapper, 'w') as f:
            f.write(wrapper_content)
        os.chmod(wrapper, 0o755)
        
        # Запускаем контейнер
        container_name = f"sandbox_{uuid.uuid4().hex[:8]}"
        
        # Образ для песочницы (используем python:3-slim для обоих, т.к. там есть bash)
        sandbox_image = "python:3-slim"
        
        # Docker run с ограничениями
        args = [
            "run", "--rm", "--name", container_name,
            "--memory", "256m",      # 256MB RAM
            "--cpus", "0.5",         # 0.5 CPU
            "--network", "none",     # нет сети
            "--read-only",           # FS только для чтения
            "--tmpfs", "/tmp:exec",  # /tmp исполняемый
            "--user", "nobody",      # запуск от nobody
            "-v", f"{temp_dir}:/tmp",
            sandbox_image,
            "sh", "-c", "chmod +x /tmp/run.sh && /tmp/run.sh"
        ]
        
        retcode, stdout, stderr = run_docker_cmd(args)
        
        return {
            "success": True,
            "returncode": retcode,
            "stdout": stdout,
            "stderr": stderr,
            "container": container_name
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        # Очистка
        shutil.rmtree(temp_dir, ignore_errors=True)


def handle_sandbox(action: str, **kwargs) -> Tuple[bool, Any, Any, bool]:
    """Обработчик команды /sandbox
    
    Формат:
    /sandbox python <code>
    /sandbox bash <code>
    """
    parts = action.strip().split(maxsplit=2)
    
    if len(parts) < 2:
        console.print("[red]Использование: /sandbox <python|bash> <код>[/red]")
        console.print("[dim]Пример: /sandbox python print('Hello, World!')[/dim]")
        return True, None, None, True
    
    language = parts[0].lower()
    code = parts[1] if len(parts) == 2 else parts[1]  # Если /sandbox python print или /sandbox python "print"
    if len(parts) == 3:
        code = parts[2]
    
    if language not in ("python", "bash", "sh"):
        console.print("[red]Поддерживаются только: python, bash[/red]")
        return True, None, None, True
    
    console.print(f"[cyan]▶ Выполняю {language} код...[/cyan]")
    
    result = run_code_in_sandbox(code, language)
    
    if not result["success"]:
        console.print(f"[red]❌ Ошибка: {result['error']}[/red]")
    else:
        rc = result["returncode"]
        stdout = result["stdout"].strip()
        stderr = result["stderr"].strip()
        
        # Вывод
        if rc == 0:
            console.print("[green]✅ Код выполнен успешно[/green]")
        else:
            console.print(f"[yellow]⚠️ Код завершился с кодом {rc}[/yellow]")
        
        if stdout:
            console.print(Panel(stdout, title="STDOUT", border_style="green"))
        if stderr:
            console.print(Panel(stderr, title="STDERR", border_style="yellow"))
        
        if not stdout and not stderr:
            console.print("[dim](нет вывода)[/dim]")
    
    return True, None, None, True
