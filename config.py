"""
🔐 Конфигурация CyberTeacher
"""

import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# === ЛОГИРОВАНИЕ ===
LOG_FILE = "./cyberteacher.log"
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
    # Отключаем форсирование цветов - используем простой вывод
    # os.environ["TERM"] = "dumb"

# === ПУТИ ===
PERSIST_DIR = "./embeddings"
DB_FILE = "./memory/chat_history.db"
KNOWLEDGE_DIR = "./knowledge_base"
METADATA_FILE = "./embeddings/metadata.json"

# === LLM ПРОВАЙДЕР ===
# Варианты: "ollama" (локально), "openrouter" (облако)
LLM_PROVIDER = "ollama"  # Локально, бесплатно

# === OLLAMA ===
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"
MODEL_TEMPERATURE = 0.3

# === OPENROUTER (если LLM_PROVIDER="openrouter") ===
OPENROUTER_URL = "https://openrouter.ai/api/v1"
# Бесплатные модели с большим контекстом:
# - "nvidia/nemotron-3-nano-30b-a3b:free" - 256K контекст, 30B, бесплатно
# - "mistralai/mixtral-8x7b-instruct" - 32K, бесплатно
OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
# Получите API ключ на https://openrouter.ai/keys
OPENROUTER_API_KEY = ""  # Заполните или установите через env: OPENROUTER_API_KEY

# Общее имя модели (логирование)
MODEL_NAME = OLLAMA_MODEL if LLM_PROVIDER == "ollama" else OPENROUTER_MODEL

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# === ОПТИМИЗАЦИЯ ===
MAX_WORKERS = 8  # Уменьшили для снижения нагрузки
CHUNK_SIZE = 600  # Оптимально для технической документации (было 300)
CHUNK_OVERLAP = 50  # Сохраняем контекст между чанками (было 15)

# === HUGGINGFACE INFERENCE API (бесплатно 10k токенов/день) ===
HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Бесплатная мощная модель
HF_API_URL = "https://api-inference.huggingface.co/models"

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

                api_key = os.getenv("OPENROUTER_API_KEY")
                if not api_key:
                    raise ValueError("OPENROUTER_API_KEY не установлен")
                cls._llm = ChatOpenAI(
                    model=OPENROUTER_MODEL,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OPENROUTER_URL,
                    api_key=api_key,
                    max_tokens=MAX_TOKENS,
                )
            elif LLM_PROVIDER == "huggingface":
                from langchain_huggingface import HuggingFaceEndpoint

                hf_token = os.getenv("HF_TOKEN")
                if not hf_token:
                    raise ValueError("HF_TOKEN не установлен")
                cls._llm = HuggingFaceEndpoint(
                    repo_id=HF_MODEL,
                    huggingfacehub_api_token=hf_token,
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
    import logging

    for path in [PERSIST_DIR, DB_FILE, KNOWLEDGE_DIR, METADATA_FILE]:
        if not os.path.exists(path):
            logging.warning(f"Путь {path} не существует.")

    # Создаём директории если нет
    os.makedirs("./memory", exist_ok=True)
    os.makedirs("./embeddings", exist_ok=True)


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
    # Режимы (1-5)
    "1": "teacher",  # Учитель
    "2": "expert",  # Эксперт
    "3": "ctf",  # CTF режим
    "4": "quiz",  # Викторина
    "5": "review",  # Анализ кода
    # Информация & справка (6-14)
    "6": "news",  # Новости
    "7": "achievements",  # Достижения
    "8": "stats",  # Статистика
    "9": "help",  # Справка
    "10": "help detail",  # Подробная справка
    "11": "guide",  # Гайд по VM
    "12": "version",  # Версия приложения
    "13": "menu",  # Показать меню
    # Практика & курсы (15-19)
    "14": "practice",  # Практика (CTF/HTB)
    "15": "lab",  # Docker лаборатории (status)
    "16": "courses",  # Учебные курсы
    "17": "story",  # Режим истории
    "18": "task",  # Задание
    "19": "genassignment",  # Генератор заданий
    # Управление (20-29)
    "20": "provider",  # Показать провайдера
    "21": "model",  # Показать модель
    "22": "terminal",  # Лог терминала
    "23": "cache stats",  # Статистика кэша
    "24": "clearcache",  # Очистить кэш
    "25": "check",  # Проверить контейнеры
    "26": "history",  # История чата
    "27": "writeup",  # Шаблон writeup
    "28": "add_book",  # Добавить книгу (интерактивно)
    "29": "social",  # Social engineering trainer
    # Разное (30-39)
    "30": "flag",  # Проверить флаг (нужен аргумент)
    "31": "log",  # Записать лог
    "32": "set-api-key",  # Установить API ключ
    "33": "smart_test",  # Умный тест (без URL)
    "34": "read_url",  # Чтение URL
    "35": "threats",  # Угрозы
    "36": "groups",  # Группы APT
    "37": "threat summary",  # Сводка угроз
    "38": "cve",  # CVE информация
    "39": "news search",  # Search
    "40": "sandbox",  # Песочница для кода
    "41": "adaptive",  # Адаптивные слабые темы
    "42": "repeat",  # Интервальные повторения
    "43": "summary",  # Генерация конспекта
    "44": "auto_writeup",  # Автоматический writeup
    # Выход (0)
    "0": "exit",  # Выход
}


def get_llm():
    """Получить экземпляр LLM (ленивая загрузка)."""
    return LazyLoader.get_llm()
