# knowledge.py - RAG and knowledge base management

from __future__ import annotations

import json
import logging
import os
import pickle
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

# Full corpus store for BM25 and metadata-aware retrieval
_all_docs_store: List[Dict[str, Any]] = []
_bm25_index: Any = None

# ----------------------------------------------------------------------
# Category inference from filename
# ----------------------------------------------------------------------
_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "network": [
        "bgp", "eigrp", "ospf", "rip", "qos", "vlan", "ipv4", "ipv6",
        "subnetting", "tcp", "udp", "dns", "dhcp", "nat", "wan", "lan",
        "cisco", "ios", "mpls", "ieee", "802", "wlan", "voip", "ppp",
        "spanning_tree", "routing", "switch", "first_hop", "frame_mode",
        "multicast", "physical_terminations", "cable",
    ],
    "security": [
        "hack", "exploit", "metasploit", "antivirus", "payload", "injection",
        "sql", "xss", "csrf", "pentest", "vulnerability", "cve", "shadow",
        "hashes", "brute", "force", "john", "hydra", "mimikatz", "meterpreter",
        "powersploit", "kali", "backtrack", "ethical", "ransomware", "malware",
        "forensic", "incident", "blue_team", "red_team", "threat",
        "password", "ssh", "private_key", "social-engineering",
    ],
    "forensics": [
        "forensic", "memory_dump", "incident", "response", "analysis",
        "registry", "log", "artifact", "windows_security", "dfir",
    ],
    "osint": [
        "shodan", "osint", "reconnaissance", "recon", "passive", "intelligence",
    ],
    "web": [
        "web", "http", "https", "burp", "owasp", "xss", "csrf", "sqli",
        "ssrf", "idor", "api", "application",
    ],
    "social_engineering": [
        "social", "phishing", "pretexting", "baiting", "tailgating",
        "influence", "friends",
    ],
    "programming": [
        "python", "black_hat", "violent_python", "scapy", "scripting",
        "automation", "code", "git",
    ],
    "tools": [
        "scapy", "netcat", "tcpdump", "wireshark", "nmap", "display_filters",
        "cheat_sheet", "cheatsheet", "payloads", "msfvenom",
    ],
    "database": [
        "sql", "database", "mysql", "postgresql", "oracle", "nosql", "mongodb",
        "databse",
    ],
    "cloud": [
        "cloud", "aws", "azure", "gcp", "docker", "kubernetes", "k8s",
    ],
    "wireless": [
        "wifi", "wireless", "wlan", "bluetooth", "rf", "802.11",
    ],
    "ids_ips": [
        "ids", "ips", "siem", "firewall", "intrusion", "detection",
    ],
}


def _infer_category(filename: str) -> str:
    """Infer document category from filename (lowercase, no extension)."""
    base = os.path.splitext(filename)[0].lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        if any(kw in base for kw in keywords):
            return category
    return "general"


# ----------------------------------------------------------------------
# BM25 utils
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
        result = self.embeddings.embed_documents(texts)
        self.processed = len(texts)
        return result

    def embed_query(self, text):
        return self.embeddings.embed_query(text)


class BM25Retriever:
    """Simple BM25 retriever for hybrid search."""

    def __init__(self, documents: List[str], tokenizer=None):
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


