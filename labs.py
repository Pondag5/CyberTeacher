"""
🔐 Командный тренажер (CLI Trainer)
"""
from ui import console, print_panel
from config import LLM

# База заданий для тренажера
TASKS = [
    {
        "id": 1,
        "category": "nmap",
        "question": "Сканировать все 65535 портов на цели 10.10.10.10",
        "correct_hint": "nmap -p- 10.10.10.10"
    },
    {
        "id": 2,
        "category": "nmap",
        "question": "Сканировать ОС и версии сервисов на цели 192.168.1.5 (агрессивно)",
        "correct_hint": "nmap -A 192.168.1.5"
    },
    {
        "id": 3,
        "category": "bash",
        "question": "Найти все файлы с расширением .txt в текущей папке и подпапках",
        "correct_hint": "find . -name '*.txt'"
    },
    {
        "id": 4,
        "category": "grep",
        "question": "Найти строку 'password' в файле config.txt, игнорируя регистр",
        "correct_hint": "grep -i 'password' config.txt"
    },
    {
        "id": 5,
        "category": "nmap",
        "question": "Проверить уязвимости SMB на Windows-машине (используя скрипты nmap)",
        "correct_hint": "nmap --script vuln -p 445 <target>"
    }
]

def check_docker():
    # Заглушка, Docker не нужен
    return True

def list_lab_categories():
    return ["Command Trainer", "Theory Quiz"]

def get_labs_by_category(category):
    return {"train": {"name": "CLI Практика", "description": "Тренировка команд"}}

def run_lab(lab_key, category):
    """Запуск сессии тренажера"""
    console.print("[bold green]💻 Режим тренировки команд активирован![/bold green]")
    console.print("Я буду давать задания, а ты пиши команды. Пиши [bold]exit[/bold] для выхода.\n")
    
    score = 0
    total = 0
    
    # Берем 3 случайных задания
    import random
    tasks_to_play = random.sample(TASKS, min(3, len(TASKS)))
    
    for task in tasks_to_play:
        total += 1
        console.print(f"[cyan]Задание {total}:[/cyan] {task['question']}")
        user_cmd = console.input("[bold yellow]Твоя команда > [/bold yellow]")
        
        if user_cmd.lower() in ["exit", "quit", "q"]:
            break
            
        # Проверяем через LLM (или простым совпадением для скорости)
        # Здесь используем LLM для умной проверки
        prompt = f"""
Ты — тренер по кибербезопасности. Пользователю дано задание: "{task['question']}'.
Правильный пример ответа: "{task['correct_hint']}'.
Пользователь написал: "{user_cmd}'.

Правильно ли это? Если да — напиши "ВЕРНО". Если нет — объясни ошибку кратко (1 предложение) и приведи правильную команду.
"""
        response = LLM.invoke(prompt)
        
        if "ВЕРНО" in response.upper():
            console.print(f"[green]✅ Верно![/green]\n")
            score += 1
        else:
            console.print(f"[red]❌ Ошибка:[/red]\n{response}\n")
            console.print(f"[dim]Подсказка: {task['correct_hint']}[/dim]\n")
            
    print_panel(f"Результат: [bold]{score}/{total}[/bold]", title="🏁 Конец тренировки", border_style="cyan")
    return True, "trainer"

def stop_lab():
    console.print("[yellow]Тренировка завершена.[/yellow]")
