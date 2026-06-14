"""
Configuration and LLM provider management.
"""

import os
import logging
from typing import Any, Dict, List, Optional, Type

from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()
logger = logging.getLogger(__name__)

# ---------- LLM Provider Configuration ----------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mixtral-8x7b-instruct")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "local-model")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
PROVIDER_TIMEOUT = int(os.getenv("PROVIDER_TIMEOUT", "30"))
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")


def reload_env() -> None:
    """Reload LLM config from .env file (for dynamic provider/model switching).

    Called by LazyLoader.invalidate() so that provider/model changes from
    the launcher or CLI take effect without restarting the process.
    """
    try:
        from dotenv import dotenv_values

        env = dotenv_values()
    except ImportError:
        logger.warning("reload_env: dotenv_values failed, keeping current values")
        return

    key_map: dict[str, str] = {
        "LLM_PROVIDER": "LLM_PROVIDER",
        "OLLAMA_MODEL": "OLLAMA_MODEL",
        "OLLAMA_URL": "OLLAMA_BASE_URL",
        "LMSTUDIO_MODEL": "LMSTUDIO_MODEL",
        "LMSTUDIO_BASE_URL": "LMSTUDIO_BASE_URL",
        "GROQ_MODEL": "GROQ_MODEL",
        "OPENROUTER_MODEL": "OPENROUTER_MODEL",
        "OPENROUTER_BASE_URL": "OPENROUTER_BASE_URL",
        "MODEL_TEMPERATURE": "TEMPERATURE",
        "MAX_TOKENS": "MAX_TOKENS",
        "PROVIDER_TIMEOUT": "PROVIDER_TIMEOUT",
        "OLLAMA_BASE_URL": "OLLAMA_BASE_URL",
    }

    globs = globals()
    for env_key, cfg_key in key_map.items():
        val = env.get(env_key)
        if val is None or not val.strip():
            continue
        val = val.strip()
        # Update os.environ so os.getenv() calls pick it up too
        os.environ[env_key] = val
        # Update module-level variable (with type casting)
        if cfg_key in ("MAX_TOKENS", "PROVIDER_TIMEOUT"):
            try:
                globs[cfg_key] = int(val)
            except (ValueError, TypeError):
                pass
        elif cfg_key == "TEMPERATURE":
            try:
                globs[cfg_key] = float(val)
            except (ValueError, TypeError):
                pass
        elif cfg_key == "LLM_PROVIDER":
            globs[cfg_key] = val.lower()
        else:
            globs[cfg_key] = val

    logger.debug("reload_env: config refreshed from .env")


# Configurable fallback chain (comma-separated, e.g. "ollama,groq,openrouter,huggingface,mock")
LLM_PROVIDERS_ENV = os.getenv("LLM_PROVIDERS", "")
if LLM_PROVIDERS_ENV:
    FALLBACK_ORDER = [
        p.strip().lower() for p in LLM_PROVIDERS_ENV.split(",") if p.strip()
    ]
else:
    FALLBACK_ORDER = ["ollama", "groq", "openrouter", "huggingface", "mock"]

# Known models per provider (for validation and suggestions)
PROVIDER_KNOWN_MODELS = {
    "ollama": {
        "description": "Локальные модели через Ollama",
        "default": "qwen2.5:7b",
        "suggested": [
            "qwen2.5:7b",
            "qwen2.5:14b",
            "llama3.2:3b",
            "llama3.2:1b",
            "mistral:7b",
            "codellama:7b",
        ],
        "docs_url": "https://ollama.com/library",
    },
    "groq": {
        "description": "Облачные модели Groq (бесплатно, быстро)",
        "default": "mixtral-8x7b-32768",
        "suggested": [
            "mixtral-8x7b-32768",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "gemma2-9b-it",
            "deepseek-coder-6.7b-instruct",
        ],
        "docs_url": "https://console.groq.com/docs/models",
    },
    "openrouter": {
        "description": "Маршрутизатор 100+ моделей (OpenRouter)",
        "default": "mistralai/mixtral-8x7b-instruct",
        "suggested": [
            "meta-llama/llama-3.3-70b-instruct:free",
            "qwen/qwen-2.5-72b-instruct",
            "google/gemma-3-27b-it:free",
            "mistralai/mixtral-8x7b-instruct",
            "deepseek/deepseek-r1:free",
        ],
        "docs_url": "https://openrouter.ai/models",
    },
    "huggingface": {
        "description": "HuggingFace Inference API",
        "default": "mistralai/Mistral-7B-Instruct-v0.2",
        "suggested": [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "meta-llama/Llama-2-70b-chat-hf",
        ],
        "docs_url": "https://huggingface.co/models",
    },
    "mock": {
        "description": "Оффлайн-режим (заглушка, без AI)",
        "default": "mock-llm",
        "suggested": ["mock-llm"],
        "docs_url": "",
    },
    "lmstudio": {
        "description": "Локальная модель через LM Studio (OpenAI-совместимый API)",
        "default": "local-model",
        "suggested": ["local-model"],
        "docs_url": "",
    },
}

