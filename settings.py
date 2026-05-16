"""
Типизированная конфигурация с валидацией через Pydantic Settings.
"""

from pathlib import Path
from typing import Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Глобальные настройки приложения с валидацией."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # === Пути ===
    persist_dir: Path = Field(default=Path("./embeddings"))
    db_file: Path = Field(default=Path("./memory/chat_history.db"))
    knowledge_dir: Path = Field(default=Path("./knowledge_base"))
    metadata_file: Path = Field(default=Path("./embeddings/metadata.json"))
    state_file: Path = Field(default=Path("./memory/app_state.json"))
    achievements_file: Path = Field(default=Path("./data/achievements.json"))
    log_file: Path = Field(default=Path("./cyberteacher.log"))
    response_cache_file: Path = Field(default=Path("./memory/response_cache.json"))

    # === LLM ===
    llm_provider: Literal["ollama", "openrouter", "huggingface"] = Field(
        default="ollama"
    )
    ollama_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="qwen2.5:7b")
    openrouter_url: str = Field(default="https://openrouter.ai/api/v1")
    openrouter_model: str = Field(default="meta-llama/llama-3.3-70b-instruct:free")
    openrouter_api_key: str = Field(default="")
    hf_model: str = Field(default="mistralai/Mixtral-8x7B-Instruct-v0.1")
    hf_api_url: str = Field(default="https://api-inference.huggingface.co/models")
    hf_token: str = Field(default="")
    model_temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, gt=0)
    embedding_model: str = Field(default="all-MiniLM-L6-v2")
    reranker_model: str = Field(default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    rerank_top_k: int = Field(default=5, gt=0)

    # === Оптимизация ===
    max_workers: int = Field(default=8, gt=0)
    chunk_size: int = Field(default=600, gt=0)
    chunk_overlap: int = Field(default=50, ge=0)
    response_cache_size: int = Field(default=100, gt=0)

    # === Педагогика ===
    socratic_enabled: bool = Field(default=True)
    thinking_enabled: bool = Field(default=True)

    # === BM25 ===
    bm25_enabled: bool = Field(default=True)
    bm25_k: int = Field(default=20, gt=0)

    @field_validator("openrouter_api_key", "hf_token", mode="after")
    @classmethod
    def warn_empty_keys(cls, v: str, info) -> str:
        if not v and info.field_name in ("openrouter_api_key", "hf_token"):
            pass  # Предупреждение будет при использовании
        return v

    @property
    def model_name(self) -> str:
        """Текущее имя модели для логирования."""
        if self.llm_provider == "ollama":
            return self.ollama_model
        elif self.llm_provider == "openrouter":
            return self.openrouter_model
        return self.hf_model

    def ensure_dirs(self) -> None:
        """Создать необходимые директории."""
        for path in [
            self.persist_dir,
            self.db_file.parent,
            self.knowledge_dir,
            self.state_file.parent,
            self.achievements_file.parent,
            self.response_cache_file.parent,
        ]:
            path.mkdir(parents=True, exist_ok=True)


# Глобальный экземпляр (ленивая инициализация)
_settings: Settings | None = None


def get_settings() -> Settings:
    """Получить настройки приложения (синглтон)."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_dirs()
    return _settings


def reset_settings() -> None:
    """Сбросить настройки (для тестов)."""
    global _settings
    _settings = None
