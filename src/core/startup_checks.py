import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

DEPENDENCIES: List[Tuple[str, str, str]] = [
    ("faiss", "faiss-cpu", "pip install faiss-cpu"),
    ("chromadb", "chromadb", "pip install chromadb"),
    ("sentence_transformers", "sentence-transformers", "pip install sentence-transformers"),
    ("fastapi", "fastapi", "pip install fastapi"),
    ("uvicorn", "uvicorn", "pip install uvicorn"),
    ("rich", "rich", "pip install rich"),
    ("sqlalchemy", "sqlalchemy", "pip install sqlalchemy"),
    ("pydantic", "pydantic", "pip install pydantic"),
    ("aiohttp", "aiohttp", "pip install aiohttp"),
]


def check_dependencies() -> bool:
    """Проверяет наличие необходимых и опциональных зависимостей.

    Возвращает True, если все зависимости найдены, иначе False.
    """
    missing: List[Tuple[str, str]] = []

    for module_name, _package_name, install_cmd in DEPENDENCIES:
        try:
            __import__(module_name)
            logger.info(f"[OK] Found module: {module_name}")
        except ImportError:
            logger.warning(
                f"[WARN] Missing module: {module_name}. Install with: {install_cmd}"
            )
            missing.append((module_name, install_cmd))

    if missing:
        print("\n" + "=" * 50)
        print("[WARN]  WARNING: Some dependencies are missing:")
        for name, cmd in missing:
            print(f"   - {name}: {cmd}")
        print("=" * 50 + "\n")
        return False

    return True
