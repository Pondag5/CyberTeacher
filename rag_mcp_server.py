import argparse
import json
import sys
import threading

_vectordb = None
_lock = threading.Lock()
_initialized = False

def get_vectordb():
    global _vectordb, _initialized
    if _vectordb is not None:
        return _vectordb
    with _lock:
        if _vectordb is not None:
            return _vectordb
        sys.stderr.write("[rag] Loading vector DB (first request)...\n")
        try:
            from knowledge import load_knowledge_base
            _vectordb = load_knowledge_base()
            if _vectordb is None:
                sys.stderr.write("[rag] Failed to load vector DB\n")
            else:
                sys.stderr.write("[rag] Vector DB loaded\n")
        except Exception as e:
            sys.stderr.write(f"[rag] Error loading vector DB: {e}\n")
            raise
        return _vectordb

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "rag-mcp-server", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "rag_query",
                        "description": "Поиск в базе знаний CyberTeacher",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Поисковый запрос"},
                                "top_k": {"type": "integer", "default": 5}
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        if tool_name == "rag_query":
            args = params.get("arguments", {})
            query = args.get("query", "")
            top_k = args.get("top_k", 5)
            try:
                vectordb = get_vectordb()
                if vectordb is None:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32000, "message": "Vector DB not loaded"}
                    }
                from knowledge import get_relevant_docs
                docs = get_relevant_docs(vectordb, query, top_k=top_k)
                results = []
                for doc in docs:
                    content = doc.page_content[:500]
                    source = doc.metadata.get("source", "unknown")
                    results.append({
                        "type": "text",
                        "text": f"📖 Источник: {source}\n\n{content}"
                    })
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": results}
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
    # Неизвестный метод
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"}
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vector-store", required=False, help="Ignored, kept for compatibility")
    args = parser.parse_args()
    
    sys.stderr.write("[rag] MCP server ready (lazy loading)\n")
    sys.stderr.flush()
    
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"[rag] Error: {e}\n")
            sys.stderr.flush()
            # Отправляем ошибку, если можем
            error_resp = {
                "jsonrpc": "2.0",
                "id": req.get("id") if 'req' in locals() else None,
                "error": {"code": -32000, "message": str(e)}
            }
            sys.stdout.write(json.dumps(error_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()