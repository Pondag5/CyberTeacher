# knowledge.py - RAG and knowledge base management

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, List, Optional

from config import (
    BM25_ENABLED,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCS_DIR,
    KNOWLEDGE_DIR,
    PERSIST_DIR,
    RERANK_TOP_K,
    LazyLoader,
)

logger = logging.getLogger(__name__)

# Глобальная переменная для текущего вектора (кеш)
_current_vectordb: Any = None

# Cache for directory file listings (invalidated every 60s)
_file_list_cache: Dict[str, Any] = {"timestamp": 0.0, "files": []}
_FILE_CACHE_TTL = 60


# ----------------------------------------------------------------------
# BM25 utils (only if enabled and installed)
# ----------------------------------------------------------------------
if BM25_ENABLED:
    try:
        import jieba
        from rank_bm25 import BM25Okapi
    except ImportError:
        jieba = None  # type: ignore
        BM25Okapi = None  # type: ignore
        logger.warning("jieba or rank_bm25 not installed, BM25 disabled")
        BM25_ENABLED = False
else:
    jieba = None  # type: ignore
    BM25Okapi = None  # type: ignore


def _chinese_tokenizer(text: str) -> List[str]:
    """Tokenize Chinese text using jieba if available."""
    if jieba is not None:
        return jieba.lcut(text)
    return text.split()


class ProgressEmbeddings:
    """Embeddings wrapper with progress tracking (batch-optimized)."""

    def __init__(self, embeddings, total_docs: int):
        self.embeddings = embeddings
        self.total_docs = total_docs
        self.processed = 0

    def embed_documents(self, texts):
        self.processed = 0
        # Use batch embedding (HuggingFaceEmbeddings supports this natively)
        result = self.embeddings.embed_documents(texts)
        self.processed = len(texts)
        return result

    def embed_query(self, text):
        return self.embeddings.embed_query(text)


