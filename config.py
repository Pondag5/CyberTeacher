"""
🔐 Конфигурация CyberTeacher
"""

import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

# === ЛОГИРОВАНИЕ ===
LOG_FILE = "./cyberteacher.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
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
LLM_PROVIDER = "openrouter"  # Переключаем на облако с большим контекстом

# === OLLAMA ===
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"
MODEL_TEMPERATURE = 0.3

# === OPENROUTER (если LLM_PROVIDER="openrouter") ===
OPENROUTER_URL = "https://openrouter.ai/api/v1"
# Бесплатные модели с большим контекстом:
# - "nvidia/nemotron-3-nano-30b-a3b:free" - 256K контекст, 30B, бесплатно
# - "mistralai/mixtral-8x7b-instruct" - 32K, бесплатно
OPENROUTER_MODEL = "stepfun/step-3.5-flash:free"
# Получите API ключ на https://openrouter.ai/keys
OPENROUTER_API_KEY = ""  # Заполните или установите через env: OPENROUTER_API_KEY

# Общее имя модели (логирование)
MODEL_NAME = OLLAMA_MODEL if LLM_PROVIDER == "ollama" else OPENROUTER_MODEL

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# === ОПТИМИЗАЦИЯ ===
MAX_WORKERS = 8   # Уменьшили для снижения нагрузки
CHUNK_SIZE = 600  # Оптимально для технической документации (было 300)
CHUNK_OVERLAP = 50  # Сохраняем контекст между чанками (было 15)

# === ПЕДАГОГИКА ===
SOCRATIC_ENABLED = True
THINKING_ENABLED = True

# === RERANKING ===
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 5  # Сколько лучших чанков возвращать после реранкинга

# === КЭШИРОВАНИЕ ===
RESPONSE_CACHE_SIZE = 100  # LRU кэш для ответов LLM

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
            logging.getLogger(__name__).info(f"🔐 Загрузка модели LLM ({LLM_PROVIDER})...")
            
            if LLM_PROVIDER == "ollama":
                from langchain_openai import ChatOpenAI
                cls._llm = ChatOpenAI(
                    model=OLLAMA_MODEL,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OLLAMA_URL + "/v1",
                    api_key=None  # Ollama doesn't require API key
                )
            elif LLM_PROVIDER == "openrouter":
                from langchain_openai import ChatOpenAI
                # OpenRouter требует api_key
                api_key = OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY", "")
                if not api_key:
                    raise ValueError("OPENROUTER_API_KEY не установлен")
                cls._llm = ChatOpenAI(
                    model=OPENROUTER_MODEL,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OPENROUTER_URL,
                    api_key=api_key if api_key else None
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
            from langchain_huggingface import HuggingFaceEmbeddings
            import torch
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            logging.getLogger(__name__).info(f"🔐 Используется устройство: {device}")
            
            cls._embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': device}
            )
            logging.getLogger(__name__).info("🔐 Эмбеддинги загружены.")
        return cls._embeddings
    
    @classmethod
    def get_reranker(cls):
        if cls._reranker is None:
            import logging
            logging.getLogger(__name__).info("🔐 Загрузка модели реранкера...")
            from sentence_transformers import CrossEncoder
            import torch
            
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            logging.getLogger(__name__).info(f"🔐 Используется устройство: {device}")
            
            cls._reranker = CrossEncoder(
                RERANKER_MODEL,
                device=device,
                max_length=512
            )
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
