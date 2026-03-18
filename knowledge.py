"""
🔐 База знаний
"""

import gc
import glob
import hashlib
import json
import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from typing import Any, List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from config import (
    BM25_ENABLED,
    BM25_K,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    KNOWLEDGE_DIR,
    MAX_WORKERS,
    METADATA_FILE,
    PERSIST_DIR,
    RERANK_TOP_K,
    RERANKER,
    LazyLoader,
)
from ui import console

# Global vectordb for runtime access
_current_vectordb = None


def get_current_vectordb():
    """Get the currently loaded vector database."""
    return _current_vectordb


def set_current_vectordb(v):
    """Set the current vector database."""
    global _current_vectordb
    _current_vectordb = v


class ProgressEmbeddings(Embeddings):
    """Обёртка для отслеживания прогресса создания эмбеддингов"""

    def __init__(self, base_embeddings, progress_obj, progress_task):
        self.base = base_embeddings
        self.progress = progress_obj
        self.task = progress_task

    def embed_documents(self, texts):
        batch_size = 64  # increased for better throughput
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            embeddings_batch = self.base.embed_documents(batch)
            all_embeddings.extend(embeddings_batch)
            self.progress.advance(self.task, len(batch))
        return all_embeddings

    def embed_query(self, text):
        return self.base.embed_query(text)

    def __call__(self, texts):
        """Для совместимости с LangChain, который ожидает callable"""
        return self.embed_documents(texts)


def get_file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):  # increased buffer
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        console.print(
            f"[yellow]⚠️ Ошибка при вычислении хеша для {file_path}: {e}[/yellow]"
        )
        return ""


def load_metadata() -> dict:
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[yellow]⚠️ Ошибка при загрузке метаданных: {e}[/yellow]")
    return {"files": {}, "created": ""}


def save_metadata(data: dict):
    os.makedirs(PERSIST_DIR, exist_ok=True)
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def scan_knowledge_files() -> dict:
    files = {}
    if os.path.exists(KNOWLEDGE_DIR):
        for ext in ["*.txt", "*.md", "*.pdf"]:
            for file_path in glob.glob(os.path.join(KNOWLEDGE_DIR, ext)):
                rel_path = os.path.relpath(file_path, KNOWLEDGE_DIR)
                files[rel_path] = get_file_hash(file_path)
    return files


def load_and_split_file(file_path: str):
    """Load a file and return its text chunks (CPU‑intensive part)."""
    try:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(docs)
        return file_path, chunks, None
    except Exception as e:
        console.print(f"[yellow]⚠️ Ошибка при обработке файла {file_path}: {e}[/yellow]")
        return file_path, None, None


