# handlers/misc.py (дополнительные функции, которые не warranted отдельного файла)
import os
from typing import Any, Dict, List, Optional, Tuple

from rich.console import Console
from rich.panel import Panel
from state import get_state

console = Console()

def _ask_confirm(message: str) -> bool:
    try:
        from rich.prompt import Confirm
        return Confirm.ask(message)
    except Exception:
        resp = input(f"{message} (yn): ").strip().lower()
        return resp in ("y", "yes", "true", "1")

def clear_chat_db(conn: Any) -> None:
    try:
        from memory import clear_chat as db_clear_chat
        db_clear_chat(conn)
    except Exception:
        pass

def extract_json_block(text: str) -> Optional[str]:
    if not text:
        return None
    stack = []
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if start is None:
                start = i
            stack.append(ch)
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack:
                    end = i + 1
                    return text[start:end]
    return None

def check_open_answer(
    question: str,
    user_ans: str,
    key_points: Optional[List[str]] = None,
) -> Dict[str, Any]:
    score = 0
    feedback = "Спасибо за ответ."
    if user_ans and len(user_ans.strip()) > 0:
        score = 6
        if "правильно" in user_ans.lower() or "верно" in user_ans.lower():
            score = 9
            feedback = "Отлично!"
    if key_points:
        found = 0
        upp = user_ans.lower() if user_ans else ""
        for kp in key_points:
            if kp.lower() in upp:
                found += 1
        if found >= max(1, len(key_points) // 2):
            score = min(10, score + 2)
            feedback = "Частично на ключевых моментах."
    return {"score": score, "feedback": feedback}

def handle_story_mode(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Режим истории (20 эпизодов) с интеграцией risk_level"""
    try:
        from story_mode import start_story_mode, submit_flag, get_story_list, get_achievements_list, get_player
        from state import get_state
        
        state = get_state()
        parts = action.split()
        
        if action == "story" or action == "episode" or action == "quest":
            # Показать список эпизодов
            console.print(get_story_list())
            return True, None, None, True
            
        elif len(parts) >= 2 and parts[0] == "story" and parts[1] == "start":
            # Начать конкретный эпизод
            try:
                if len(parts) >= 3:
                    episode_id = int(parts[2])
                    console.print(start_story_mode(episode_id))
                else:
                    console.print(start_story_mode())
            except ValueError:
                console.print("[red]Неверный номер эпизода[/red]")
            return True, None, None, True
            
        elif len(parts) >= 2 and parts[0] in ("story", "flag"):
            # Проверить флаг
            if len(parts) >= 3:
                flag = parts[2] if parts[0] == "flag" else " ".join(parts[2:])
                result = submit_flag(flag)
                console.print(result)
                
                # Обновляем риск уровень на основе успеха
                if "✅" in result or "ПРОЙДЕН" in result:
                    state.decrease_risk(15)  # Успех снижает риск
                    console.print(f"[green]🛡️ Уровень риска снижен! Текущий: {state.get_risk_status()} ({state.risk_level}/100)[/green]")
                else:
                    state.increase_risk(10)  # Ошибка повышает риск
                    console.print(f"[red]⚠️  Уровень риска повышен! Текущий: {state.get_risk_status()} ({state.risk_level}/100)[/red]")
            else:
                console.print("[yellow]Использование: /flag <флаг>  или  /story flag <флаг>[/yellow]")
            return True, None, None, True
            
        elif len(parts) >= 2 and parts[0] == "achievements":
            # Показать достижения
            console.print(get_achievements_list())
            return True, None, None, True
            
        else:
            console.print("[cyan]Использование Story Mode:[/cyan]")
            console.print("  /story            - список эпизодов")
            console.print("  /story start [N]  - начать эпизод N (или следующий)")
            console.print("  /flag <флаг>      - отправить флаг")
            console.print("  /achievements     - список достижений")
            return True, None, None, True
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
        return True, None, None, True

def handle_risk(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Управление и просмотр уровня риска"""
    try:
        from state import get_state
        state = get_state()
        parts = action.split()
        
        if len(parts) == 1:
            # Показать текущий статус
            status = state.get_risk_status()
            console.print(f"[bold cyan]⚡ Уровень риска: {status} ({state.risk_level}/100)[/bold cyan]")
            console.print("[dim]Уровень риска повышается при ошибках и снижается при успехах в CTF/Story режимах.[/dim]")
            return True, None, None, True
        
        # Изменить уровень вручную (для отладки/админа)
        if len(parts) >= 2:
            try:
                if parts[1] == "reset":
                    state.reset_risk()
                    console.print(f"[green]✅ Уровень риска сброшен[/green]")
                elif parts[1] == "up":
                    amount = int(parts[2]) if len(parts) >= 3 else 10
                    state.increase_risk(amount)
                    console.print(f"[yellow]⚠️  Уровень риска увеличен на {amount}[/yellow]")
                elif parts[1] == "down":
                    amount = int(parts[2]) if len(parts) >= 3 else 5
                    state.decrease_risk(amount)
                    console.print(f"[green]🛡️ Уровень риска уменьшен на {amount}[/green]")
                else:
                    amount = int(parts[1])
                    state.risk_level = max(0, min(100, amount))
                    console.print(f"[cyan]Уровень риска установлен: {state.risk_level}/100[/cyan]")
                
                console.print(f"[bold]Текущий статус: {state.get_risk_status()} ({state.risk_level}/100)[/bold]")
            except ValueError:
                console.print("[red]Использование: /risk [reset|up|down <колво>|число 0-100][/red]")
            
            return True, None, None, True
            
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_history(conn) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from memory import get_chat_history
        history = get_chat_history(conn, limit=20)
        if history:
            console.print("[bold cyan]📜 История чата:[/bold cyan]")
            for msg in history:
                role = msg.get('role', '?')
                content = msg.get('content', '')[:150]
                console.print(f"[{role}] {content}")
        else:
            console.print("[yellow]История пуста[/yellow]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True

def handle_course(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    console.print("[yellow]Курсы временно недоступны[/yellow]")
    return True, None, None, True

def handle_terminal_log(action: Optional[str] = None) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    try:
        from terminal_log import get_terminal_log, log_command
        if action and action.startswith("log "):
            cmd = action[4:].strip()
            log_command(cmd, is_input=False)
            console.print(f"[green]✅ Команда записана в лог[/green]")
            return True, None, None, True
        log_text = get_terminal_log(last_n=20)
        console.print(Panel(log_text, title="📟 Терминал (последние 20 строк)", border_style="cyan"))
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True

def handle_version() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    console.print("[bold cyan]CyberTeacher v3.2[/bold cyan]")
    console.print("Обучение кибербезопасности с LLM")
    console.print("Основано на: Ollama/OpenRouter, ChromaDB, Rich")
    console.print("© 2025 CyberTeacher Project")
    return True, None, None, True

def handle_writeup() -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    template = """
# Write-up: [Название задачи]

## Информация
- **Категория:** [web|crypto|pwn|forensics|reversing|misc]
- **Сложность:** [★☆☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★★☆]
- **Инструменты:** инструмент1, инструмент2, ...

## Описание
[Краткое описание задачи и цели]

## Решение

### 1. Разведка (Reconnaissance)
[Описание шагов разведки: сканирование, анализ, ...]

### 2. Эксплуатация (Exploitation)
[Как использовал уязвимость, команды, эксплойт]

### 3. Получение флага/доступа
[Что получилось в итоге, флаг]

## Выводы
- **Чему научился:** ...
- **Что было сложно:** ...
- **Что можно улучшить:** ...
"""
    console.print(Panel(template, title="📝 Шаблон Write-up", border_style="magenta"))
    return True, None, None, True

def handle_provider(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Управление провайдером LLM"""
    import config
    from config import LLM_PROVIDER, LazyLoader
    
    # Показать текущий провайдер
    if not action or action == "provider":
        console.print(f"[cyan]📡 Текущий провайдер: {LLM_PROVIDER}[/cyan]")
        console.print("[cyan]Доступные провайдеры:[/cyan]")
        console.print("  • ollama      - локально, бесплатно (рекомендуется)")
        console.print("  • openrouter  - облако, требуется API ключ")
        console.print("  • huggingface - HF Inference API, требуется HF_TOKEN")
        console.print("\nИспользование: /provider <имя>")
        return True, None, None, True
    
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[yellow]Использование: /provider <ollama|openrouter|huggingface>[/yellow]")
        return True, None, None, True
    
    provider = parts[1].strip()
    
    if provider not in ("ollama", "openrouter", "huggingface"):
        console.print("[red]❌ Неизвестный провайдер. Доступные: ollama, openrouter, huggingface[/red]")
        return True, None, None, True
    
    # Меняем провайдер
    old_provider = LLM_PROVIDER
    config.LLM_PROVIDER = provider
    # Сбрасываем кэш LLM для перезагрузки
    LazyLoader._llm = None
    
    console.print(f"[green]✅ Провайдер изменён: {old_provider} → {provider}[/green]")
    console.print("[yellow]Следующий запрос загрузит модель нового провайдера.[/yellow]")
    
    # Показываем настройки для нового провайдера
    if provider == "ollama":
        console.print(f"[dim]Модель: {config.OLLAMA_MODEL}[/dim]")
        console.print("[dim]Запустите 'ollama serve' и 'ollama pull <модель>' если ещё не[/dim]")
    elif provider == "openrouter":
        console.print(f"[dim]Модель: {config.OPENROUTER_MODEL}[/dim]")
        console.print("[dim]Убедитесь, что OPENROUTER_API_KEY установлен в .env[/dim]")
    elif provider == "huggingface":
        console.print(f"[dim]Модель: {config.HF_MODEL}[/dim]")
        console.print("[dim]Убедитесь, что HF_TOKEN установлен в .env[/dim]")
    
    return True, None, None, True


def handle_model(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Управление моделями LLM для текущего провайдера"""
    import config
    
    provider = config.LLM_PROVIDER
    
    # Показать текущую модель
    if not action or action == "model":
        console.print(f"[cyan]🤖 Текущий провайдер: {provider}[/cyan]")
        if provider == "ollama":
            console.print(f"[cyan]Модель: {config.OLLAMA_MODEL}[/cyan]")
            console.print("[cyan]Доступные модели: qwen2.5:7b, mistral:7b, llama2:7b и другие[/cyan]")
        elif provider == "openrouter":
            console.print(f"[cyan]Модель: {config.OPENROUTER_MODEL}[/cyan]")
            console.print("[cyan]Примеры: meta-llama/llama-3.3-70b-instruct:free, google/gemma-3-27b-it:free[/cyan]")
        elif provider == "huggingface":
            console.print(f"[cyan]Модель: {config.HF_MODEL}[/cyan]")
            console.print("[cyan]Примеры: mistralai/Mixtral-8x7B-Instruct-v0.1, meta-llama/Llama-2-70b-chat-hf[/cyan]")
        console.print("\nИспользование: /model <имя_модели>")
        return True, None, None, True
    
    # Изменить модель
    parts = action.split(maxsplit=1)
    if len(parts) < 2:
        console.print("[yellow]Использование: /model <имя_модели>[/yellow]")
        return True, None, None, True
    
    model_name = parts[1].strip()
    
    # Устанавливаем модель в зависимости от провайдера
    if provider == "ollama":
        config.OLLAMA_MODEL = model_name
        console.print(f"[green]✅ Модель Ollama изменена: {model_name}[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    elif provider == "openrouter":
        config.OPENROUTER_MODEL = model_name
        console.print(f"[green]✅ Модель OpenRouter изменена: {model_name}[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    elif provider == "huggingface":
        config.HF_MODEL = model_name
        console.print(f"[green]✅ Модель HuggingFace изменена: {model_name}[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    else:
        console.print("[red]❌ Неизвестный провайдер[/red]")
        return True, None, None, True
    
    console.print("[dim]Следующий запрос загрузит новую модель.[/dim]")
    return True, None, None, True


def handle_set_api_key(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Установка API ключа для провайдера"""
    import os
    
    if not action or action == "set-api-key":
        console.print("[cyan]Установка API ключа[/cyan]")
        console.print("Использование:")
        console.print("  /set-api-key openrouter <ключ>")
        console.print("  /set-api-key huggingface <ключ>")
        console.print("\nПримечание: Ключ будет сохранён только в текущей сессии.")
        return True, None, None, True
    
    parts = action.split(maxsplit=2)
    if len(parts) < 3:
        console.print("[yellow]Использование: /set-api-key <openrouter|huggingface> <api_key>[/yellow]")
        return True, None, None, True
    
    provider = parts[1].strip().lower()
    api_key = parts[2].strip()
    
    if provider == "openrouter":
        os.environ["OPENROUTER_API_KEY"] = api_key
        console.print("[green]✅ OPENROUTER_API_KEY установлен для текущей сессии[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    elif provider == "huggingface":
        os.environ["HF_TOKEN"] = api_key
        console.print("[green]✅ HF_TOKEN установлен для текущей сессии[/green]")
        console.print("[yellow]Сброс кэша LLM...[/yellow]")
        config.LazyLoader._llm = None
    else:
        console.print("[red]❌ Поддерживаются только: openrouter, huggingface[/red]")
    
    return True, None, None, True


def handle_add_book(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Добавить PDF книгу в базу знаний"""
    try:
        parts = action.split(maxsplit=1)
        if len(parts) < 2:
            console.print("[yellow]Использование: /add_book <путь_к_PDF>[/yellow]")
            return True, None, None, True

        src_path = parts[1].strip()
        if not os.path.exists(src_path):
            console.print(f"[red]Файл не найден: {src_path}[/red]")
            return True, None, None, True

        # ✅ Path traversal защита
        from config import KNOWLEDGE_DIR
        src_path_abs = os.path.abspath(src_path)
        knowledge_dir_abs = os.path.abspath(KNOWLEDGE_DIR)
        if not src_path_abs.startswith(knowledge_dir_abs):
            console.print("[red]❌ Запрещенный путь. Файл должен находиться в knowledge_base/[/red]")
            return True, None, None, True

        if not src_path.lower().endswith('.pdf'):
            console.print("[yellow]Поддерживаются только PDF файлы[/yellow]")
            return True, None, None, True

        import shutil
        filename = os.path.basename(src_path)
        dst_path = os.path.join(KNOWLEDGE_DIR, filename)

        if os.path.exists(dst_path):
            console.print(f"[yellow]Файл уже существует: {filename}[/yellow]")
            return True, None, None, True

        shutil.copy2(src_path, dst_path)
        console.print(f"[green]✓ Книга добавлена: {filename}[/green]")
        console.print("[cyan]Перезапустите приложение или запустите переиндексацию чтобы обновить базу.[/cyan]")

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
    return True, None, None, True


def handle_adaptive(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Показать слабые темы и адаптивный план обучения"""
    try:
        state = get_state()
        weak = state.get_weak_topics(threshold=70.0)
        if not weak:
            console.print("[green]Поздравляю! Нет слабых тем (все темы с успешностью >=70%)[/green]")
        else:
            console.print("[bold cyan]Адаптивное обучение: слабые темы[/bold cyan]")
            console.print(f"[dim]Порог: 70%. Темы с успешностью ниже порога приоритетны для повторения.[/dim]\n")
            for w in weak:
                console.print(f"  • {w['topic']}: {w['success_rate']:.1f}% (попыток: {w['attempts']})")
            # Recommend next focus
            next_topic = state.get_next_weak_topic()
            if next_topic:
                console.print(f"\n[yellow]Следующая тема для фокуса: {next_topic}[/yellow]")
                console.print("[dim]Запустите /quiz чтобы потренировать эту тему[/dim]")
        return True, None, None, True
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_repeat(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Интервальные повторения (Spaced Repetition) - повторение тем, готовых к проверке."""
    try:
        state = get_state()
        due = state.get_due_reviews()
        
        if not due:
            console.print("[green]🎉 Нет тем для повторения! Все темы в актуальном состоянии.[/green]")
            return True, None, None, True
        
        console.print("[bold cyan]📚 Темы для повторения:[/bold cyan]")
        console.print(f"[dim]Всего: {len(due)}[/dim]\n")
        for idx, item in enumerate(due, 1):
            console.print(f"  {idx}. {item['topic']} (интервал: {item['interval']} дней, попыток: {item['repetitions']})")
        
        console.print("\n[yellow]Выберите тему для повторения (номер) или /cancel для отмены[/yellow]")
        choice = input("Номер: ").strip()
        if choice.lower() in ['/cancel', '/exit']:
            console.print("[yellow]Отмена[/yellow]")
            return True, None, None, True
        
        try:
            idx = int(choice) - 1
        except ValueError:
            console.print("[red]Неверный ввод[/red]")
            return True, None, None, True
        
        if idx < 0 or idx >= len(due):
            console.print("[red]Неверный номер[/red]")
            return True, None, None, True
        
        topic = due[idx]['topic']
        console.print(f"[cyan]Запускаю квиз по теме: {topic}[/cyan]")
        
        try:
            from knowledge import get_current_vectordb
            from generators import generate_quiz
            vectordb = get_current_vectordb()
            quiz = generate_quiz(vectordb, topic=topic)
            questions = quiz.get('questions', [])
            if not questions:
                console.print("[yellow]Не удалось сгенерировать вопросы для этой темы[/yellow]")
                return True, None, None, True
        except Exception as e:
            console.print(f"[red]Ошибка генерации квиза: {e}[/red]")
            return True, None, None, True
        
        console.print(f"[bold green]📝 Квиз: {len(questions)} вопросов[/bold green]\n")
        total_score = 0
        max_total = 0
        
        for i, q in enumerate(questions, 1):
            console.print(f"[bold cyan]Вопрос {i}/{len(questions)}:[/bold cyan]")
            console.print(q.get('question', '?'))
            if 'options' in q:
                for opt_key, opt_val in q['options'].items():
                    console.print(f"  {opt_key}) {opt_val}")
            try:
                user_ans = input("\nВаш ответ: ").strip()
                if user_ans.lower() in ['/exit', '/quit']:
                    console.print("[yellow]Квиз прерван[/yellow]")
                    break
                if user_ans.lower() == '/skip':
                    console.print("[dim]Пропущено[/dim]\n")
                    continue
                if not user_ans:
                    console.print("[dim]Пустой ответ[/dim]\n")
                    continue
            except KeyboardInterrupt:
                console.print("\n[yellow]Прервано[/yellow]")
                break
            
            # Evaluate
            if 'options' in q:
                correct = q.get('correct', '')
                if user_ans.upper() == correct.upper():
                    score = 10
                    feedback = "✅ Верно!"
                else:
                    score = 0
                    feedback = f"❌ Неверно. Правильный ответ: {correct}"
            else:
                result = check_open_answer(q.get('question', ''), user_ans, None)
                score = result['score']
                feedback = result['feedback']
            console.print(f"[bold]Результат:[/bold] {score}/10 - {feedback}\n")
            total_score += score
            max_total += 10
        
        if max_total > 0:
            success_rate = total_score / max_total * 100
            console.print(f"[bold]📊 Итог:[/bold] {total_score}/{max_total} ({success_rate:.1f}%)")
            
            state.update_weak_topic(topic, total_score, max_total)
            state.mark_reviewed(topic, total_score, max_total)
            
            entry = state.review_schedule.get(topic, {})
            if entry:
                import time
                next_date = time.strftime("%Y-%m-%d", time.localtime(entry["next_review"]))
                console.print(f"[cyan]Следующее повторение: {next_date} (интервал: {entry['interval']} дней)[/cyan]")
            
            state.save_to_file()
        else:
            console.print("[dim]Нет результатов[/dim]")
        
        return True, None, None, True
        
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
        return True, None, None, True
        
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        import traceback
        traceback.print_exc()
        return True, None, None, True