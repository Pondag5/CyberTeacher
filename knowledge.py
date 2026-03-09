"""
🔐 База знаний
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS

from config import KNOWLEDGE_DIR, PERSIST_DIR, METADATA_FILE, LazyLoader, CHUNK_SIZE, CHUNK_OVERLAP, MAX_WORKERS
from ui import console

def get_file_hash(file_path: str) -> str:
    h = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        console.print(f"[yellow]⚠️ Ошибка при вычислении хеша для {file_path}: {e}[/yellow]")
        return ""

def load_metadata() -> dict:
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[yellow]⚠️ Ошибка при загрузке метаданных: {e}[/yellow]")
    return {"files": {}, "created": ""}

def save_metadata(data: dict):
    os.makedirs(PERSIST_DIR, exist_ok=True)
    with open(METADATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def scan_knowledge_files() -> dict:
    files = {}
    if os.path.exists(KNOWLEDGE_DIR):
        for ext in ['*.txt', '*.md', '*.pdf']:
            for file_path in glob.glob(os.path.join(KNOWLEDGE_DIR, ext)):
                rel_path = os.path.relpath(file_path, KNOWLEDGE_DIR)
                files[rel_path] = get_file_hash(file_path)
    return files

def load_single_file(file_path):
    try:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding='utf-8')
        docs = loader.load()
        return file_path, docs, None
    except Exception as e:
        console.print(f"[yellow]⚠️ Ошибка при загрузке файла {file_path}: {e}[/yellow]")
        return file_path, None, None

def load_knowledge_base():
    current_files = scan_knowledge_files()

    if not current_files:
        console.print("[yellow]⚠️ Файлы не найдены[/yellow]")
        return None

    saved_metadata = load_metadata()
    saved_files = saved_metadata.get("files", {})
    saved_chunks = saved_metadata.get("total_chunks", 0)

    current_set = set(current_files.keys())
    saved_set = set(saved_files.keys())

    new_files = current_set - saved_set
    deleted_files = saved_set - current_set
    
    # Если нет сохранённой базы - нужна полная пересборка
    if not saved_files:
        changed_files = current_set
    else:
        changed_files = new_files | deleted_files
    
    if changed_files:
        print(f"[INFO] Rebuilding knowledge base: {len(changed_files)} files changed")
    elif new_files:
        print(f"[INFO] Adding {len(new_files)} new files")
    else:
        print("[INFO] Knowledge base up to date")
        return None

    # Full rebuild
    print("[INFO] Indexing knowledge base...")
    all_files = list(current_files.keys())
    file_paths = [os.path.join(KNOWLEDGE_DIR, f) for f in all_files]
    documents = []
    total = len(all_files)

    print(f"Loading {total} files...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(load_single_file, fp): fp for fp in file_paths}
        completed = 0

        for future in as_completed(futures):
            completed += 1
            file_path, docs, _ = future.result()
            if docs:
                documents.extend(docs)
                print(f"  [{completed}/{total}] Loaded: {os.path.basename(file_path)[:40]}")

    if documents:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        texts = text_splitter.split_documents(documents)
        total_chunks = len(texts)
        print(f"Total chunks: {total_chunks}")

        # Use FAISS
        from langchain_community.vectorstores import FAISS
        embeddings = LazyLoader.get_embeddings()
        
        if os.path.exists(PERSIST_DIR):
            shutil.rmtree(PERSIST_DIR)
        os.makedirs(PERSIST_DIR, exist_ok=True)

        vectordb = FAISS.from_documents(texts, embeddings)
        vectordb.save_local(PERSIST_DIR)
        print("[OK] Knowledge base saved!")

        save_metadata({
            "files": current_files,
            "created": datetime.now().isoformat(),
            "total_chunks": total_chunks
        })
        return vectordb

    return None


def get_relevant_docs(vectordb, query, k=3):
    if vectordb is None:
        return []
    try:
        return vectordb.similarity_search(query, k=k)
    except Exception as e:
        console.print(f"[yellow]⚠️ Ошибка при поиске документов: {e}[/yellow]")
        return []


def get_knowledge_status():
    """Возвращает статистику базы знаний"""
    import json
    from config import METADATA_FILE, KNOWLEDGE_DIR
    
    files_on_disk = []
    if os.path.exists(KNOWLEDGE_DIR):
        for f in os.listdir(KNOWLEDGE_DIR):
            if f.endswith(('.txt', '.md', '.pdf')):
                files_on_disk.append(f)
    
    files_in_db = []
    total_chunks = 0
    
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            data = json.load(f)
            files_in_db = list(data.get("files", {}).keys())
            total_chunks = data.get("total_chunks", 0)
            
    return {
        "files_on_disk": len(files_on_disk),
        "files_in_db": len(files_in_db),
        "total_chunks": total_chunks,
        "list": files_in_db
    }