# ----------------------------------------------------------------------
# Document loading and splitting
# ----------------------------------------------------------------------
def load_and_split_file(file_path: str):
    """Load a file and split into chunks with rich metadata."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import PyPDFLoader, TextLoader

    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    try:
        documents = loader.load()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to load file {file_path}: {e}")
        return []

    # Adaptive chunking based on file type
    if ext == ".pdf":
        chunk_size = max(CHUNK_SIZE, 800)
        chunk_overlap = max(CHUNK_OVERLAP, 120)
    else:
        chunk_size = CHUNK_SIZE
        chunk_overlap = CHUNK_OVERLAP

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)

    filename = os.path.basename(file_path)
    category = _infer_category(filename)

    for idx, chunk in enumerate(chunks):
        chunk.metadata.setdefault("source", filename)
        chunk.metadata.setdefault("category", category)
        chunk.metadata.setdefault("chunk_index", idx)
        chunk.metadata.setdefault("total_chunks", len(chunks))
        chunk.metadata.setdefault("file_type", ext.lstrip("."))

    return chunks


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


# ----------------------------------------------------------------------
# BM25 persistence
# ----------------------------------------------------------------------
def _bm25_persist_path() -> str:
    return os.path.join(PERSIST_DIR, "bm25_index.pkl")


def _save_bm25_index(bm25_retriever: Any, corpus: List[str]) -> None:
    path = _bm25_persist_path()
    try:
        os.makedirs(PERSIST_DIR, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({"bm25": bm25_retriever, "corpus": corpus}, f)
    except Exception as e:
        logger.warning(f"Failed to save BM25 index: {e}")


def _load_bm25_index() -> Optional[Dict[str, Any]]:
    path = _bm25_persist_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        logger.warning(f"Failed to load BM25 index: {e}")
        return None


# ----------------------------------------------------------------------
# Hybrid index loading
# ----------------------------------------------------------------------
def load_knowledge_base():
    """Load or create FAISS vector store from knowledge_base and docs directories."""
    from langchain_community.vectorstores import FAISS

    global _current_vectordb, _all_docs_store, _bm25_index
    embeddings = LazyLoader.get_embeddings()
    if embeddings is None:
        logger.error("Embeddings not available, cannot load knowledge base")
        return None

    # Try to load existing FAISS index
    if os.path.exists(PERSIST_DIR):
        try:
            vectordb = FAISS.load_local(
                PERSIST_DIR, embeddings, allow_dangerous_deserialization=True
            )
            _current_vectordb = vectordb
            _INDEX_TIMESTAMP = time.time()
            logger.info(f"Loaded existing FAISS index from {PERSIST_DIR}")

            # Load BM25 from disk or rebuild from existing FAISS docstore
            bm25_data = _load_bm25_index()
            if bm25_data:
                _bm25_index = bm25_data.get("bm25")
                _all_docs_store = [
                    {"text": t, "source": "", "category": ""}
                    for t in bm25_data.get("corpus", [])
                ]
                logger.info("Loaded persistent BM25 index")
            else:
                try:
                    corpus = []
                    store = getattr(getattr(vectordb, "docstore", None), "_dict", {}) or {}
                    for doc in store.values():
                        corpus.append(doc.page_content)
                    if corpus:
                        _bm25_index = BM25Retriever(corpus, tokenizer=_chinese_tokenizer)
                        _all_docs_store = [
                            {"text": t, "source": "", "category": ""} for t in corpus
                        ]
                        _save_bm25_index(_bm25_index, corpus)
                        logger.info("Rebuilt BM25 index from existing FAISS docstore")
                except Exception as e:
                    logger.debug(f"Failed to rebuild BM25 from docstore: {e}")
                    _bm25_index = None

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
    all_docs: List[Any] = []
    _all_docs_store = []

    for src_dir in source_dirs:
        dir_docs = _load_docs_from_dir(src_dir)
        logger.info(f"Loaded {len(dir_docs)} chunks from {src_dir}")
        all_docs.extend(dir_docs)

        # Build full corpus store for BM25
        for doc in dir_docs:
            _all_docs_store.append({
                "text": doc.page_content,
                "source": doc.metadata.get("source", ""),
                "category": doc.metadata.get("category", ""),
            })

    if not all_docs:
        logger.warning("No documents loaded from any source directory")
        return None

    progress_emb = ProgressEmbeddings(embeddings, len(all_docs))
    vectordb = FAISS.from_documents(all_docs, progress_emb)
    os.makedirs(PERSIST_DIR, exist_ok=True)
    vectordb.save_local(PERSIST_DIR)
    _current_vectordb = vectordb
    _INDEX_TIMESTAMP = time.time()

    # Build and persist BM25 on full corpus
    if BM25_ENABLED and BM25Okapi is not None:
        try:
            corpus_texts = [d["text"] for d in _all_docs_store]
            bm25 = BM25Retriever(corpus_texts, tokenizer=_chinese_tokenizer)
            _bm25_index = bm25
            _save_bm25_index(bm25, corpus_texts)
            logger.info(f"Built and saved BM25 index with {len(corpus_texts)} documents")
        except Exception as e:
            logger.warning(f"Failed to build BM25 index: {e}")
            _bm25_index = None

    logger.info(f"Created and saved FAISS index with {len(all_docs)} chunks")
    return vectordb


def get_current_vectordb():
    """Return the current vector database instance."""
    global _current_vectordb
    return _current_vectordb


# ----------------------------------------------------------------------
# Query cache
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Hybrid search helpers
# ----------------------------------------------------------------------
def _rrf_fuse(faiss_docs: List[Any], bm25_docs: List[Any], k: int = 50) -> List[Any]:
    """Reciprocal Rank Fusion of FAISS and BM25 results."""
    scores: Dict[int, float] = {}
    doc_map: Dict[int, Any] = {}

    for rank, doc in enumerate(faiss_docs):
        doc_id = id(doc)
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (60 + rank)
        doc_map[doc_id] = doc

    for rank, doc in enumerate(bm25_docs):
        doc_id = id(doc)
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (60 + rank)
        doc_map[doc_id] = doc

    ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:k]
    return [doc_map[doc_id] for doc_id in ranked_ids]


def _expand_query(query: str) -> str:
    """Simple query expansion for technical terms."""
    expansions = {
        "hack": "hack exploit penetration test pentest",
        "exploit": "exploit payload metasploit attack",
        "network": "network tcp ip routing switch vlan",
        "sql": "sql injection database query",
        "password": "password hash cracking brute force",
        "scan": "scan nmap reconnaissance osint",
        "malware": "malware virus ransomware trojan",
        "forensic": "forensic analysis incident response",
        "phishing": "phishing social engineering email",
        "wireless": "wireless wifi wlan 802.11",
        "cloud": "cloud aws azure docker kubernetes",
    }
    expanded = query
    for term, synonyms in expansions.items():
        if term in query.lower():
            expanded += " " + synonyms
    return expanded


# ----------------------------------------------------------------------
# Main retrieval
# ----------------------------------------------------------------------
def get_relevant_docs(
    vectordb,
    query: str,
    top_k: int = RERANK_TOP_K,
    source_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
):
    """Retrieve relevant documents using hybrid search (FAISS + BM25 + reranker)."""
    if vectordb is None:
        return []

    cached = _get_kb_cache(vectordb, query, top_k)
    if cached is not None:
        return cached

    expanded_query = _expand_query(query)

    # Step 1: FAISS similarity search
    faiss_docs = vectordb.similarity_search(expanded_query, k=top_k * 3)

    # Step 2: BM25 on full corpus (if available)
    bm25_docs: List[Any] = []
    if BM25_ENABLED and _bm25_index is not None and _all_docs_store:
        try:
            bm25_indices = _bm25_index.get_top_n(expanded_query, n=top_k * 3)
            # Convert BM25 indices back to Document-like objects
            for idx in bm25_indices:
                if idx < len(_all_docs_store):
                    store_entry = _all_docs_store[idx]
                    # Apply filters
                    if source_filter and source_filter not in store_entry.get("source", ""):
                        continue
                    if category_filter and category_filter != store_entry.get("category", ""):
                        continue
                    # Create a Document-like object
                    from langchain_core.documents import Document

                    doc = Document(
                        page_content=store_entry["text"],
                        metadata={
                            "source": store_entry.get("source", ""),
                            "category": store_entry.get("category", ""),
                        },
                    )
                    bm25_docs.append(doc)
        except Exception as e:
            logger.debug(f"BM25 search failed: {e}")

    # Step 3: RRF fusion
    if bm25_docs:
        combined = _rrf_fuse(faiss_docs, bm25_docs, k=top_k * 3)
    else:
        combined = faiss_docs

    # Apply source/category filters to FAISS results if BM25 wasn't used
    if not bm25_docs and (source_filter or category_filter):
        filtered = []
        for doc in combined:
            meta = getattr(doc, "metadata", {}) or {}
            source = meta.get("source", "")
            category = meta.get("category", "")
            if source_filter and source_filter not in source:
                continue
            if category_filter and category_filter != category:
                continue
            filtered.append(doc)
        combined = filtered

    # Step 4: Cross-encoder reranking
    reranker = LazyLoader.get_reranker()
    if reranker is not None and combined:
        try:
            pairs = [(expanded_query, doc.page_content) for doc in combined]
            scores = reranker.predict(pairs)
            scored = list(zip(scores, combined))
            scored.sort(key=lambda x: x[0], reverse=True)
            top_docs = [doc for _, doc in scored[:top_k]]
        except Exception as e:
            logger.debug(f"Reranker failed: {e}")
            top_docs = combined[:top_k]
    else:
        top_docs = combined[:top_k]

    _set_kb_cache(vectordb, query, top_k, top_docs)
    return top_docs


# ----------------------------------------------------------------------
# Add PDF to knowledge base
# ----------------------------------------------------------------------
def add_pdf_to_knowledge_base(pdf_path: str) -> bool:
    """
    Добавляет один PDF-файл в базу знаний (переиндексация).
    Возвращает True при успехе, иначе False.
    """
    global _current_vectordb, _file_list_cache, _all_docs_store, _bm25_index
    try:
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            return False

        docs = load_and_split_file(pdf_path)
        if not docs:
            logger.warning(f"No chunks extracted from {pdf_path}")
            return False

        vectordb = get_current_vectordb()
        if vectordb is None:
            vectordb = load_knowledge_base()

        if vectordb is None:
            from langchain_community.vectorstores import FAISS

            embeddings = LazyLoader.get_embeddings()
            if embeddings is None:
                logger.error("No embeddings available")
                return False
            vectordb = FAISS.from_documents(docs, embeddings)
        else:
            vectordb.add_documents(docs)

        os.makedirs(PERSIST_DIR, exist_ok=True)
        vectordb.save_local(PERSIST_DIR)
        _current_vectordb = vectordb
        _INDEX_TIMESTAMP = time.time()
        _file_list_cache = {"timestamp": 0.0, "files": []}
        clear_kb_cache()

        # Update full corpus store
        for doc in docs:
            _all_docs_store.append({
                "text": doc.page_content,
                "source": doc.metadata.get("source", ""),
                "category": doc.metadata.get("category", ""),
            })

        # Rebuild BM25 index
        if BM25_ENABLED and BM25Okapi is not None and _all_docs_store:
            try:
                corpus_texts = [d["text"] for d in _all_docs_store]
                _bm25_index = BM25Retriever(corpus_texts, tokenizer=_chinese_tokenizer)
                _save_bm25_index(_bm25_index, corpus_texts)
            except Exception as e:
                logger.warning(f"Failed to rebuild BM25 after adding PDF: {e}")

        logger.info(f"Successfully added {pdf_path} to knowledge base")
        return True

    except Exception as e:
        logger.error(f"Failed to add PDF {pdf_path}: {e}")
        return False


# ----------------------------------------------------------------------
# Knowledge base status
# ----------------------------------------------------------------------
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
