"""
🔐 Конфигурация CyberTeacher
"""

import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# === ПУТИ (можно переопределить через .env) ===
PERSIST_DIR = os.getenv("PERSIST_DIR", "./embeddings")
DB_FILE = os.getenv("DB_FILE", "./memory/chat_history.db")
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "./knowledge_base")
METADATA_FILE = os.getenv("METADATA_FILE", "./embeddings/metadata.json")
STATE_FILE = os.getenv("STATE_FILE", "./memory/app_state.json")
ACHIEVEMENTS_FILE = os.getenv("ACHIEVEMENTS_FILE", "./data/achievements.json")
LOG_FILE = os.getenv("LOG_FILE", "./cyberteacher.log")
# === ЛОГИРОВАНИЕ ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# === КОДИРОВКА ===
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["COLORTERM"] = "truecolor"

# === LLM ПРОВАЙДЕР ===
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# === OLLAMA ===
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.3"))

# === OPENROUTER ===
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# === HUGGINGFACE ===
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1")
HF_API_URL = os.getenv("HF_API_URL", "https://api-inference.huggingface.co/models")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Общее имя модели (логирование)
MODEL_NAME = OLLAMA_MODEL if LLM_PROVIDER == "ollama" else OPENROUTER_MODEL

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# === ОПТИМИЗАЦИЯ ===
MAX_WORKERS = 8  # Уменьшили для снижения нагрузки
CHUNK_SIZE = 600  # Оптимально для технической документации (было 300)
CHUNK_OVERLAP = 50  # Сохраняем контекст между чанками (было 15)

# === ПЕДАГОГИКА ===
SOCRATIC_ENABLED = True
THINKING_ENABLED = True

# === RERANKING ===
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 5  # Сколько лучших чанков возвращать после реранкинга

# === ГИБРИДНЫЙ ПОИСК (BM25) ===
BM25_ENABLED = os.getenv("BM25_ENABLED", "true").lower() == "true"
BM25_K = int(os.getenv("BM25_K", "20"))

# === ЛИМИТЫ LLM ===
MAX_TOKENS = 2000  # Максимальное количество токенов в ответе LLM

# === КЭШИРОВАНИЕ ===
RESPONSE_CACHE_SIZE = 100  # LRU кэш для ответов LLM
RESPONSE_CACHE_FILE = "./memory/response_cache.json"  # Персистентный кэш


# === LAZY LOADING (Оптимизация) ===
class LazyLoader:
    """Ленивая загрузка моделей - загружаются только при первом использовании"""

    _llm = None
    _embeddings = None
    _embedding_model = None
    _reranker = None

    @classmethod
    def get_llm(cls):
        if cls._llm is None:
            import logging

            logging.getLogger(__name__).info(
                f"🔐 Загрузка модели LLM ({LLM_PROVIDER})..."
            )

            if LLM_PROVIDER == "ollama":
                from langchain_community.chat_models import ChatOllama

                cls._llm = ChatOllama(
                    model=OLLAMA_MODEL,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OLLAMA_URL,
                    num_predict=MAX_TOKENS,
                )
            elif LLM_PROVIDER == "openrouter":
                from langchain_openai import ChatOpenAI

                if not OPENROUTER_API_KEY:
                    raise ValueError("OPENROUTER_API_KEY не установлен в .env")
                cls._llm = ChatOpenAI(
                    model=OPENROUTER_MODEL,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OPENROUTER_URL,
                    api_key=OPENROUTER_API_KEY,
                    max_tokens=MAX_TOKENS,
                )
            elif LLM_PROVIDER == "huggingface":
                from langchain_huggingface import HuggingFaceEndpoint

                if not HF_TOKEN:
                    raise ValueError("HF_TOKEN не установлен в .env")
                cls._llm = HuggingFaceEndpoint(
                    repo_id=HF_MODEL,
                    huggingfacehub_api_token=HF_TOKEN,
                    max_new_tokens=MAX_TOKENS,
                    temperature=MODEL_TEMPERATURE,
                )
            else:
                raise ValueError(f"Неизвестный LLM_PROVIDER: {LLM_PROVIDER}")

            logging.getLogger(__name__).info(f"🔐 LLM загружена ({LLM_PROVIDER}).")
        return cls._llm

    @classmethod
    def get_embeddings(cls):
        if cls._embeddings is None:
            import logging

            logging.getLogger(__name__).info("🔐 Загрузка модели эмбеддингов...")
            import torch
            from langchain_huggingface import HuggingFaceEmbeddings

            device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.getLogger(__name__).info(f"🔐 Используется устройство: {device}")

            cls._embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL, model_kwargs={"device": device}
            )
            logging.getLogger(__name__).info("🔐 Эмбеддинги загружены.")
        return cls._embeddings

    @classmethod
    def get_reranker(cls):
        if cls._reranker is None:
            import logging

            logging.getLogger(__name__).info("🔐 Загрузка модели реранкера...")
            import torch
            from sentence_transformers import CrossEncoder

            device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.getLogger(__name__).info(f"🔐 Используется устройство: {device}")

            cls._reranker = CrossEncoder(RERANKER_MODEL, device=device, max_length=512)
            logging.getLogger(__name__).info("🔐 Реранкер загружен.")
        return cls._reranker


