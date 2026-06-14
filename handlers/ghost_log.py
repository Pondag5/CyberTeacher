"""Ghost Log — скрытый лог с атмосферными записями (Глава 1)."""

import random
from typing import List, Dict, Any

from state import get_state

GHOST_ENTRIES = [
    {
        "id": "gl_001",
        "chapter": 1,
        "condition": lambda s: True,
        "text": "[CORRUPTED] ...они смотрят через камеры. Не через объективы — через метаданные.",
        "hint": "Проверь EXIF у фото из лабы.",
    },
    {
        "id": "gl_002",
        "chapter": 1,
        "condition": lambda s: getattr(s, "noise_level", 0) > 30,
        "text": "[FRAGMENT] Шум — это не помехи. Это *их* голос. Чем выше — тем ближе.",
        "hint": "Stealth mode не панацея. Есть другие способы стать невидимым.",
    },
    {
        "id": "gl_003",
        "chapter": 1,
        "condition": lambda s: getattr(s, "digital_debts", 0) > 0,
        "text": "[WARNING] Долг — это не цифры. Это привязка. Каждый долг — нить, по которой тебя тянут.",
        "hint": "/debts покажет, кто тянет ниточки.",
    },
    {
        "id": "gl_004",
        "chapter": 2,
        "condition": lambda s: s.current_chapter >= 2,
        "text": "[LOG] Фракции — это не команды. Это идеологии, замаскированные под выбор. Выбирай внимательно.",
        "hint": "Репутация с фракциями открывает уникальные лабы. И закрывает другие.",
    },
    {
        "id": "gl_005",
        "chapter": 2,
        "condition": lambda s: s.current_chapter >= 2 and getattr(s, "faction_chosen", ""),
        "text": f"[ENCRYPTED] Твой выбор — {{faction}}. Хорошо. Теперь докажи, что достоин.",
        "hint": None,
    },
    {
        "id": "gl_006",
        "chapter": 3,
        "condition": lambda s: s.current_chapter >= 3 and getattr(s, "cp_level", 0) > 30,
        "text": "[GLITCH] Киберпсихоз — это не баг. Это фича системы. Она *хочет*, чтобы ты сдался.",
        "hint": "CP > 30 — триггер для Phantom Labs. И для чего-то ещё.",
    },
    {
        "id": "gl_007",
        "chapter": 3,
        "condition": lambda s: getattr(s, "trace_active", False),
        "text": "[TRACE] Они уже здесь. Таймер — это не предупреждение. Это дедлайн.",
        "hint": "wipe_logs покупает время. Но не навсегда.",
    },
    {
        "id": "gl_008",
        "chapter": 4,
        "condition": lambda s: s.current_chapter >= 4,
        "text": "[ARCHIVE] В глубине кода спрятано то, зачем ты пришёл. Не в флагах. В контексте.",
        "hint": "secret_room требует: 4 главы + фракция + watchers encounter.",
    },
    {
        "id": "gl_009",
        "chapter": 5,
        "condition": lambda s: s.current_chapter >= 5,
        "text": "[BACKDOOR] Двери, которые ты открыл, не закрываются. Они ведут туда, где не должен быть никто.",
        "hint": "/backdoor list покажет, что осталось открытым.",
    },
    {
        "id": "gl_010",
        "chapter": 6,
        "condition": lambda s: s.current_chapter >= 6,
        "text": "[FINAL] Выбор сделан. Путь зажат. Теперь осталось только пройти до конца.",
        "hint": None,
    },
    {
        "id": "gl_011",
        "chapter": 1,
        "condition": lambda s: getattr(s, "messages_sent", 0) > 50,
        "text": "[OBSERVER] Ты много говоришь. Всякое бывает полезно. Всякое — нет.",
        "hint": "Teacher memory запоминает не только факты. Тон. Стиль. Ошибки.",
    },
    {
        "id": "gl_012",
        "chapter": 1,
        "condition": lambda s: getattr(s, "stealth_ops", 0) >= 5,
        "text": "[GHOST] Ты учишься быть невидимым. Хорошо. Но помни: идеальная невидимость — это тоже сигнал.",
        "hint": "Слишком чистые логи подозрительнее грязных.",
    },
    {
        "id": "gl_013",
        "chapter": 2,
        "condition": lambda s: len(getattr(s, "memorable_events", [])) >= 3,
        "text": "[MEMORY] Учитель запомнил больше, чем ты думаешь. Каждое 'помнишь?' — это метка.",
        "hint": "memories влияют на подсказки. И на финальный выбор.",
    },
    {
        "id": "gl_014",
        "chapter": 1,
        "condition": lambda s: True,
        "text": "[ECHO] signal://ghost_log/entry_point — найди меня, когда будешь готов.",
        "hint": "Команда /ghost_log покажет доступные записи.",
    },
]


def get_available_entries() -> List[Dict[str, Any]]:
    """Вернуть записи, доступные для текущего состояния."""
    state = get_state()
    available = []
    for entry in GHOST_ENTRIES:
        if state.current_chapter >= entry["chapter"]:
            try:
                if entry["condition"](state):
                    available.append(entry)
            except Exception:
                continue
    return available


def format_entry(entry: Dict[str, Any], show_hint: bool = True) -> str:
    """Отформатировать запись для вывода."""
    lines = [
        f"\n{'='*60}",
        f"[LOG] Ghost Log Entry: {entry['id']} (Chapter {entry['chapter']})",
        f"{'='*60}",
        entry["text"],
    ]
    if show_hint and entry.get("hint"):
        lines.append(f"\n[HINT] Подсказка: {entry['hint']}")
    lines.append("="*60)
    return "\n".join(lines)


def handle_ghost_log(args: str = "") -> str:
    """CLI: /ghost_log [id|list|random]."""
    state = get_state()
    available = get_available_entries()

    if not available:
        return "[Ghost Log] Пока пусто. Пройди Главу 1."

    parts = args.strip().split()
    sub = parts[0].lower() if parts else "list"

    if sub == "list":
        lines = ["[Ghost Log] Доступные записи:"]
        for e in available:
            hint_tag = " [HINT]" if e.get("hint") else ""
            lines.append(f"  {e['id']} (Ch{e['chapter']}){hint_tag}")
        lines.append(f"\nВсего: {len(available)}. Использование: /ghost_log <id> или /ghost_log random")
        return "\n".join(lines)

    if sub == "random":
        entry = random.choice(available)
        return format_entry(entry)

    # Поиск по id
    for e in available:
        if e["id"] == sub:
            return format_entry(e)

    return f"[Ghost Log] Запись '{sub}' не найдена или недоступна. /ghost_log list для списка."