class BM25Retriever:
    """Simple BM25 retriever for hybrid search."""

    def __init__(self, documents, tokenizer=None):
        if BM25Okapi is None:
            raise RuntimeError("rank_bm25 not installed")
        self.documents = documents
        tokenized = [tokenizer(doc) for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def get_top_n(self, query: str, n: int = 5) -> List[int]:
        import numpy as np

        tokens = _chinese_tokenizer(query) if BM25_ENABLED else query.split()
        scores = self.bm25.get_scores(tokens)
        top_indices = np.argsort(scores)[::-1][:n]
        return top_indices.tolist()


def load_and_split_file(file_path: str):
    """Load a file and split into chunks."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import PyPDFLoader, TextLoader

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    return text_splitter.split_documents(documents)


def _list_supported_files(directories: List[str]) -> List[str]:
    """List all supported files from directories with caching."""
    global _file_list_cache
    now = time.time()
    if now - _file_list_cache["timestamp"] < _FILE_CACHE_TTL:
        return _file_list_cache["files"]
    files: List[str] = []
    for directory in directories:
        if not os.path.exists(directory):
            continue
        for root, _, filenames in os.walk(directory):
            for f in filenames:
                if f.endswith((".pdf", ".txt", ".md")):
                    files.append(os.path.join(root, f))
    _file_list_cache = {"timestamp": now, "files": files}
    return files


_INDEX_TIMESTAMP: float = 0.0


def reindex_if_needed() -> bool:
    """Check if source files changed since last index and rebuild if so. Returns True if rebuilt."""
    global _INDEX_TIMESTAMP
    if not _INDEX_TIMESTAMP:
        return False
    latest_mtime = _INDEX_TIMESTAMP
    for src_dir in (KNOWLEDGE_DIR, DOCS_DIR):
        if not os.path.exists(src_dir):
            continue
        for root, _, files in os.walk(src_dir):
            for f in files:
                if f.endswith((".pdf", ".txt", ".md")):
                    mtime = os.path.getmtime(os.path.join(root, f))
                    if mtime > latest_mtime:
                        latest_mtime = mtime
    if latest_mtime > _INDEX_TIMESTAMP:
        logger.info("Source files changed, rebuilding FAISS index")
        result = load_knowledge_base()
        return result is not None
    return False


def _load_docs_from_dir(directory: str):
    """Load all supported documents from a directory tree."""
    docs = []
    if not os.path.exists(directory):
        logger.debug(f"Directory does not exist: {directory}")
        return docs
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".pdf", ".txt", ".md")):
                path = os.path.join(root, file)
                try:
                    docs.extend(load_and_split_file(path))
                except Exception as e:
                    logger.error(f"Error loading {path}: {e}")
    return docs


def load_knowledge_base():
    """Load or create FAISS vector store from knowledge_base and docs directories."""
    from langchain_community.vectorstores import FAISS

    global _current_vectordb
    embeddings = LazyLoader.get_embeddings()
    if embeddings is None:
        logger.error("Embeddings not available, cannot load knowledge base")
        return None

    # Try to load existing index
    if os.path.exists(PERSIST_DIR):
        try:
            vectordb = FAISS.load_local(
                PERSIST_DIR, embeddings, allow_dangerous_deserialization=True
            )
            _current_vectordb = vectordb
            _INDEX_TIMESTAMP = time.time()
            logger.info(f"Loaded existing FAISS index from {PERSIST_DIR}")
            return vectordb
        except Exception as e:
            logger.warning(f"Failed to load existing index: {e}")
            try:
                import shutil

                shutil.rmtree(PERSIST_DIR)
                logger.info(f"Cleaned up corrupted index at {PERSIST_DIR}")
            except Exception as cleanup_err:
                logger.warning(f"Failed to clean up index: {cleanup_err}")

    source_dirs = [KNOWLEDGE_DIR, DOCS_DIR]
    all_docs = []
    for src_dir in source_dirs:
        dir_docs = _load_docs_from_dir(src_dir)
        logger.info(f"Loaded {len(dir_docs)} chunks from {src_dir}")
        all_docs.extend(dir_docs)

    if not all_docs:
        logger.warning("No documents loaded from any source directory")
        return None

    progress_emb = ProgressEmbeddings(embeddings, len(all_docs))
    vectordb = FAISS.from_documents(all_docs, progress_emb)
    os.makedirs(PERSIST_DIR, exist_ok=True)
    vectordb.save_local(PERSIST_DIR)
    _current_vectordb = vectordb
    _INDEX_TIMESTAMP = time.time()
    logger.info(f"Created and saved FAISS index with {len(all_docs)} chunks")
    return vectordb


def get_current_vectordb():
    """Return the current vector database instance."""
    global _current_vectordb
    return _current_vectordb


# LRU cache for KB queries (avoid repeated FAISS searches)
_kb_query_cache: Dict[str, Any] = {}
_KB_CACHE_MAX = 50


def _kb_cache_key(vectordb, query: str, top_k: int) -> str:
    return f"{id(vectordb)}:{query}:{top_k}"


def _get_kb_cache(vectordb, query: str, top_k: int):
    key = _kb_cache_key(vectordb, query, top_k)
    if key in _kb_query_cache:
        val = _kb_query_cache.pop(key)
        _kb_query_cache[key] = val
        return val
    return None


def _set_kb_cache(vectordb, query: str, top_k: int, result):
    key = _kb_cache_key(vectordb, query, top_k)
    _kb_query_cache[key] = result
    if len(_kb_query_cache) > _KB_CACHE_MAX:
        oldest = next(iter(_kb_query_cache))
        del _kb_query_cache[oldest]


def clear_kb_cache():
    """Clear the KB query cache (call after adding new documents)."""
    _kb_query_cache.clear()


def get_relevant_docs(vectordb, query: str, top_k: int = RERANK_TOP_K):
    """Retrieve relevant documents using hybrid search (FAISS + optional BM25 + reranker)."""
    if vectordb is None:
        return []

    cached = _get_kb_cache(vectordb, query, top_k)
    if cached is not None:
        return cached

    # Step 1: FAISS similarity search (get more candidates for reranking)
    faiss_docs = vectordb.similarity_search(query, k=top_k * 2)

    # Step 2: BM25 (if enabled)
    if BM25_ENABLED:
        all_texts = [doc.page_content for doc in faiss_docs]
        bm25 = BM25Retriever(all_texts, tokenizer=_chinese_tokenizer)
        bm25_indices = bm25.get_top_n(query, n=top_k)
        bm25_docs = [faiss_docs[i] for i in bm25_indices if i < len(faiss_docs)]
        combined = {doc.page_content: doc for doc in (bm25_docs + faiss_docs)}
        candidates = list(combined.values())
    else:
        candidates = faiss_docs

    # Step 3: Cross-encoder reranking
    reranker = LazyLoader.get_reranker()
    if reranker is not None:
        pairs = [(query, doc.page_content) for doc in candidates]
        scores = reranker.predict(pairs)
        scored = list(zip(scores, candidates))
        scored.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc for _, doc in scored[:top_k]]
    else:
        top_docs = candidates[:top_k]

    _set_kb_cache(vectordb, query, top_k, top_docs)
    return top_docs


def add_pdf_to_knowledge_base(pdf_path: str) -> bool:
    """
    Добавляет один PDF-файл в базу знаний (переиндексация).
    Возвращает True при успехе, иначе False.
    """
    global _current_vectordb, _file_list_cache
    try:
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            return False

        # Загружаем и разбиваем документ
        docs = load_and_split_file(pdf_path)
        if not docs:
            logger.warning(f"No chunks extracted from {pdf_path}")
            return False

        # Получаем текущий vectordb или создаём новый
        vectordb = get_current_vectordb()
        if vectordb is None:
            vectordb = load_knowledge_base()

        if vectordb is None:
            from langchain_community.vectorstores import FAISS

            # Создаём новый с нуля
            embeddings = LazyLoader.get_embeddings()
            if embeddings is None:
                logger.error("No embeddings available")
                return False
            vectordb = FAISS.from_documents(docs, embeddings)
        else:
            # Добавляем документы в существующий индекс
            vectordb.add_documents(docs)

        # Сохраняем и сбрасываем кеш списка файлов + кеш запросов
        os.makedirs(PERSIST_DIR, exist_ok=True)
        vectordb.save_local(PERSIST_DIR)
        _current_vectordb = vectordb
        _INDEX_TIMESTAMP = time.time()
        _file_list_cache = {"timestamp": 0.0, "files": []}
        clear_kb_cache()
        logger.info(f"Successfully added {pdf_path} to knowledge base")
        return True

    except Exception as e:
        logger.error(f"Failed to add PDF {pdf_path}: {e}")
        return False


def get_knowledge_status() -> Dict[str, Any]:
    """Return status of knowledge base: files on disk, files in index, chunks, etc."""
    result: Dict[str, Any] = {
        "files_on_disk": 0,
        "files_in_db": 0,
        "total_chunks": 0,
        "list": [],
        "vectordb": get_current_vectordb(),
    }
    for src_dir in (KNOWLEDGE_DIR, DOCS_DIR):
        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                for f in files:
                    if f.endswith((".pdf", ".txt", ".md")):
                        result["files_on_disk"] += 1
                        result["list"].append(
                            os.path.relpath(os.path.join(root, f), src_dir)
                        )

    if os.path.exists(PERSIST_DIR) and os.path.exists(
        os.path.join(PERSIST_DIR, "index.faiss")
    ):
        result["files_in_db"] = 1
        result["total_chunks"] = "unknown (FAISS index present)"
    return result