# === ПРОСТЫЕ ДОСТУПЫ ДЛЯ СОВМЕСТИМОСТИ ===
LLM = LazyLoader()
EMBEDDINGS = LazyLoader()
RERANKER = LazyLoader()


# === ПРОВЕРКА ПУТЕЙ ===
def check_paths():
    for path in [PERSIST_DIR, DB_FILE, KNOWLEDGE_DIR, METADATA_FILE]:
        if not os.path.exists(path):
            logging.warning(f"Путь {path} не существует.")

    # Создаём директории если нет
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    os.makedirs(PERSIST_DIR, exist_ok=True)
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs("./data", exist_ok=True)


check_paths()

# === САНИТИЗАЦИЯ ЛОГОВ ===
import re


def sanitize_log(text: str) -> str:
    """Удалить чувствительные данные из текста перед логированием"""
    if not text:
        return text

    # Паттерны для чувствительных данных
    patterns = [
        (r'password\s*=\s*[\'"][^\'"]+[\'"]', "password=***"),
        (r'passwd\s*=\s*[\'"][^\'"]+[\'"]', "passwd=***"),
        (r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]', "api_key=***"),
        (r'secret\s*=\s*[\'"][^\'"]+[\'"]', "secret=***"),
        (r'token\s*=\s*[\'"][^\'"]+[\'"]', "token=***"),
        (r'bearer\s+[\'"][^\'"]+[\'"]', "bearer ***"),
        (r'authorization:\s*[\'"]?[^\s"\']+[\'"]?', "Authorization: ***"),
        (r'--password\s+[\'"]?[^\s"\']+[\'"]?', "--password ***"),
        (r'-p\s+[\'"]?[^\s"\']+[\'"]?', "-p ***"),
    ]

    sanitized = text
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

    return sanitized


