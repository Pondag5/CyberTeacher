"""Асинхронные обработчики (H-16).

Параллельные запросы: RAG + LLM одновременно для скорости ответа.
"""

import asyncio
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


async def async_rag_search(query: str, knowledge_base: Any) -> str | None:
    """Асинхронный поиск в RAG базе."""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, knowledge_base.get_relevant_docs, query)
        return result
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        return None


async def async_llm_call(llm: Any, prompt: str) -> str | None:
    """Асинхронный вызов LLM."""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, llm.invoke, prompt)
        return result
    except Exception as e:
        logger.error(f"LLM call error: {e}")
        return None


async def async_combined_query(query: str, llm: Any, knowledge_base: Any) -> dict[str, Any]:
    """Параллельный запрос: RAG + LLM одновременно.

    Returns:
        Dict с ключами 'rag_result', 'llm_result', 'combined_response'.
    """
    rag_task = asyncio.create_task(async_rag_search(query, knowledge_base))
    llm_task = asyncio.create_task(async_llm_call(llm, query))

    rag_result, llm_result = await asyncio.gather(rag_task, llm_task, return_exceptions=True)

    combined = ""
    if rag_result and not isinstance(rag_result, Exception):
        combined += f"[RAG]: {rag_result}\n\n"
    if llm_result and not isinstance(llm_result, Exception):
        combined += f"[LLM]: {llm_result}"

    return {
        "rag_result": rag_result if not isinstance(rag_result, Exception) else None,
        "llm_result": llm_result if not isinstance(llm_result, Exception) else None,
        "combined_response": combined,
    }


def run_async_query(query: str, llm: Any, knowledge_base: Any) -> dict[str, Any]:
    """Обёртка для запуска асинхронного запроса из синхронного кода."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Уже в event loop (например, в Jupyter)
            return asyncio.run(async_combined_query(query, llm, knowledge_base))
        return loop.run_until_complete(async_combined_query(query, llm, knowledge_base))
    except RuntimeError:
        return asyncio.run(async_combined_query(query, llm, knowledge_base))