def load_knowledge_base():
    current_files = scan_knowledge_files()

    if not current_files:
        console.print("[yellow]⚠️ Файлы не найдены[/yellow]")
        return None

    saved_metadata = load_metadata()
    saved_files = saved_metadata.get("files", {})
    total_chunks_before = saved_metadata.get("total_chunks", 0)

    current_set = set(current_files.keys())
    saved_set = set(saved_files.keys())

    new_files = current_set - saved_set
    deleted_files = saved_set - current_set
    modified_files = {
        f for f in current_set & saved_set if saved_files.get(f) != current_files[f]
    }

    changed_files = new_files | deleted_files | modified_files

    if not changed_files:
        console.print("[INFO] Knowledge base up to date")
        # Load existing index to provide vectordb
        if os.path.exists(PERSIST_DIR):
            try:
                base_emb = LazyLoader.get_embeddings()
                vectordb = FAISS.load_local(
                    PERSIST_DIR, base_emb, allow_dangerous_deserialization=True
                )
                set_current_vectordb(vectordb)
                return vectordb
            except Exception as e:
                console.print(f"[yellow]⚠️ Не удалось загрузить индекс: {e}[/yellow]")
                return None
        else:
            console.print("[yellow]Индекс не найден[/yellow]")
            return None

    is_incremental = (
        bool(new_files)
        and not deleted_files
        and not modified_files
        and os.path.exists(PERSIST_DIR)
    )

    if is_incremental:
        console.print(f"[INFO] Adding {len(new_files)} new files")
        try:
            vectordb = FAISS.load_local(
                PERSIST_DIR,
                LazyLoader.get_embeddings(),
                allow_dangerous_deserialization=True,
            )
        except Exception:
            is_incremental = False

    if not is_incremental:
        console.print(f"[INFO] Rebuilding: {len(changed_files)} files changed")
        files_to_process = list(current_files.keys())
        full_rebuild = True
    else:
        files_to_process = list(new_files)
        full_rebuild = False

    file_paths = [os.path.join(KNOWLEDGE_DIR, f) for f in files_to_process]
    total = len(file_paths)

    all_chunks: list = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        load_task = progress.add_task(
            f"[cyan]Loading & splitting {total} files...", total=total
        )
        # Use ProcessPoolExecutor for CPU‑bound loading + splitting
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(load_and_split_file, fp): fp for fp in file_paths
            }
            for future in as_completed(futures):
                _, chunks, _ = future.result()
                if chunks:
                    all_chunks.extend(chunks)
                progress.advance(load_task)

        if not all_chunks:
            console.print("[yellow]⚠️ No documents loaded[/yellow]")
            return None if full_rebuild else None  # fallback not needed

        chunk_task = progress.add_task("[green]Splitting complete", total=1)
        progress.console.print(f"[green]✓ Total chunks: {len(all_chunks)}")
        progress.advance(chunk_task)

        embed_task = progress.add_task(
            "[magenta]Creating embeddings...", total=len(all_chunks)
        )

        # Use the outer ProgressEmbeddings (has __call__)
        base_emb = LazyLoader.get_embeddings()
        progress_embeddings = ProgressEmbeddings(base_emb, progress, embed_task)

        if full_rebuild:
            if os.path.exists(PERSIST_DIR):
                shutil.rmtree(PERSIST_DIR)
            os.makedirs(PERSIST_DIR, exist_ok=True)
            vectordb = FAISS.from_documents(all_chunks, progress_embeddings)
        else:
            # Incremental case: load existing index and add
            vectordb = FAISS.load_local(
                PERSIST_DIR, base_emb, allow_dangerous_deserialization=True
            )
            vectordb.add_documents(all_chunks)

        vectordb.save_local(PERSIST_DIR)
        progress.console.print("[bold green]✓ Knowledge base saved!")

        # Update metadata
        updated_files = {**saved_files, **{f: current_files[f] for f in new_files}}
        for f in deleted_files:
            updated_files.pop(f, None)
        total_chunks_final = (
            len(all_chunks) if full_rebuild else total_chunks_before + len(all_chunks)
        )
        save_metadata(
            {
                "files": updated_files,
                "created": datetime.now().isoformat(),
                "total_chunks": total_chunks_final,
            }
        )
        console.print(
            f"[bold cyan]📊 Total chunks: {total_chunks_final}, files: {len(updated_files)}[/bold cyan]"
        )

        # Free GPU memory after embedding operations
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

        set_current_vectordb(vectordb)
        return vectordb

    # Incremental addition path (only new files)
    new_file_paths = [os.path.join(KNOWLEDGE_DIR, f) for f in new_files]
    total_new = len(new_file_paths)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        load_task = progress.add_task(
            f"[cyan]Loading & splitting {total_new} new files...", total=total_new
        )
        new_chunks: list = []
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(load_and_split_file, fp): fp for fp in new_file_paths
            }
            for future in as_completed(futures):
                _, chunks, _ = future.result()
                if chunks:
                    new_chunks.extend(chunks)
                progress.advance(load_task)

        if not new_chunks:
            console.print("[yellow]⚠️ No documents loaded from new files[/yellow]")
            return None  # should not happen

        chunk_task = progress.add_task("[green]Splitting complete", total=1)
        progress.console.print(f"[green]✓ New chunks: {len(new_chunks)}")
        progress.advance(chunk_task)

        embed_task = progress.add_task(
            "[magenta]Creating embeddings for new chunks...", total=len(new_chunks)
        )
        base_emb = LazyLoader.get_embeddings()
        progress_embeddings = ProgressEmbeddings(base_emb, progress, embed_task)

        # Load existing index
        vectordb = FAISS.load_local(
            PERSIST_DIR, base_emb, allow_dangerous_deserialization=True
        )
        vectordb.add_documents(new_chunks)
        vectordb.save_local(PERSIST_DIR)
        progress.console.print("[bold green]✓ New documents added to knowledge base!")

        # Free GPU memory after embedding operations
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

        # Update metadata
        updated_files = {**saved_files, **{f: current_files[f] for f in new_files}}
        total_chunks = total_chunks_before + len(new_chunks)
        save_metadata(
            {
                "files": updated_files,
                "created": datetime.now().isoformat(),
                "total_chunks": total_chunks,
            }
        )
        console.print(
            f"[bold cyan]📊 Total chunks: {total_chunks}, files: {len(updated_files)}[/bold cyan]"
        )
        set_current_vectordb(vectordb)
        return vectordb


