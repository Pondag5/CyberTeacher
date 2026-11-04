#!/usr/bin/env python3
"""
search_faiss.py – поиск по FAISS индексу
Запуск: python search_faiss.py "ваш запрос"
"""

import sys
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
FAISS_INDEX_PATH = PROJECT_ROOT / "faiss_index.bin"
METADATA_PATH = PROJECT_ROOT / "chunks_metadata.json"

def search(query: str, top_k: int = 5):
    # Загружаем индекс и метаданные
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    chunks = metadata["chunks"]
    
    # Эмбеддинг запроса
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_emb = model.encode([query])
    query_emb = np.array(query_emb).astype('float32')
    
    # Поиск
    distances, indices = index.search(query_emb, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        chunk_data = chunks[idx]
        results.append({
            "score": float(distances[0][i]),
            "source": chunk_data["source"],
            "text": chunk_data["text"][:500] + "..."
        })
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python search_faiss.py 'ваш запрос'")
        sys.exit(1)
    query = sys.argv[1]
    results = search(query)
    print(f"\n🔍 Результаты по запросу: {query}\n")
    for r in results:
        print(f"📄 {r['source']} (score={r['score']:.2f})")
        print(f"   {r['text']}\n")