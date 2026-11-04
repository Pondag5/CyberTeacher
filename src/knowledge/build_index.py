#!/usr/bin/env python3
"""
build_index.py – Создаёт FAISS индекс для всей кодовой базы CyberTeacher.
Запуск: python build_index.py
Результат: faiss_index.bin, chunks_metadata.json в корне проекта.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Настройки
PROJECT_ROOT = Path(__file__).parent.resolve()
CHUNK_SIZE = 700           # символов на чанк
OVERLAP = 150              # перекрытие между чанками
MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = PROJECT_ROOT / "faiss_index.bin"
METADATA_PATH = PROJECT_ROOT / "chunks_metadata.json"

# Расширения файлов, которые индексируем
EXTENSIONS = {
    '.py', '.md', '.txt', '.json', '.yaml', '.yml',
    '.sh', '.bat', '.js', '.html', '.css', '.toml',
    '.cfg', '.ini', '.xml', '.sql'
}

# Папки, которые игнорируем
IGNORE_DIRS = {
    '.git', '__pycache__', '.ruff_cache', '.mypy_cache',
    'node_modules', 'venv', 'env', '.venv', '.idea',
    '.vscode', 'dist', 'build', '*.egg-info'
}
IGNORE_FILES = {
    '.gitignore', '.env', '.env.bak', '*.log',
    '*.bin', '*.pkl', '*.faiss', '*.db', '*.sqlite3',
    '*.pdf', '*.png', '*.jpg', '*.ico'
}

def should_ignore(path: Path) -> bool:
    """Проверяет, нужно ли игнорировать файл или директорию."""
    for part in path.parts:
        if part in IGNORE_DIRS or part.startswith('.'):
            return True
    # Проверяем расширение
    if path.suffix in IGNORE_FILES or path.suffix in ['.bin', '.pkl', '.faiss', '.db']:
        return True
    # Игнорируем бинарные файлы по расширению (можно расширить)
    if path.suffix in ['.pyc', '.pyo', '.so', '.dll', '.exe']:
        return True
    return False

def get_file_chunks(file_path: Path) -> List[str]:
    """Читает файл и разбивает на чанки с перекрытием."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return []
    if not content:
        return []
    # Удаляем слишком длинные строки? Можно оставить как есть.
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + CHUNK_SIZE, len(content))
        chunk = content[start:end]
        chunks.append(chunk)
        start = end - OVERLAP  # перекрытие
        if start < 0:
            start = 0
    return chunks

def main():
    print("🔍 Сбор файлов для индексации...")
    all_chunks: List[Dict] = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Удаляем игнорируемые директории из обхода
        dirs[:] = [d for d in dirs if not should_ignore(Path(root) / d)]
        for file in files:
            file_path = Path(root) / file
            if should_ignore(file_path):
                continue
            # Проверяем расширение
            if file_path.suffix not in EXTENSIONS:
                continue
            # Получаем относительный путь
            rel_path = str(file_path.relative_to(PROJECT_ROOT))
            chunks = get_file_chunks(file_path)
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source": rel_path,
                    "chunk_id": i
                })
            if len(all_chunks) % 100 == 0:
                print(f"  Обработано {len(all_chunks)} чанков...")
    print(f"✅ Собрано {len(all_chunks)} чанков.")

    if not all_chunks:
        print("❌ Нет чанков для индексации.")
        return

    print("🧠 Загрузка модели для эмбеддингов...")
    model = SentenceTransformer(MODEL_NAME)
    print("📊 Вычисление эмбеддингов...")
    texts = [c["text"] for c in all_chunks]
    # Вычисляем батчами для экономии памяти (batch_size=32)
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    print("💾 Сохранение FAISS индекса...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # косинусное сходство через нормализацию? Можно IndexFlatL2, но у нас косинус.
    # Для косинусного сходства нужно нормализовать векторы:
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))

    print("💾 Сохранение метаданных...")
    metadata = {
        "chunks": all_chunks,
        "model_name": MODEL_NAME,
        "chunk_size": CHUNK_SIZE,
        "overlap": OVERLAP,
        "total_chunks": len(all_chunks)
    }
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Готово: {INDEX_PATH} и {METADATA_PATH}")
    print(f"   Всего чанков: {len(all_chunks)}, размерность: {dim}")

if __name__ == "__main__":
    main()