"""
🔐 Конфигурация CyberTeacher
"""

import os
import sys
import logging

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

# === OLLAMA ===
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:7b"  # Баланс скорости и качества
MODEL_TEMPERATURE = 0.3

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# === ОПТИМИЗАЦИЯ ===
MAX_WORKERS = 16
CHUNK_SIZE = 800
CHUNK_OVERLAP = 50

# === ПЕДАГОГИКА ===
SOCRATIC_ENABLED = True
THINKING_ENABLED = True

# === LAZY LOADING (Оптимизация) ===
class LazyLoader:
    """Ленивая загрузка моделей - загружаются только при первом использовании"""
    
    _llm = None
    _embeddings = None
    _embedding_model = None
    
    @classmethod
    def get_llm(cls):
        if cls._llm is None:
            import logging
            logging.getLogger(__name__).info("🔐 Загрузка модели LLM (Ollama через curl)...")
            
            from ollama_client import OllamaClient
            cls._llm = OllamaClient()
            logging.getLogger(__name__).info("🔐 LLM загружена (Ollama).")
        return cls._llm
    
    @classmethod
    def get_embeddings(cls):
        if cls._embeddings is None:
            import logging
            logging.getLogger(__name__).info("🔐 Загрузка модели эмбеддингов...")
            from sentence_transformers import SentenceTransformer
            
            # Оптимизация: использовать локальную модель если есть
            cls._embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            
            class SentenceTransformerWrapper:
                def __init__(self, model):
                    self.model = model
                
                def embed_documents(self, texts):
                    return self.model.encode(texts, show_progress_bar=False).tolist()
                
                def embed_query(self, text):
                    return self.model.encode([text], show_progress_bar=False)[0].tolist()
            
            cls._embeddings = SentenceTransformerWrapper(cls._embedding_model)
            logging.getLogger(__name__).info("🔐 Эмбеддинги загружены.")
        return cls._embeddings

# === ПРОСТЫЕ ДОСТУПЫ ДЛЯ СОВМЕСТИМОСТИ ===
LLM = LazyLoader()
EMBEDDINGS = LazyLoader()

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