# ---------- RAG / Knowledge Base Configuration ----------
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "./knowledge_base")
DOCS_DIR = os.getenv("DOCS_DIR", "./docs")
PERSIST_DIR = os.getenv("PERSIST_DIR", "./embeddings")
METADATA_FILE = os.getenv("METADATA_FILE", "./embeddings/metadata.json")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "2"))
RERANKER = os.getenv("RERANKER", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANK_TOP_K = int(os.getenv("RERANK_TOP_K", "5"))
BM25_ENABLED = os.getenv("BM25_ENABLED", "true").lower() == "true"
BM25_K = int(os.getenv("BM25_K", "2"))


# ---------- Security & Logging ----------
def sanitize_log(text: str) -> str:
    """Remove sensitive information from logs."""
    # Простейшая заглушка
    return text


# ---------- Other Configuration ----------
NUMERIC_MENU: Dict[str, str] = {
    "0": "exit",
    "1": "teacher",
    "2": "expert",
    "3": "ctf",
    "4": "quiz",
    "5": "review",
    "6": "news",
    "7": "achievements",
    "8": "stats",
    "9": "help",
    "10": "help detail",
    "11": "guide",
    "12": "version",
    "13": "menu",
    "14": "practice",
    "15": "htb",
    "16": "walkthrough",
    "17": "exploit",
    "18": "lab",
    "19": "courses",
    "20": "tracks",
    "21": "story",
    "22": "task",
    "23": "genassignment",
    "24": "adaptive",
    "25": "provider",
    "26": "model",
    "27": "terminal",
    "28": "cache stats",
    "29": "clearcache",
    "30": "check",
    "31": "history",
    "32": "writeup",
    "33": "add_book",
    "34": "social",
    "35": "repeat",
    "36": "summary",
    "37": "auto_writeup",
    "38": "flag",
    "39": "log",
    "40": "set-api-key",
    "41": "smart_test",
    "42": "read_url",
    "43": "threats",
    "44": "groups",
    "45": "threat summary",
    "46": "cve",
    "47": "news search",
    "48": "sandbox",
    "49": "hint",
    "50": "dashboard",
    "51": "bounty",
    "52": "analytics",
    "53": "voice",
    "54": "export",
    "55": "usage",
    "56": "config",
    "57": "theme",
    "58": "lang",
    "59": "features",
    "60": "summarize",
    "61": "phishing",
    "62": "mermaid",
    "63": "skills",
    "64": "reputation",
    "65": "depth",
    "66": "fixcode",
    "67": "templates",
    "68": "emotions",
    "69": "dockergen",
    "70": "ctf",
    "71": "profile",
    "72": "daily",
}
THINKING_ENABLED = True
SOCRATIC_ENABLED = True

# Пути к файлам
ACHIEVEMENTS_FILE = os.getenv("ACHIEVEMENTS_FILE", "./data/achievements.json")
SHOP_ITEMS_FILE = os.getenv("SHOP_ITEMS_FILE", "./data/shop_items.json")

# Прочие переменные, на которые ругался mypy
HF_MODEL = HUGGINGFACE_MODEL
HF_TOKEN = HUGGINGFACE_API_KEY
LLM: Any = None  # будет установлен через LazyLoader


def _get_secret(key: Optional[str]) -> Optional[SecretStr]:
    """Convert plain string key to SecretStr."""
    if key is None:
        return None
    return SecretStr(key)


def get_llm() -> Optional[Any]:
    """Initialize and return the configured LLM based on provider."""
    if LLM_PROVIDER == "openrouter":
        if not OPENROUTER_API_KEY:
            logger.warning("OpenRouter API key missing")
            return None
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            logger.error("langchain-openai not installed")
            return None
        return ChatOpenAI(  # type: ignore[call-arg]
            api_key=_get_secret(OPENROUTER_API_KEY),
            model=OPENROUTER_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            base_url=OPENROUTER_BASE_URL,
        )
    elif LLM_PROVIDER == "groq":
        if not GROQ_API_KEY:
            logger.warning("Groq API key missing")
            return None
        try:
            from langchain_groq import ChatGroq
        except ImportError:
            logger.error("langchain-groq not installed")
            return None
        return ChatGroq(
            api_key=_get_secret(GROQ_API_KEY),
            model=GROQ_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    elif LLM_PROVIDER == "huggingface":
        if not HUGGINGFACE_API_KEY:
            logger.warning("HuggingFace API key missing")
            return None
        try:
            from langchain_community.llms import HuggingFaceEndpoint
        except ImportError:
            logger.error("langchain-community not installed")
            return None
        return HuggingFaceEndpoint(
            endpoint_url=f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
            huggingfacehub_api_token=_get_secret(HUGGINGFACE_API_KEY),
            task="text-generation",
            temperature=TEMPERATURE,
            max_new_tokens=MAX_TOKENS,
        )
    elif LLM_PROVIDER == "ollama":
        try:
            from langchain_ollama import OllamaLLM
        except ImportError:
            logger.error("langchain-ollama not installed")
            return None
        return OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=TEMPERATURE,
            num_predict=MAX_TOKENS,
        )
    elif LLM_PROVIDER == "lmstudio":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            logger.error("langchain-openai not installed (needed for LM Studio)")
            return None
        return ChatOpenAI(  # type: ignore[call-arg]
            api_key=_get_secret("not-needed"),
            model=LMSTUDIO_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            base_url=LMSTUDIO_BASE_URL,
        )
    elif LLM_PROVIDER == "mock":
        try:
            from mock_llm import MockLLM

            return MockLLM()
        except ImportError:
            logger.error("mock_llm.py not found")
            return None
    else:
        logger.error(f"Unknown LLM provider: {LLM_PROVIDER}")
        return None


def _get_fallback_llms() -> list:
    """Create LLM instances for available providers (excluding current primary)."""
    fallbacks = []
    original_provider = LLM_PROVIDER
    for provider in FALLBACK_ORDER:
        if provider == original_provider:
            continue
        try:
            import config as _cfg

            _cfg.LLM_PROVIDER = provider
            llm = get_llm()
            if llm is not None:
                fallbacks.append(llm)
        except (ImportError, ValueError, RuntimeError):
            pass
    # Restore original provider
    import config as _cfg

    _cfg.LLM_PROVIDER = original_provider
    return fallbacks


class LazyLoader:
    """Lazy loader for LLM, embeddings, reranker to avoid import delays."""

    _llm: Optional[Any] = None
    _embeddings: Optional[Any] = None
    _reranker: Optional[Any] = None

    @classmethod
    def get_llm(cls) -> Optional[Any]:
        if cls._llm is None:
            primary = get_llm()
            fallbacks = _get_fallback_llms()

            # Build ResilientLLM with primary + fallbacks
            # If primary is None, use MockLLM as primary
            if primary is None and not fallbacks:
                try:
                    from mock_llm import MockLLM

                    cls._llm = MockLLM()
                    logger.info(
                        "No LLM providers available — using MockLLM (offline mode)"
                    )
                except ImportError:
                    logger.error("No LLM providers and MockLLM not available")
                    return None
            elif primary is not None:
                try:
                    from resilient_llm import ResilientLLM

                    # Always add MockLLM as last fallback if not already in chain
                    has_mock = any(
                        getattr(f, "model", "") == "mock-llm" for f in fallbacks
                    )
                    if not has_mock:
                        try:
                            from mock_llm import MockLLM

                            fallbacks.append(MockLLM())
                        except ImportError:
                            pass
                    cls._llm = ResilientLLM(primary=primary, fallbacks=fallbacks)
                    logger.info(
                        f"ResilientLLM: primary={LLM_PROVIDER}, "
                        f"fallbacks={[getattr(f, 'model', '?') for f in fallbacks]}"
                    )
                except ImportError:
                    cls._llm = primary
                    logger.warning("resilient_llm not available, using single provider")
            else:
                # Primary is None but fallbacks exist
                if fallbacks:
                    cls._llm = fallbacks[0]
                else:
                    try:
                        from mock_llm import MockLLM

                        cls._llm = MockLLM()
                    except ImportError:
                        return None

            global LLM
            LLM = cls._llm
        return cls._llm

    @classmethod
    def invalidate(cls) -> None:
        """Invalidate cached LLM (for provider switching or failure recovery).
        Also reloads .env so launcher/CLI changes take effect immediately.
        """
        reload_env()
        cls._llm = None
        global LLM
        LLM = None

    @classmethod
    def get_embeddings(cls) -> Optional[Any]:
        if cls._embeddings is None:
            try:
                from langchain_huggingface import HuggingFaceEmbeddings

                cls._embeddings = HuggingFaceEmbeddings(
                    model_name="intfloat/multilingual-e5-small",
                    model_kwargs={"device": "cpu"},
                )
            except ImportError:
                logger.warning(
                    "sentence-transformers not installed, embeddings disabled"
                )
                cls._embeddings = None
        return cls._embeddings

    @classmethod
    def get_reranker(cls) -> Optional[Any]:
        if cls._reranker is None and RERANKER:
            try:
                from sentence_transformers import CrossEncoder

                cls._reranker = CrossEncoder(RERANKER)
            except ImportError:
                logger.warning("sentence-transformers not installed, reranker disabled")
                cls._reranker = None
        return cls._reranker


# Для обратной совместимости (функция, чтобы всегда отдавать актуальное значение)
def get_model_name() -> str:
    if LLM_PROVIDER == "ollama":
        return OLLAMA_MODEL
    elif LLM_PROVIDER == "groq":
        return GROQ_MODEL
    elif LLM_PROVIDER == "lmstudio":
        return LMSTUDIO_MODEL
    elif LLM_PROVIDER == "huggingface":
        return HUGGINGFACE_MODEL
    elif LLM_PROVIDER == "openrouter":
        return OPENROUTER_MODEL
    elif LLM_PROVIDER == "mock":
        return "mock-llm"
    return OLLAMA_MODEL


MODEL_NAME = get_model_name()
