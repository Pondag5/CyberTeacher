#!/usr/bin/env python3
"""
MCP сервер для поиска по коду проекта (FAISS + sentence-transformers)
Запуск: python mcp_server_faiss.py
"""

import os
import sys
import json
from pathlib import Path

# Подавляем stdout и stderr на время загрузки модели
old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).parent.resolve()
FAISS_INDEX_PATH = PROJECT_ROOT / "faiss_index.bin"
METADATA_PATH = PROJECT_ROOT / "chunks_metadata.json"

try:
    index = faiss.read_index(str(FAISS_INDEX_PATH))
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    chunks = metadata["chunks"]
    model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    print(f"Error loading index: {e}", file=sys.stderr)
    sys.exit(1)

# Восстанавливаем stdout/stderr
sys.stdout = old_stdout
sys.stderr = old_stderr


def search(query: str, top_k: int = 5):
    """Поиск релевантных чанков по запросу."""
    query_emb = model.encode([query])
    query_emb = np.array(query_emb).astype('float32')
    distances, indices = index.search(query_emb, top_k)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        chunk_data = chunks[idx]
        results.append({
            "score": float(distances[0][i]),
            "source": chunk_data["source"],
            "text": chunk_data["text"]
        })
    return results


def format_results(results):
    if not results:
        return "Ничего не найдено."
    output = []
    for i, r in enumerate(results, 1):
        output.append(f"=== Результат {i} (файл: {r['source']}, score={r['score']:.2f}) ===")
        output.append(r['text'][:1000] + "..." if len(r['text']) > 1000 else r['text'])
        output.append("")
    return "\n".join(output)


def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",  # ← ВОТ ЭТО БЫЛО ПРОПУЩЕНО
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "code-search-mcp", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "search_codebase",
                        "description": "Search the project codebase for relevant code snippets or documentation.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"},
                                "n_results": {"type": "integer", "description": "Number of results", "default": 5}
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "search_codebase":
            query = args.get("query", "")
            n = args.get("n_results", 5)
            results = search(query, n)
            text = format_results(results)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": text}]
                }
            }
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main():
    print("MCP Code Search Server (FAISS) running...", file=sys.stderr)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()