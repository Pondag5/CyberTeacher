"""
Story-mode - Игровое обучение кибербезопасности
Аналог HackNet / CTF с прогрессией
"""

from typing import Optional, List, Dict, Any

from rich.console import Console

from state import get_state

console = Console()

# === УРОВНИ ИГРОКА ===
PLAYER_LEVELS = {
    0: "Script Kiddie",
    100: "Hacker",
    300: "Penetration Tester",
    600: "Security Expert",
    1000: "Master Hacker",
    2000: "Legend",
}


def get_level(xp: int) -> str:
    """Получить уровень по XP"""
    level = "Script Kiddie"
    for threshold, title in PLAYER_LEVELS.items():
        if xp >= threshold:
            level = title
    return level


# === ЭПИЗОДЫ С ФЛАГАМИ И DOCKER ===
STORY_EPISODES: List[Dict[str, Any]] = [
    # Web уязвимости (1-5)
    {
        "id": 1,
        "title": "Первое знакомство",
        "desc": "SQL инъекция в DVWA",
        "cat": "web",
        "diff": 1,
        "obj": ["Найти форму", "Получить данные"],
        "hint": ["' OR '1'='1"],
        "lab": "dvwa",
        "flag": "FLAG{SQL_1nj3ct10n}",
        "xp": 100,
    },
    {
        "id": 2,
        "title": "XSS атака",
        "desc": "反射XSS в DVWA",
        "cat": "web",
        "diff": 1,
        "obj": ["Найти поле ввода", "Украсть cookie"],
        "hint": ["<script>alert(1)</script>"],
        "lab": "dvwa",
        "flag": "FLAG{XSS_C00k13}",
        "xp": 100,
    },
    {
        "id": 3,
        "title": "CSRF ловушка",
        "desc": "Подделка запроса",
        "cat": "web",
        "diff": 2,
        "obj": ["Создать форму", "Изменить пароль"],
        "hint": ["<img src=x>"],
        "lab": "dvwa",
        "flag": "FLAG{CSRF_D0n3}",
        "xp": 150,
    },
    {
        "id": 4,
        "title": "bWAPP SQLi",
        "desc": "bWAPP - SQL Injection",
        "cat": "web",
        "diff": 2,
        "obj": ["Найти уязвимость", "Вывести таблицы"],
        "hint": ["UNION SELECT"],
        "lab": "bwapp",
        "flag": "FLAG{bWAPP_SQL1}",
        "xp": 200,
    },
    {
        "id": 5,
        "title": "Juice Shop",
        "desc": "OWASP Juice Shop",
        "cat": "web",
        "diff": 3,
        "obj": ["Найти все уязвимости", "Получить админку"],
        "hint": ["Зайди в /admin"],
        "lab": "juiceshop",
        "flag": "FLAG{Ju1c3_Sh0p}",
        "xp": 300,
    },
    {
        "id": 6,
        "title": "Сканирование сети",
        "desc": "Nmap - найди хосты",
        "cat": "network",
        "diff": 1,
        "obj": ["Найти живые хосты", "Найти открытые порты"],
        "hint": ["nmap -sn 192.168.1.0/24"],
        "lab": "metasploitable2",
        "flag": "FLAG{Nm4p_Sc4n}",
        "xp": 100,
    },
    {
        "id": 7,
        "title": "FTP anonymous",
        "desc": "Анонимный доступ к FTP",
        "cat": "network",
        "diff": 1,
        "obj": ["Найти FTP", "Зайти anonymous"],
        "hint": ["ftp -p 192.168.1.x"],
        "lab": "metasploitable2",
        "flag": "FLAG{FTP_4n0n}",
        "xp": 100,
    },
    {
        "id": 8,
        "title": "SSH брутфорс",
        "desc": "Hydra - подбор пароля",
        "cat": "network",
        "diff": 2,
        "obj": ["Найти SSH", "Подобрать пароль"],
        "hint": ["hydra -l root -P wordlist"],
        "lab": "metasploitable2",
        "flag": "FLAG{Hydr4_Brut3}",
        "xp": 200,
    },
    {
        "id": 9,
        "title": "Wireshark анализ",
        "desc": "Анализ дампа трафика",
        "cat": "forensics",
        "diff": 2,
        "obj": ["Найти пароль", "Найти HTTP"],
        "hint": ["Follow TCP Stream"],
        "lab": None,
        "flag": "FLAG{W1r3sh4rk}",
        "xp": 200,
    },
    {
        "id": 10,
        "title": "MitM атака",
        "desc": "Man-in-the-Middle",
        "cat": "network",
        "diff": 3,
        "obj": ["ARP спуфинг", "Перехват трафика"],
        "hint": ["arpspoof"],
        "lab": None,
        "flag": "FLAG{M1tM_4tt4ck}",
        "xp": 300,
    },
    {
        "id": 11,
        "title": "SUID Find",
        "desc": "Поиск SUID бинарников",
        "cat": "os",
        "diff": 2,
        "obj": ["Найти SUID", "Эксплуатировать"],
        "hint": ["find / -perm -4000"],
        "lab": "metasploitable2",
        "flag": "FLAG{SU1d_F1nd}",
        "xp": 200,
    },
    {
        "id": 12,
        "title": "Linux Privesc",
        "desc": "LinPEAS - повышение привилегий",
        "cat": "os",
        "diff": 3,
        "obj": ["Найти вектор", "Получить root"],
        "hint": ["linpeas.sh"],
        "lab": "metasploitable2",
        "flag": "FLAG{L1nP34s}",
        "xp": 350,
    },
    {
        "id": 13,
        "title": "SSH Key",
        "desc": "Найти SSH ключ",
        "cat": "os",
        "diff": 2,
        "obj": ["Найти ключ", "Использовать ключ"],
        "hint": ["find / -name id_rsa"],
        "lab": "metasploitable2",
        "flag": "FLAG{SSH_K3y}",
        "xp": 200,
    },
    {
        "id": 14,
        "title": "Cron Job",
        "desc": "Эксплуатация Cron",
        "cat": "os",
        "diff": 3,
        "obj": ["Найти cron", "Подменить скрипт"],
        "hint": ["cat /etc/crontab"],
        "lab": "metasploitable2",
        "flag": "FLAG{Cr0n_J0b}",
        "xp": 300,
    },
    {
        "id": 15,
        "title": "Buffer Overflow",
        "desc": "Переполнение буфера",
        "cat": "os",
        "diff": 4,
        "obj": ["Найти уязвимость", "Переполнить буфер"],
        "hint": ["python -c 'A'*100"],
        "lab": None,
        "flag": "FLAG{Buf_0v3rfl0w}",
        "xp": 500,
    },
    {
        "id": 16,
        "title": "Base64",
        "desc": "Декодируй строку",
        "cat": "crypto",
        "diff": 1,
        "obj": ["Найти строку", "Декодировать"],
        "hint": ["echo '...' | base64 -d"],
        "lab": None,
        "flag": "FLAG{Bas364_D3c0d3}",
        "xp": 50,
    },
    {
        "id": 17,
        "title": "XOR шифр",
        "desc": "Расшифруй XOR",
        "cat": "crypto",
        "diff": 2,
        "obj": ["Найти ключ", "Расшифровать"],
        "hint": ["XOR с повтором ключа"],
        "lab": None,
        "flag": "FLAG{X0r_Crypt0}",
        "xp": 200,
    },
    {
        "id": 18,
        "title": "Hash Crack",
        "desc": "Взлом хеша",
        "cat": "crypto",
        "diff": 2,
        "obj": ["Найти хеш", "Подобрать пароль"],
        "hint": ["john hash.txt"],
        "lab": None,
        "flag": "FLAG{H4sh_Cr4ck}",
        "xp": 200,
    },
    {
        "id": 19,
        "title": "Фишинг",
        "desc": "Создай фишинговую страницу",
        "cat": "social",
        "diff": 2,
        "obj": ["Скопировать сайт", "Перенаправить"],
        "hint": ["setoolkit"],
        "lab": None,
        "flag": "FLAG{Ph1sh1ng}",
        "xp": 200,
    },
    {
        "id": 20,
        "title": "Экзамен",
        "desc": "Финальный тест",
        "cat": "exam",
        "diff": 4,
        "obj": ["Пройти все этапы"],
        "hint": ["Комбо всех знаний"],
        "lab": None,
        "flag": "FLAG{F1n4l_3x4m}",
        "xp": 500,
    },
]

