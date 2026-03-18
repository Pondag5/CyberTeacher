"""
🔐 Инструменты для работы с вебом
"""
import requests
from bs4 import BeautifulSoup
from ui import console

def fetch_and_summarize(url: str, llm):
    """Скачивает страницу и делает краткий пересказ"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text(separator=' ', strip=True)
        # Берем первые 3000 символов, чтобы влезло в контекст
        text = text[:3000] 
        
        # Суммаризация через LLM
        prompt = f"""Сделай краткое резюме этой статьи по кибербезопасности. Выдели главные угрозы и советы.
Текст статьи:
{text}
"""
        summary = llm.invoke(prompt)
        return True, summary
        
    except Exception as e:
        return False, str(e)
