"""
🔍 Аудит базы знаний
"""
import os
from config import KNOWLEDGE_DIR
from ui import console, print_panel

def audit_knowledge_base():
    """Проверяет файлы базы знаний на наличие ошибок и мусора"""
    if not os.path.exists(KNOWLEDGE_DIR):
        return "Папка knowledge_base не найдена."
    
    files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith(('.txt', '.md', '.pdf'))]
    results = []
    
    error_markers = ["<html", "<!doctype", "404: not found", "access denied", "error", "<title>error</title>"]
    
    for filename in files:
        filepath = os.path.join(KNOWLEDGE_DIR, filename)
        
        # 1. Проверка размера
        size = os.path.getsize(filepath)
        if size < 100:
            results.append(f"❌ [red]{filename}[/red] - Пустой или слишком маленький ({size} байт)")
            continue
            
        # 2. Проверка содержимого (только для текстовых)
        if filename.endswith('.txt') or filename.endswith('.md'):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    start_content = f.read(500).lower() # Читаем первые 500 символов
                    
                    # Ищем признаки ошибок
                    is_error = any(marker in start_content for marker in error_markers)
                    
                    if is_error:
                        results.append(f"❌ [red]{filename}[/red] - Похоже на ошибку HTML/404")
                    else:
                        # Если все ок, показываем начало для уверенности
                        snippet = start_content[:50].replace('\n', ' ')
                        results.append(f"✅ [green]{filename}[/green] ({size//1024}KB) - '{snippet}...'")
            except Exception as e:
                results.append(f"⚠️ [yellow]{filename}[/yellow] - Ошибка чтения: {e}")
        else:
            # PDF файлы просто проверяем на размер
            results.append(f"✅ [green]{filename}[/green] ({size//1024}KB) - Бинарный файл (PDF)")

    return "\n".join(results)