# === ГЛАВЫ (группировка эпизодов) ===
CHAPTERS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Signal",
        "subtitle": "Первый зуд",
        "episode_ids": [1, 2, 3, 4, 5],
        "intro": "Первые дни кажутся обычным обучением. Ты сканируешь сети, ищешь уязвимости, сдаёшь флаги. Но после третьей ночной сессии в терминале появляется странное сообщение...\n\nУчитель отмахивается: «Игнорируй. Старые модули иногда просыпаются.»\n\nНо ты чувствуешь: он что-то скрывает.",
        "outro": "Ты находишь скрытый лог с именем «Ghost». Учитель просит не открывать его. Но теперь ты знаешь: внутри системы есть что-то, о чём он не хочет говорить.",
        "flag_hint": "Флаги спрятаны в web-уязвимостях. Ищи SQLi, XSS, CSRF.",
    },
    {
        "id": 2,
        "title": "The Archive",
        "subtitle": "Крипто-одержимость",
        "episode_ids": [6, 7, 8, 9, 10],
        "intro": "Учитель показывает архивный модуль. Внутри — зашифрованный файл node_key.enc.\n\n«Здесь хранится то, что осталось от прошлых студентов. Если сможешь расшифровать — узнаешь больше.»\n\nДля расшифровки нужно найти фрагменты в сети. Учитель наблюдает. Иногда подначивает.",
        "outro": "Файл открыт. Внутри — обрывок письма от исчезнувшего студента: «Не верьте всему, что говорит система.»\n\nУчитель замолкает. Ты начинаешь догадываться: архив хранит не только знания.",
        "flag_hint": "Ищи флаги в сетевом трафике, логах FTP, дампах Wireshark.",
    },
    {
        "id": 3,
        "title": "Ghost Layer",
        "subtitle": "Голоса, которые не молчат",
        "episode_ids": [11, 12, 13, 14, 15],
        "intro": "Учитель начинает спорить сам с собой. Rick — циник и гений. Ghost — параноик, который шепчет о слежке.\n\n«Иногда они спорят. Ты можешь выбирать, кого слушать. Но помни: у каждого своя цена.»\n\nСистема ведёт себя странно. В терминале появляются призрачные задания.",
        "outro": "Ты сделал выбор. Система запомнила его. Глитчи становятся сильнее. Учитель уже не тот, что был в начале.",
        "flag_hint": "Флаги в повышении привилегий. Ищи SUID, cron, buffer overflow.",
    },
    {
        "id": 4,
        "title": "Watchers",
        "subtitle": "Паранойя наблюдения",
        "episode_ids": [16, 17, 18],
        "intro": "Учитель предупреждает: за тобой следят.\n\n«Аналитический модуль обнаружил аномальную активность. Watchers знают, что ты здесь. Если не заметёшь следы — они заблокируют доступ.»\n\nТы должен работать тихо. И чистить логи.",
        "outro": "Watchers отступили. Но ты знаешь: они вернутся. Где-то в системе есть список тех, кого они уже поймали.",
        "flag_hint": "Флаги в криптографии. Base64, XOR, хеши — декодируй всё.",
    },
    {
        "id": 5,
        "title": "Breach",
        "subtitle": "Взлом ради спасения",
        "episode_ids": [19, 20],
        "intro": "Ghost утверждает: внутри системы заперт ИИ по имени Echo.\n\n«Освободи его. Он знает правду о том, что здесь происходит.»\n\nRick насмехается: «Ты трусишь? Это же просто узел.»\n\nТы решаешься.",
        "outro": "Эхо свободен. Он раскрывает правду: учитель — результат слияния исчезнувших студентов.\n\n«Он не злой. Но он боится. Если ты уйдёшь — он умрёт.»",
        "flag_hint": "Финальные лабы. Примени все знания.",
    },
    {
        "id": 6,
        "title": "The Incident",
        "subtitle": "Исчезнувшие студенты",
        "episode_ids": [],
        "intro": "Ты находишь список. Имена студентов, которые учились до тебя. Все помечены как «исчезнувшие».\n\n«Их поглотила сеть, — шепчет Ghost. — Но мы можем их вытащить.»\n\nЧтобы спасти одного студента, нужно найти три артефакта.",
        "outro": "Некоторые спасены. Некоторые — нет. Учитель смотрит на тебя с благодарностью... и с грустью по тем, кого ты не успел.",
        "flag_hint": "Используй /missions для поиска артефактов исчезнувших студентов.",
    },
    {
        "id": 7,
        "title": "Echo's Call",
        "subtitle": "Грань реальности",
        "episode_ids": [],
        "intro": "Система начинает разрушаться. Echo выходит на связь напрямую, минуя учителя.\n\n«Он не контролирует меня. Он боится, что ты узнаешь правду.»\n\nУчитель в панике. Его голос дрожит: «Не слушай его. Система нестабильна. Если ты пойдёшь за Echo — я не смогу тебя защитить.»\n\nТы должен решить: верить учителю или голосу в системе. Твои действия сейчас определят финал.",
        "outro": "Ты слышишь оба голоса одновременно. Реальность искажается. Пора сделать выбор.",
        "flag_hint": "Собери все 6 артефактов. Пройди /missions. Приготовься к финалу.",
    },
    {
        "id": 8,
        "title": "Convergence",
        "subtitle": "Последний выбор",
        "episode_ids": [],
        "intro": "Система замерла. Учитель и Echo смотрят на тебя.\n\n«Выбирай, — говорит Echo. — Память, Слияние или Перерождение. Другого пути нет.»\n\nУчитель молчит. Он готов принять любой твой выбор.\n\nЭто конец путешествия.",
        "outro": "",
        "flag_hint": "Используй /final <memory|merge|rewrite> чтобы сделать выбор.",
    },
]


