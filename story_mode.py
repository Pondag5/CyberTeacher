"""
Story-mode - Игровое обучение кибербезопасности
Аналог HackNet / CTF с прогрессией
"""

import random
from dataclasses import dataclass
from typing import List, Optional

# === УРОВНИ ИГРОКА ===
PLAYER_LEVELS = {
    0: "Script Kiddie",
    100: "Hacker",
    300: "Penetration Tester",
    600: "Security Expert",
    1000: "Master Hacker",
    2000: "Legend"
}

def get_level(xp: int) -> str:
    """Получить уровень по XP"""
    level = "Script Kiddie"
    for threshold, title in PLAYER_LEVELS.items():
        if xp >= threshold:
            level = title
    return level

# === ЭПИЗОДЫ С ФЛАГАМИ И DOCKER ===
STORY_EPISODES = [
    # Web уязвимости (1-5)
    {"id": 1, "title": "Первое знакомство", "desc": "SQL инъекция в DVWA", "cat": "web", "diff": 1, "obj": ["Найти форму", "Получить данные"], "hint": ["' OR '1'='1"], "lab": "dvwa", "flag": "FLAG{SQL_1nj3ct10n}", "xp": 100},
    {"id": 2, "title": "XSS атака", "desc": "反射XSS в DVWA", "cat": "web", "diff": 1, "obj": ["Найти поле ввода", "Украсть cookie"], "hint": ["<script>alert(1)</script>"], "lab": "dvwa", "flag": "FLAG{XSS_C00k13}", "xp": 100},
    {"id": 3, "title": "CSRF ловушка", "desc": "Подделка запроса", "cat": "web", "diff": 2, "obj": ["Создать форму", "Изменить пароль"], "hint": ["<img src=x>"], "lab": "dvwa", "flag": "FLAG{CSRF_D0n3}", "xp": 150},
    {"id": 4, "title": "bWAPP SQLi", "desc": "bWAPP - SQL Injection", "cat": "web", "diff": 2, "obj": ["Найти уязвимость", "Вывести таблицы"], "hint": ["UNION SELECT"], "lab": "bwapp", "flag": "FLAG{bWAPP_SQL1}", "xp": 200},
    {"id": 5, "title": "Juice Shop", "desc": "OWASP Juice Shop", "cat": "web", "diff": 3, "obj": ["Найти все уязвимости", "Получить админку"], "hint": ["Зайди в /admin"], "lab": "juiceshop", "flag": "FLAG{Ju1c3_Sh0p}", "xp": 300},
    
    # Network (6-10)
    {"id": 6, "title": "Сканирование сети", "desc": "Nmap - найди хосты", "cat": "network", "diff": 1, "obj": ["Найти живые хосты", "Найти открытые порты"], "hint": ["nmap -sn 192.168.1.0/24"], "lab": "metasploitable2", "flag": "FLAG{Nm4p_Sc4n}", "xp": 100},
    {"id": 6, "title": "Сканирование сети", "desc": "Nmap - найди хосты", "cat": "network", "diff": 1, "obj": ["Найти живые хосты", "Найти открытые порты"], "hint": ["nmap -sn 192.168.1.0/24"], "lab": "metasploitable2", "flag": "FLAG{Nm4p_Sc4n}", "xp": 100},
    {"id": 7, "title": "FTP anonymous", "desc": "Анонимный доступ к FTP", "cat": "network", "diff": 1, "obj": ["Найти FTP", "Зайти anonymous"], "hint": ["ftp -p 192.168.1.x"], "lab": "metasploitable2", "flag": "FLAG{FTP_4n0n}", "xp": 100},
    {"id": 8, "title": "SSH брутфорс", "desc": "Hydra - подбор пароля", "cat": "network", "diff": 2, "obj": ["Найти SSH", "Подобрать пароль"], "hint": ["hydra -l root -P wordlist"], "lab": "metasploitable2", "flag": "FLAG{Hydr4_Brut3}", "xp": 200},
    {"id": 9, "title": "Wireshark анализ", "desc": "Анализ дампа трафика", "cat": "forensics", "diff": 2, "obj": ["Найти пароль", "Найти HTTP"], "hint": ["Follow TCP Stream"], "lab": None, "flag": "FLAG{W1r3sh4rk}", "xp": 200},
    {"id": 10, "title": "MitM атака", "desc": "Man-in-the-Middle", "cat": "network", "diff": 3, "obj": ["ARP спуфинг", "Перехват трафика"], "hint": ["arpspoof"], "lab": None, "flag": "FLAG{M1tM_4tt4ck}", "xp": 300},
    
    # OS / PrivEsc (11-15)
    {"id": 11, "title": "SUID Find", "desc": "Поиск SUID бинарников", "cat": "os", "diff": 2, "obj": ["Найти SUID", "Эксплуатировать"], "hint": ["find / -perm -4000"], "lab": "metasploitable2", "flag": "FLAG{SU1d_F1nd}", "xp": 200},
    {"id": 12, "title": "Linux Privesc", "desc": "LinPEAS - повышение привилегий", "cat": "os", "diff": 3, "obj": ["Найти вектор", "Получить root"], "hint": ["linpeas.sh"], "lab": "metasploitable2", "flag": "FLAG{L1nP34s}", "xp": 350},
    {"id": 13, "title": "SSH Key", "desc": "Найти SSH ключ", "cat": "os", "diff": 2, "obj": ["Найти ключ", "Использовать ключ"], "hint": ["find / -name id_rsa"], "lab": "metasploitable2", "flag": "FLAG{SSH_K3y}", "xp": 200},
    {"id": 14, "title": "Cron Job", "desc": "Эксплуатация Cron", "cat": "os", "diff": 3, "obj": ["Найти cron", "Подменить скрипт"], "hint": ["cat /etc/crontab"], "lab": "metasploitable2", "flag": "FLAG{Cr0n_J0b}", "xp": 300},
    {"id": 15, "title": "Buffer Overflow", "desc": "Переполнение буфера", "cat": "os", "diff": 4, "obj": ["Найти уязвимость", "Переполнить буфер"], "hint": ["python -c 'A'*100"], "lab": None, "flag": "FLAG{Buf_0v3rfl0w}", "xp": 500},
    
    # Crypto (16-18)
    {"id": 16, "title": "Base64", "desc": "Декодируй строку", "cat": "crypto", "diff": 1, "obj": ["Найти строку", "Декодировать"], "hint": ["echo '...' | base64 -d"], "lab": None, "flag": "FLAG{Bas364_D3c0d3}", "xp": 50},
    {"id": 17, "title": "XOR шифр", "desc": "Расшифруй XOR", "cat": "crypto", "diff": 2, "obj": ["Найти ключ", "Расшифровать"], "hint": ["XOR с повтором ключа"], "lab": None, "flag": "FLAG{X0r_Crypt0}", "xp": 200},
    {"id": 18, "title": "Hash Crack", "desc": "Взлом хеша", "cat": "crypto", "diff": 2, "obj": ["Найти хеш", "Подобрать пароль"], "hint": ["john hash.txt"], "lab": None, "flag": "FLAG{H4sh_Cr4ck}", "xp": 200},
    
    # Social Engineering (19-20)
    {"id": 19, "title": "Фишинг", "desc": "Создай фишинговую страницу", "cat": "social", "diff": 2, "obj": ["Скопировать сайт", "Перенаправить"], "hint": ["setoolkit"], "lab": None, "flag": "FLAG{Ph1sh1ng}", "xp": 200},
    {"id": 20, "title": "Экзамен", "desc": "Финальный тест", "cat": "exam", "diff": 4, "obj": ["Пройти все этапы"], "hint": ["Комбо всех знаний"], "lab": None, "flag": "FLAG{F1n4l_3x4m}", "xp": 500},
]

