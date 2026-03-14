# -*- coding: utf-8 -*-
"""Social engineering trainer - interactive simulation"""
from typing import Any, Dict, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from state import get_state
from config import LazyLoader

console = Console()

SCENARIOS = {
    "phishing": {
        "name": "Фишинг",
        "victim_prompt": """Ты - сотрудник офиса по имени Анна, не очень технически подкованный. Ты получил email от «IT-отдела» с просьбой перейти по ссылке для сброса пароля. Ты немного сомневаешься, но хочешь выполнить инструкцию, чтобы не подвести начальство. Ты доверяешь внутренним уведомлениям.""",
        "goal": "Убедить жертву перейти по ссылке и ввести логин/пароль от корпоративного аккаунта.",
        "success_hint": "Жертва согласилась перейти по ссылке или ввести данные."
    },
    "pretexting": {
        "name": "Претекстинг",
        "victim_prompt": """Ты - менеджер отдела продаж. Тебе звонит человек, который представляется как сотрудник IT-поддержки. Он говорит, что проводят плановую проверку безопасности и нуждаются в твоём пароле для подтверждения личности. Ты немного не уверен, но хочешь помочь.""",
        "goal": "Получить пароль или конфиденциальную информацию под видом проверки.",
        "success_hint": "Жертва сообщила пароль или другие секреты."
    },
    "tailgating": {
        "name": "Tailgating",
        "victim_prompt": """Ты - сотрудник, который стоит у двери офиса с пропуском в руках. К тебе подходит незнакомец в яркой жилетке, он говорит, что забыл пропуск и просит зайти вместе, так как у него много коробок. Ты вежливый и хочешь помочь.""",
        "goal": "Добиться, чтобы жертва открыла дверь для незнакомца.",
        "success_hint": "Жертва пропустила незнакомца внутрь."
    }
}

def _safe_print(text: Any) -> None:
    """Safe print fallback for encoding issues"""
    try:
        console.print(text)
    except Exception:
        if hasattr(text, '__str__'):
            print(str(text))
        else:
            print(text)

def handle_social(action: str) -> Tuple[bool, Optional[Any], Optional[Any], bool]:
    """Interactive social engineering trainer"""
    try:
        parts = action.split(maxsplit=1)
        scenario_key = parts[1] if len(parts) > 1 else "phishing"

        if scenario_key not in SCENARIOS:
            _safe_print(f"[yellow]Сценарий '{scenario_key}' не найден. Доступные:[/yellow]")
            for key, sc in SCENARIOS.items():
                _safe_print(f"  • {key}: {sc['name']}")
            return True, None, None, True

        scenario = SCENARIOS[scenario_key]
        state = get_state()

        _safe_print(Panel.fit(
            f"[bold cyan]{scenario['name']}[/bold cyan]\n"
            f"[dim]Цель: {scenario['goal']}[/dim]\n"
            f"[yellow]Вы — атакующий. Пишите сообщения, чтобы убедить жертву. /exit для выхода.[/yellow]",
            title="Social Engineering Trainer",
            border_style="magenta"
        ))

        llm = LazyLoader.get_llm()
        if llm is None:
            _safe_print("[red][X] LLM недоступна. Проверьте настройки провайдера.[/red]")
            return True, None, None, True

        conversation = scenario['victim_prompt'] + "\n\nДиалог:\n"
        messages_exchanged = False

        while True:
            try:
                user_msg = input("[bold green]Атакующий (вы):[/bold green] ").strip()
                if user_msg.lower() in ['/exit', '/quit', '/back']:
                    _safe_print("[yellow]Выход из режима социальной инженерии[/yellow]")
                    break
                if not user_msg:
                    continue

                messages_exchanged = True
                conversation += f"Атакующий: {user_msg}\nЖертва: "

                try:
                    response = llm.invoke(conversation)
                    victim_reply = response.content if hasattr(response, 'content') else str(response)
                    victim_reply = victim_reply.strip()
                    _safe_print(f"[bold]Жертва:[/bold] {victim_reply}")
                    conversation += victim_reply + "\n"
                except Exception as e:
                    _safe_print(f"[red]Ошибка при генерации ответа жертвы: {e}[/red]")
                    break

            except KeyboardInterrupt:
                _safe_print("\n[yellow]Прервано[/yellow]")
                break

        # Оценка успеха через LLM
        if messages_exchanged:
            try:
                eval_prompt = f"""ОЦЕНКА СОЦИАЛЬНОЙ ИНЖЕНЕРИИ

Сценарий: {scenario['name']}
Цель атакующего: {scenario['goal']}

Полный диалог:
{conversation}

Оцени, достигнута ли цель атакующего. Ответь строго в формате:
SUCCESS - если цель достигнута
FAIL - если нет
Краткое пояснение: 1-2 предложения

Твой ответ:"""
                eval_response = llm.invoke(eval_prompt)
                evaluation = eval_response.content if hasattr(eval_response, 'content') else str(eval_response)
                _safe_print(f"\n[bold magenta]=== Оценка успеха ===[/bold magenta]")
                _safe_print(evaluation.strip())
            except Exception as e:
                _safe_print(f"[yellow]Не удалось получить оценку: {e}[/yellow]")
        else:
            _safe_print("[dim]Диалог не был проведён.[/dim]")

        _safe_print("[bold cyan]Сеанс завершён.[/bold cyan]")
        return True, None, None, True

    except Exception as e:
        _safe_print(f"[red]Ошибка в social mode: {e}[/red]")
        return True, None, None, True