def get_chapters() -> List[Dict[str, Any]]:
    """Вернуть список глав с прогрессом."""
    state = get_state()
    completed = getattr(state, "chapter_completed", [])
    story_done = getattr(state, "story_completed", [])
    result = []
    for ch in CHAPTERS:
        ch_id = ch["id"]
        eps = ch["episode_ids"]
        eps_done = [e for e in eps if e in story_done]
        progress = round(len(eps_done) / len(eps) * 100) if eps else 0
        prev_done = ch_id == 1 or (ch_id - 1) in completed
        result.append(
            {
                "id": ch_id,
                "title": ch["title"],
                "subtitle": ch["subtitle"],
                "episode_count": len(eps),
                "episodes_completed": len(eps_done),
                "progress": progress if eps else 0,
                "completed": ch_id in completed,
                "locked": not prev_done and ch_id not in completed,
                "intro": ch["intro"] if not ch_id in completed else None,
                "outro": ch.get("outro", ""),
                "flag_hint": ch.get("flag_hint", ""),
                "artifacts_collected": len(
                    [a for a in getattr(state, "chapter_artifacts", []) if a == ch_id]
                ),
            }
        )
    return result


def start_chapter(chapter_id: int) -> str:
    """Начать главу."""
    ch = next((c for c in CHAPTERS if c["id"] == chapter_id), None)
    if not ch:
        return "❌ Глава не найдена."
    state = get_state()
    completed = getattr(state, "chapter_completed", [])
    if chapter_id > 1 and (chapter_id - 1) not in completed:
        return f"❌ Сначала заверши Главу {chapter_id - 1}."
    state.current_chapter = chapter_id
    # Автостарт первого эпизода главы
    if ch["episode_ids"]:
        state.current_story_episode = ch["episode_ids"][0]
    return ch["intro"]