# ===ЦИФРОВОЕ МЕНЮ (цифра -> команда без /)===
# Только команды без параметров или с интерактивными параметрами
NUMERIC_MENU = {
    # Выход
    "0": "exit",
    # Режимы (1-5)
    "1": "teacher",  # Учитель
    "2": "expert",  # Эксперт
    "3": "ctf",  # CTF режим
    "4": "quiz",  # Викторина
    "5": "review",  # Анализ кода
    # Информация & справка (6-13)
    "6": "news",  # Новости
    "7": "achievements",  # Достижения
    "8": "stats",  # Статистика
    "9": "help",  # Справка
    "10": "help detail",  # Подробная справка
    "11": "guide",  # Гайд по VM
    "12": "version",  # Версия приложения
    "13": "menu",  # Показать меню
    # Практика & курсы (14-24) - расширено
    "14": "practice",  # Практика (CTF/HTB)
    "15": "htb",  # HackTheBox интеграция
    "16": "walkthrough",  # Пошаговый разбор эксплойта
    "17": "exploit",  # Поиск эксплойтов
    "18": "lab",  # Docker лаборатории
    "19": "courses",  # Учебные курсы
    "20": "tracks",  # Учебные траектории
    "21": "story",  # Режим истории
    "22": "task",  # Задание
    "23": "genassignment",  # Генератор заданий
    "24": "adaptive",  # Адаптивные слабые темы
    # Управление (25-34)
    "25": "provider",  # Показать провайдера
    "26": "model",  # Показать модель
    "27": "terminal",  # Лог терминала
    "28": "cache stats",  # Статистика кэша
    "29": "clearcache",  # Очистить кэш
    "30": "check",  # Проверить контейнеры
    "31": "history",  # История чата
    "32": "writeup",  # Шаблон writeup
    "33": "add_book",  # Добавить книгу (интерактивно)
    "34": "social",  # Social engineering trainer
    # Разное (35-51)
    "35": "repeat",  # Интервальные повторения
    "36": "summary",  # Генерация конспекта
    "37": "auto_writeup",  # Автоматический writeup
    "38": "flag",  # Проверить флаг (нужен аргумент)
    "39": "log",  # Записать лог
    "40": "set-api-key",  # Установить API ключ
    "41": "smart_test",  # Умный тест (без URL)
    "42": "read_url",  # Чтение URL
    "43": "threats",  # Угрозы
    "44": "groups",  # Группы APT
    "45": "threat summary",  # Сводка угроз
    "46": "cve",  # CVE информация
    "47": "news search",  # Search
    "48": "sandbox",  # Песочница для кода
    "49": "hint",  # Подсказки в реальном времени
    "50": "dashboard",  # Личный дашборд
    "51": "bounty",  # Bug Bounty симуляция
    "52": "analytics",  # Продвинутая аналитика и AI рекомендации
    "53": "voice",  # Голосовой помощник (TTS/STT) (M-34)
    "54": "export",  # Экспорт истории чата (M-30)
    "55": "usage",  # Статистика использования команд (M-31)
    "56": "config",  # Интерактивный мастер настройки (M-28)
    "57": "theme",  # Смена цветовой схемы (M-29)
    "58": "features",  # Управление модулями (M-32)
    "59": "summarize",  # Суммаризация истории (M-22)
    "60": "phishing",  # Конструктор фишинговых писем (M-04)
    "61": "mermaid",  # Mermaid-инфографика (M-09)
    "62": "skills",  # Трекер практических навыков (L-02)
    "63": "reputation",  # Репутация и хэндлы (L-10)
    "64": "depth",  # Глубина объяснений (L-05)
    "65": "fixcode",  # Генерация безопасного кода (L-09)
    "66": "templates",  # YAML шаблоны заданий (L-17)
    "67": "emotions",  # Эмоции учителя (M-19)
    "68": "dockergen",  # Генерация docker-compose (L-06)
    "69": "ctf",  # Динамические CTF-флаги (G-03)
    "70": "profile",  # Профиль пользователя (G-09)
    "71": "daily",  # Ежедневный челлендж со стриком
}


def get_llm():
    """Получить экземпляр LLM (ленивая загрузка)."""
    llm = LazyLoader.get_llm()
    if llm is None:
        return None
    return InstrumentedLLM(llm)


class InstrumentedLLM:
    """Wrapper around LLM to record usage metrics."""

    def __init__(self, llm):
        self._llm = llm

    def invoke(self, prompt, **kwargs):
        from time import perf_counter

        from state import get_state

        start = perf_counter()
        result = self._llm.invoke(prompt, **kwargs)
        duration = perf_counter() - start
        tokens = None
        try:
            if hasattr(result, "usage_metadata"):
                meta = result.usage_metadata
                if isinstance(meta, dict):
                    tokens = meta.get("total_tokens")
                else:
                    tokens = (
                        meta.total_tokens if hasattr(meta, "total_tokens") else None
                    )
            elif hasattr(result, "response_metadata"):
                meta = result.response_metadata
                if isinstance(meta, dict):
                    tokens = meta.get("token_usage", {}).get("total_tokens")
        except Exception:
            tokens = None
        state = get_state()
        state.llm_call_count += 1
        state.llm_total_time += duration
        if tokens is not None:
            state.llm_total_tokens += tokens
        return result

    def __getattr__(self, name):
        return getattr(self._llm, name)

    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)
