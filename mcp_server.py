#!/usr/bin/env python3
"""
mcp_server.py – MCP-сервер для поиска по коду проекта (FAISS + sentence-transformers)
Запуск: python mcp_server.py
"""

import json
import sys
import os
from pathlib import Path
from typing import Any

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Подавляем stdout/stderr на время загрузки
old_stdout, old_stderr = sys.stdout, sys.stderr
sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")

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
    sys.stdout, sys.stderr = old_stdout, old_stderr
    print(f"Error loading index: {e}", file=sys.stderr)
    sys.exit(1)

sys.stdout, sys.stderr = old_stdout, old_stderr


def search(query: str, top_k: int = 5) -> str:
    """Ищет релевантные чанки через FAISS."""
    query_emb = model.encode([query])
    query_emb = np.array(query_emb).astype("float32")
    distances, indices = index.search(query_emb, top_k)
    output = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        chunk = chunks[idx]
        text = chunk["text"]
        source = chunk["source"]
        output.append(
            f"=== Результат {i + 1} (файл: {source}, score={float(distances[0][i]):.2f}) ==="
        )
        output.append((text[:1000] + "...") if len(text) > 1000 else text)
        output.append("")
    return "\n".join(output) if output else "Ничего не найдено."


def get_project_structure() -> str:
    """Возвращает структуру проекта (директории верхнего уровня)."""
    parts = []
    for p in sorted(PROJECT_ROOT.iterdir()):
        if p.name.startswith(".") or p.name.startswith("__"):
            continue
        if p.is_dir():
            parts.append(f"📁 {p.name}/")
        else:
            parts.append(f"📄 {p.name}")
    return "\n".join(parts)


# MCP протокол: читаем строки из stdin, отправляем JSON в stdout
def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "project-info-mcp", "version": "1.0.0"},
            },
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "search_codebase",
                        "description": "Semantic search across the entire CyberTeacher project codebase.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query (e.g., 'how are labs started?', 'docker labs configuration')",
                                },
                                "n_results": {
                                    "type": "integer",
                                    "description": "Number of results to return (default 5)",
                                    "default": 5,
                                },
                            },
                            "required": ["query"],
                        },
                    },
                    {
                        "name": "get_project_structure",
                        "description": "List top-level files and directories in the project.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                        },
                    },
                ]
            },
        }
    elif method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "search_codebase":
            query = args.get("query", "")
            n = args.get("n_results", 5)
            result_text = search(query, n)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": result_text}]},
            }
        elif tool_name == "get_project_structure":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": get_project_structure()}]
                },
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool not found: {tool_name}"},
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }


def main():
    print("🔍 MCP Code Search Server running. Waiting for requests...", file=sys.stderr)
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
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)},
            }
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