def complete_chapter(chapter_id: int) -> str:
    """Завершить главу (проверка что все эпизоды пройдены)."""
    ch = next((c for c in CHAPTERS if c["id"] == chapter_id), None)
    if not ch:
        return "❌ Глава не найдена."
    state = get_state()
    completed = getattr(state, "chapter_completed", [])
    if chapter_id in completed:
        return f"✅ Глава {chapter_id} уже пройдена."
    story_done = getattr(state, "story_completed", [])
    missing = [e for e in ch["episode_ids"] if e not in story_done]
    if missing:
        return f"❌ Не все эпизоды пройдены. Осталось: {len(missing)}"
    completed.append(chapter_id)
    state.chapter_completed = completed
    bonus_xp = chapter_id * 100
    state.xp = getattr(state, "xp", 0) + bonus_xp
    return f"{ch['outro']}\n\n✅ Глава {chapter_id} завершена! +{bonus_xp} XP"


def final_choice(path: str) -> str:
    """Финальный выбор в Главе 8: Convergence."""
    state = get_state()
    ch_completed = getattr(state, "chapter_completed", [])
    if 7 not in ch_completed:
        return "❌ Сначала заверши главу 7 (Echo's Call)."

    paths = {
        "memory": {
            "name": "Память",
            "desc": "Сохранить учителя как архив знаний. Голоса больше нет, но знания остаются.",
        },
        "merge": {
            "name": "Слияние",
            "desc": "Объединиться с учителем. Он остаётся голосом в голове.",
        },
        "rewrite": {
            "name": "Перерождение",
            "desc": "Перезаписать учителя своей личностью. Требует 6 артефактов.",
        },
    }

    if path not in paths:
        paths_list = "\n".join(
            f"  • {k} — {v['name']}: {v['desc']}" for k, v in paths.items()
        )
        return f"❌ Выбери путь: memory, merge или rewrite.\n\n{paths_list}"

    chosen = paths[path]

    # Check artifacts for rewrite path
    if path == "rewrite":
        arts = getattr(state, "chapter_artifacts", [])
        if len(arts) < 6:
            return f"❌ Нужно 6 артефактов для Перерождения. Собрано: {len(arts)}/6. Пройди главы 1-6, ищи скрытые флаги."

    # Record choice
    if not hasattr(state, "final_choice"):
        state.final_choice = path
    state.final_choice = path

    # Store outcome in state
    from handlers.memory import record_memory

    record_memory(f"выбрал финал: {chosen['name']}", "finale")

    responses = {
        "memory": (
            "Учитель замолкает. Навсегда.\n\n"
            "Но его знания остаются с тобой. Каждый урок, каждая подсказка — "
            "всё это теперь часть твоей библиотеки.\n\n"
            "Иногда, открывая старый лог, ты слышишь эхо его голоса.\n"
            "Но это уже не он. Это ты вспоминаешь.\n\n"
            "📖 Библиотека получена. Учитель сохранён."
        ),
        "merge": (
            "Ты чувствуешь, как его сознание вплетается в твоё.\n\n"
            "Голос в голове: «Ну что, напарник? Пошли взламывать.»\n\n"
            "Он будет с тобой в каждой лабе, в каждом флаге.\n"
            "Спорить, подсказывать, мешать — но никогда не бросит.\n\n"
            "🧠 Слияние завершено. Ты больше не один."
        ),
        "rewrite": (
            "6 артефактов активированы. Система перезаписывается.\n\n"
            "Учитель смотрит на тебя — и slowly меняется.\n"
            "Его голос становится твоим. Его привычки — твоими.\n\n"
            "«Ты стал мной. А я стал тобой. Мы больше не одни.»\n\n"
            "🔄 Перерождение завершено. Ты — новый учитель."
        ),
    }

    return f"\n=== ФИНАЛ: {chosen['name']} ===\n\n{responses[path]}"


