#!/usr/bin/env python3
"""
index_project.py – индексация проекта с FAISS (векторный поиск)
Запуск: python index_project.py
"""

import os
import hashlib
import json
import re
import pickle
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

PROJECT_ROOT = Path(__file__).parent.resolve()
FAISS_INDEX_PATH = PROJECT_ROOT / "faiss_index.bin"
METADATA_PATH = PROJECT_ROOT / "chunks_metadata.json"
FILE_HASHES_PATH = PROJECT_ROOT / "file_hashes.json"

EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".html",
    ".css",
    ".js",
    ".toml",
    ".ini",
    ".cfg",
    ".rst",
}
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".ruff_cache",
    "book_new",
    "venv",
    "env",
    "node_modules",
    "test_reports",
    "backups",
    "embeddings",
    ".context",
    "chroma_db",
    "cves",
    "tests",
}

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MAX_FILE_AGE_DAYS = 30  # Only re-index files modified in the last 30 days


def get_file_hash(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def load_hashes() -> Dict[str, str]:
    if FILE_HASHES_PATH.exists():
        with open(FILE_HASHES_PATH, "r", encoding="utf-8") as f:
            result: Dict[str, str] = json.load(f)
            return result
    return {}


def save_hashes(hashes: Dict[str, str]) -> None:
    with open(FILE_HASHES_PATH, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2, ensure_ascii=False)


def get_text_files(old_hashes: Dict[str, str] = None) -> List[Path]:
    import time

    files: List[Path] = []
    cutoff_time = time.time() - (MAX_FILE_AGE_DAYS * 86400)
    for ext in EXTENSIONS:
        for f in PROJECT_ROOT.rglob(f"*{ext}"):
            if any(excl in f.parts for excl in EXCLUDE_DIRS):
                continue
            try:
                rel_path = str(f.relative_to(PROJECT_ROOT))
                mtime = f.stat().st_mtime
                # Always include if new (not in old_hashes) or recently modified
                if old_hashes and rel_path not in old_hashes:
                    files.append(f)
                elif mtime >= cutoff_time:
                    files.append(f)
            except OSError:
                pass
    return files


def split_text_into_chunks(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> List[str]:
    if not text:
        return []
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 <= chunk_size:
            if current:
                current += "\n\n" + para
            else:
                current = para
        else:
            if current:
                chunks.append(current)
            if overlap > 0 and current:
                overlap_text = current[-overlap:] if len(current) > overlap else current
                current = overlap_text + "\n\n" + para
            else:
                current = para
    if current:
        chunks.append(current)
    return chunks


def main():
    print("[INDEX] Индексация проекта (FAISS)...")
    old_hashes = load_hashes()
    files = get_text_files(old_hashes)
    print(f"[INDEX] Найдено файлов для проверки: {len(files)}")

    new_hashes = {}

    # Собираем все чанки и их метаданные
    all_chunks = []  # list of (source, chunk_text)
    updated_files = 0

    for file_path in files:
        rel_path = str(file_path.relative_to(PROJECT_ROOT))
        new_hash = get_file_hash(file_path)
        new_hashes[rel_path] = new_hash

        if old_hashes.get(rel_path) == new_hash:
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            print(f"[WARN] {rel_path}: {e}")
            continue

        chunks = split_text_into_chunks(text)
        if chunks:
            for ch in chunks:
                all_chunks.append((rel_path, ch))
            updated_files += 1
            print(f"[OK] {rel_path} – {len(chunks)} chunks")
        else:
            print(f"[SKIP] {rel_path} – empty")

    if not all_chunks:
        print("[INDEX] No new data to index.")
        return

    print("[INDEX] Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("[INDEX] Generating embeddings...")
    texts = [chunk[1] for chunk in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(FAISS_INDEX_PATH))
    metadata = {"chunks": [{"source": src, "text": txt} for src, txt in all_chunks]}
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    save_hashes(new_hashes)

    print(f"\n[INDEX] Done!")
    print(f"   Total chunks: {len(all_chunks)}")
    print(f"   Updated files: {updated_files}")
    print(f"   FAISS index: {FAISS_INDEX_PATH}")
    print(f"   Metadata: {METADATA_PATH}")


if __name__ == "__main__":
    main()