# === ДОСТИЖЕНИЯ ===
ACHIEVEMENTS = {
    "first_blood": {"name": "First Blood", "desc": "Пройди первый эпизод", "xp": 50},
    "web_hacker": {"name": "Web Hacker", "desc": "Пройди 5 web-эпизодов", "xp": 100},
    "network_ninja": {"name": "Network Ninja", "desc": "Пройди 5 network-эпизодов", "xp": 100},
    "root_master": {"name": "Root Master", "desc": "Получи root на любой машине", "xp": 200},
    "crypto_master": {"name": "Crypto Master", "desc": "Пройди все crypto эпизоды", "xp": 150},
    "complete_all": {"name": "Legend", "desc": "Пройди все эпизоды", "xp": 1000},
}


@dataclass
class StoryPlayer:
    """Игрок в Story Mode"""
    xp: int = 0
    completed_episodes: List[int] = None
    current_episode: int = 1
    
    def __post_init__(self):
        if self.completed_episodes is None:
            self.completed_episodes = []
    
    @property
    def level(self) -> str:
        return get_level(self.xp)
    
    def complete_episode(self, episode_id: int, xp: int):
        """Завершить эпизод"""
        if episode_id not in self.completed_episodes:
            self.completed_episodes.append(episode_id)
            self.xp += xp
    
    def check_achievements(self) -> List[str]:
        """Проверить достижения"""
        new_achievements = []
        
        # First Blood
        if len(self.completed_episodes) == 1 and "first_blood" not in self.completed_episodes:
            new_achievements.append("first_blood")
        
        # Web Hacker - 5 web эпизодов
        web_done = sum(1 for e in self.completed_episodes if e <= 5)
        if web_done >= 5:
            new_achievements.append("web_hacker")
        
        # Network Ninja - 5 network эпизодов  
        net_done = sum(1 for e in self.completed_episodes if 6 <= e <= 10)
        if net_done >= 5:
            new_achievements.append("network_ninja")
        
        return new_achievements