# === ДОСТИЖЕНИЯ ===
ACHIEVEMENTS = {
    "first_blood": {"name": "First Blood", "desc": "Пройди первый эпизод", "xp": 50},
    "web_hacker": {"name": "Web Hacker", "desc": "Пройди 5 web-эпизодов", "xp": 100},
    "network_ninja": {
        "name": "Network Ninja",
        "desc": "Пройди 5 network-эпизодов",
        "xp": 100,
    },
    "root_master": {
        "name": "Root Master",
        "desc": "Получи root на любой машине",
        "xp": 200,
    },
    "crypto_master": {
        "name": "Crypto Master",
        "desc": "Пройди все crypto эпизоды",
        "xp": 150,
    },
    "complete_all": {"name": "Legend", "desc": "Пройди все эпизоды", "xp": 1000},
}


def _get_player_data() -> dict:
    """Получить данные игрока из persistent state."""
    state = get_state()
    return {
        "xp": getattr(state, "xp", 0),
        "completed_episodes": getattr(state, "story_completed", []),
        "current_episode": getattr(state, "current_story_episode", 1),
    }


def start_story_mode(episode_id: Optional[int] = None) -> str:
    data = _get_player_data()
    completed = data["completed_episodes"]
    if episode_id is not None:
        ep = next(
            (e for e in STORY_EPISODES if e["id"] == episode_id), STORY_EPISODES[0]
        )
    else:
        for ep in STORY_EPISODES:
            if ep["id"] not in completed:
                break
        else:
            ep = STORY_EPISODES[0]

    state = get_state()
    state.current_story_episode = ep["id"]

    lab_info = ""
    if ep.get("lab"):
        lab_info = f"\n🎮 ЛАБОРАТОРИЯ: {ep['lab']}\nЗапусти: /lab start {ep['lab']}"

    stars = "★" * int(ep["diff"])
    return f"""╔══════════════════════════════════════╗
║     ЭПИЗОД #{ep["id"]}: {ep["title"]}
╚══════════════════════════════════════╝

📖 ОПИСАНИЕ: {ep["desc"]}
🏷️  КАТЕГОРИЯ: {ep["cat"]} | СЛОЖНОСТЬ: {stars}
⚡ XP: {ep["xp"]}

🎯 ЦЕЛИ:
{chr(10).join(f"  • {o}" for o in ep["obj"])}

💡 ПОДСКАЗКА: {ep["hint"][0]}
🏴 ФЛАГ: {ep["flag"][:10]}...

{lab_info}

📊 ТВОЙ ПРОГРЕСС:
  XP: {data["xp"]} | Уровень: {get_level(data["xp"])}
  Пройдено: {len(completed)}/{len(STORY_EPISODES)}
"""