def get_relevant_docs(vectordb, query, k=3):
    """Гибридный поиск: векторный + BM25 + reranker"""
    if vectordb is None:
        return []
    try:
        # Получаем настройки из config с безопасным fallback
        try:
            bm25_enabled = BM25_ENABLED
            bm25_k = BM25_K
        except NameError:
            # Fallback если константы ещё не инициализированы (например, в тестах)
            bm25_enabled = False
            bm25_k = 20

        # Начинаем с векторного поиска (больше документов)
        initial_k = max(k * 3, bm25_k if bm25_enabled else k * 3)
        docs = vectordb.similarity_search(query, k=initial_k)

        if not docs:
            return []

        # === ШАГ 1: BM25 ===
        if bm25_enabled:
            try:
                import jieba
                from rank_bm25 import BM25Okapi

                # Токенизация
                doc_texts = [doc.page_content for doc in docs]
                tokenized_docs = [jieba.lcut(text) for text in doc_texts]
                tokenized_query = jieba.lcut(query)

                # Создаём BM25
                bm25 = BM25Okapi(tokenized_docs)
                bm25_scores = bm25.get_scores(tokenized_query)

                # Нормализация 0-1
                min_score, max_score = min(bm25_scores), max(bm25_scores)
                if max_score - min_score > 0:
                    bm25_norm = [
                        (s - min_score) / (max_score - min_score) for s in bm25_scores
                    ]
                else:
                    bm25_norm = [0.5] * len(bm25_scores)

                # Комбинируем: 50% векторная (по позиции) + 50% BM25
                combined_scores = []
                for i in range(len(docs)):
                    vector_score = 1.0 - (
                        i / len(docs)
                    )  # позиция в векторном результате
                    combined = 0.5 * vector_score + 0.5 * bm25_norm[i]
                    combined_scores.append((i, combined))

                # Сортируем по комбинированному скору
                sorted_indices = [
                    i
                    for i, _ in sorted(
                        combined_scores, key=lambda x: x[1], reverse=True
                    )
                ]
                bm25_docs = [docs[i] for i in sorted_indices[:bm25_k]]
                docs = bm25_docs
            except Exception as e:
                console.print(f"[yellow]⚠️ BM25 не сработал: {e}[/yellow]")
                # Продолжаем с векторными результатами

        # === ШАГ 2: RERANKER ===
        if RERANKER:
            try:
                reranker = LazyLoader.get_reranker()
                pairs = [(query, doc.page_content) for doc in docs]
                scores = reranker.predict(pairs)
                sorted_indices = sorted(
                    range(len(scores)), key=lambda i: scores[i], reverse=True
                )
                reranked_docs = [docs[i] for i in sorted_indices[:k]]
                return reranked_docs
            except Exception as e:
                console.print(f"[yellow]⚠️ Reranking failed: {e}[/yellow]")
                return docs[:k]

        return docs[:k]
    except Exception as e:
        console.print(f"[yellow]⚠️ Ошибка при поиске документов: {e}[/yellow]")
        return []
    try:
        # Начинаем с векторного поиска (больше документов)
        initial_k = max(k * 3, BM25_K if BM25_ENABLED else k * 3)

        if not docs:
            return []

        # === ШАГ 1: BM25 ===
        if BM25_ENABLED:
            try:
                import jieba
                from rank_bm25 import BM25Okapi

                # Токенизация
                doc_texts = [doc.page_content for doc in docs]
                tokenized_docs = [jieba.lcut(text) for text in doc_texts]
                tokenized_query = jieba.lcut(query)

                # Создаём BM25
                bm25 = BM25Okapi(tokenized_docs)
                bm25_scores = bm25.get_scores(tokenized_query)

                # Нормализация 0-1
                min_score, max_score = min(bm25_scores), max(bm25_scores)
                if max_score - min_score > 0:
                    bm25_norm = [
                        (s - min_score) / (max_score - min_score) for s in bm25_scores
                    ]
                else:
                    bm25_norm = [0.5] * len(bm25_scores)

                # Комбинируем: 50% векторная (по позиции) + 50% BM25
                combined_scores = []
                for i in range(len(docs)):
                    vector_score = 1.0 - (
                        i / len(docs)
                    )  # позиция в векторном результате
                    combined = 0.5 * vector_score + 0.5 * bm25_norm[i]
                    combined_scores.append((i, combined))

                # Сортируем по комбинированному скору
                sorted_indices = [
                    i
                    for i, _ in sorted(
                        combined_scores, key=lambda x: x[1], reverse=True
                    )
                ]
                bm25_docs = [docs[i] for i in sorted_indices[:BM25_K]]
                docs = bm25_docs
            except Exception as e:
                console.print(f"[yellow]⚠️ BM25 не сработал: {e}[/yellow]")
                # Продолжаем с векторными результатами

        # === ШАГ 2: RERANKER ===
        if RERANKER:
            try:
                reranker = LazyLoader.get_reranker()
                pairs = [(query, doc.page_content) for doc in docs]
                scores = reranker.predict(pairs)
                sorted_indices = sorted(
                    range(len(scores)), key=lambda i: scores[i], reverse=True
                )
                reranked_docs = [docs[i] for i in sorted_indices[:k]]
                return reranked_docs
            except Exception as e:
                console.print(f"[yellow]⚠️ Reranking failed: {e}[/yellow]")
                return docs[:k]

        return docs[:k]
    except Exception as e:
        console.print(f"[yellow]⚠️ Ошибка при поиске документов: {e}[/yellow]")
        return []


def get_knowledge_status():
    """Возвращает статистику базы знаний"""
    import json

    from config import KNOWLEDGE_DIR, METADATA_FILE

    files_on_disk = []
    if os.path.exists(KNOWLEDGE_DIR):
        for f in os.listdir(KNOWLEDGE_DIR):
            if f.endswith((".txt", ".md", ".pdf")):
                files_on_disk.append(f)

    files_in_db = []
    total_chunks = 0

    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            data = json.load(f)
            files_in_db = list(data.get("files", {}).keys())
            total_chunks = data.get("total_chunks", 0)

    return {
        "files_on_disk": len(files_on_disk),
        "files_in_db": len(files_in_db),
        "total_chunks": total_chunks,
        "list": files_in_db,
    }