# Глобальный игрок
player = StoryPlayer()


def get_player() -> StoryPlayer:
    """Получить игрока"""
    return player


def start_story_mode(episode_id: int = None) -> str:
    """Начать эпизод"""
    global player
    
    if episode_id:
        ep = next((e for e in STORY_EPISODES if e["id"] == episode_id), STORY_EPISODES[0])
    else:
        # Найти следующий незавершённый
        for ep in STORY_EPISODES:
            if ep["id"] not in player.completed_episodes:
                break
        else:
            ep = STORY_EPISODES[0]
    
    player.current_episode = ep["id"]
    
    lab_info = ""
    if ep.get("lab"):
        lab_info = f"\n🎮 ЛАБОРАТОРИЯ: {ep['lab']}\nЗапусти: /lab start {ep['lab']}"
    
    return f"""╔══════════════════════════════════════╗
║     ЭПИЗОД #{ep['id']}: {ep['title']}
╚══════════════════════════════════════╝

📖 ОПИСАНИЕ: {ep['desc']}
🏷️  КАТЕГОРИЯ: {ep['cat']} | СЛОЖНОСТЬ: {'★' * ep['diff']}
⚡ XP: {ep['xp']}

🎯 ЦЕЛИ:
{chr(10).join(f'  • {o}' for o in ep['obj'])}

💡 ПОДСКАЗКА: {ep['hint'][0]}
🏴 ФЛАГ: {ep['flag'][:10]}...

{lab_info}

📊 ТВОЙ ПРОГРЕСС:
  XP: {player.xp} | Уровень: {player.level}
  Пройдено: {len(player.completed_episodes)}/{len(STORY_EPISODES)}
"""


def submit_flag(flag: str) -> str:
    """Проверить флаг"""
    global player
    
    # Ищем флаг в эпизодах
    for ep in STORY_EPISODES:
        if ep["flag"] == flag:
            if ep["id"] in player.completed_episodes:
                return f"❌ Эпизод #{ep['id']} уже пройден!"
            
            # Завершаем эпизод
            player.complete_episode(ep["id"], ep["xp"])
            
            # Проверяем достижения
            new_ach = player.check_achievements()
            ach_text = ""
            if new_ach:
                for ach_key in new_ach:
                    ach = ACHIEVEMENTS.get(ach_key, {})
                    ach_text += f"\n🏆 ПОЛУЧЕНО ДОСТИЖЕНИЕ: {ach.get('name', ach_key)} - {ach.get('desc', '')} (+{ach.get('xp', 0)} XP)"
            
            return f"""✅ ЭПИЗОД #{ep['id']}: {ep['title']} - ПРОЙДЕН!

⚡ +{ep['xp']} XP
📊 Всего XP: {player.xp} | Уровень: {player.level}
📈 Прогресс: {len(player.completed_episodes)}/{len(STORY_EPISODES)}{ach_text}

Следующий эпизод: /story"""
    
    return "❌ Неверный флаг! Попробуй ещё."


def get_story_list() -> str:
    """Список всех эпизодов"""
    global player
    
    lines = ["🎮 ДОСТУПНЫЕ ЭПИЗОДЫ:\n"]
    
    for ep in STORY_EPISODES:
        status = "✅" if ep["id"] in player.completed_episodes else "⬜"
        lines.append(f"{status} #{ep['id']:2d} {ep['title']:<20} [{ep['cat']:<8}] {'★' * ep['diff']:<4} +{ep['xp']} XP")
    
    lines.append(f"\n📊 Твой прогресс: {player.xp} XP | {player.level}")
    lines.append(f"   Пройдено: {len(player.completed_episodes)}/{len(STORY_EPISODES)}")
    
    return "\n".join(lines)


def get_achievements_list() -> str:
    """Список достижений"""
    global player
    
    lines = ["🏆 ДОСТИЖЕНИЯ:\n"]
    
    for key, ach in ACHIEVEMENTS.items():
        unlocked = key in [a for a in player.completed_episodes] or (
            key == "first_blood" and len(player.completed_episodes) >= 1
        )
        status = "✅" if unlocked else "🔒"
        lines.append(f"{status} {ach['name']:<15} - {ach['desc']} (+{ach['xp']} XP)")
    
    return "\n".join(lines)