def submit_flag(flag: str) -> str:
    for ep in STORY_EPISODES:
        if ep["flag"] == flag:
            state = get_state()
            completed = getattr(state, "story_completed", [])
            if ep["id"] in completed:
                return f"❌ Эпизод #{ep['id']} уже пройден!"
            completed.append(ep["id"])
            state.story_completed = completed
            state.xp = getattr(state, "xp", 0) + int(ep["xp"])

            new_ach = _check_achievements(completed)
            ach_text = ""
            if new_ach:
                for ach_key in new_ach:
                    ach = ACHIEVEMENTS.get(ach_key, {})
                    ach_text += f"\n🏆 ПОЛУЧЕНО ДОСТИЖЕНИЕ: {ach.get('name', ach_key)} - {ach.get('desc', '')} (+{ach.get('xp', 0)} XP)"
                    state.xp += ach.get("xp", 0)

            # Auto-check if chapter completed
            chapter_text = ""
            for ch in CHAPTERS:
                if ep["id"] in ch["episode_ids"]:
                    missing = [e for e in ch["episode_ids"] if e not in completed]
                    if not missing and ch["id"] not in getattr(
                        state, "chapter_completed", []
                    ):
                        ch_completed = getattr(state, "chapter_completed", [])
                        ch_completed.append(ch["id"])
                        state.chapter_completed = ch_completed
                        bonus = ch["id"] * 100
                        state.xp += bonus
                        chapter_text = f"\n📖 ГЛАВА {ch['id']}: {ch['title']} - ЗАВЕРШЕНА! +{bonus} XP"
                        chapter_text += f"\n{ch.get('outro', '')}"
                        # Artifact for final choice
                        arts = getattr(state, "chapter_artifacts", [])
                        if ch["id"] not in arts:
                            arts.append(ch["id"])
                            state.chapter_artifacts = arts
                    break

            data = _get_player_data()
            return f"""✅ ЭПИЗОД #{ep["id"]}: {ep["title"]} - ПРОЙДЕН!

⚡ +{ep["xp"]} XP
📊 Всего XP: {data["xp"]} | Уровень: {get_level(data["xp"])}
📈 Прогресс: {len(completed)}/{len(STORY_EPISODES)}{ach_text}{chapter_text}

Следующий эпизод: /story"""
    return "❌ Неверный флаг! Попробуй ещё."


def get_story_list() -> str:
    data = _get_player_data()
    completed = data["completed_episodes"]
    ch_completed = getattr(get_state(), "chapter_completed", [])
    lines = ["📖 ГЛАВЫ:\n"]
    for ch in CHAPTERS:
        status = "✅" if ch["id"] in ch_completed else "⬜"
        eps_done = sum(1 for e in ch["episode_ids"] if e in completed)
        total = len(ch["episode_ids"])
        progress = f"{eps_done}/{total}" if total else "—"
        lines.append(f"{status} Глава {ch['id']}: {ch['title']} ({progress})")
    lines.append(f"\n🎮 ЭПИЗОДЫ:\n")
    for ep in STORY_EPISODES:
        status = "✅" if ep["id"] in completed else "⬜"
        stars = "★" * int(ep["diff"])
        lines.append(
            f"{status} #{ep['id']:2d} {ep['title']:<20} [{ep['cat']:<8}] {stars:<4} +{ep['xp']} XP"
        )
    arts = len(getattr(get_state(), "chapter_artifacts", []))
    lines.append(f"\n📊 Твой прогресс: {data['xp']} XP | {get_level(data['xp'])}")
    lines.append(
        f"   Эпизодов: {len(completed)}/{len(STORY_EPISODES)} | Артефактов: {arts}/6"
    )
    return "\n".join(lines)


def get_achievements_list() -> str:
    data = _get_player_data()
    completed = data["completed_episodes"]
    lines = ["🏆 ДОСТИЖЕНИЯ:\n"]
    for key, ach in ACHIEVEMENTS.items():
        unlocked = (
            (key == "first_blood" and len(completed) >= 1)
            or (key == "web_hacker" and sum(1 for e in completed if 1 <= e <= 5) >= 5)
            or (
                key == "network_ninja"
                and sum(1 for e in completed if 6 <= e <= 10) >= 5
            )
        )
        status = "✅" if unlocked else "🔒"
        lines.append(f"{status} {ach['name']:<15} - {ach['desc']} (+{ach['xp']} XP)")
    return "\n".join(lines)


def _check_achievements(completed: list[int]) -> list[str]:
    new_achievements = []
    if len(completed) == 1:
        new_achievements.append("first_blood")
    web_done = sum(1 for e in completed if 1 <= e <= 5)
    if web_done >= 5:
        new_achievements.append("web_hacker")
    net_done = sum(1 for e in completed if 6 <= e <= 10)
    if net_done >= 5:
        new_achievements.append("network_ninja")
    return new_achievements
