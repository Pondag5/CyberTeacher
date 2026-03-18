"""
Модуль новостей
"""

import json
import logging
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

NEWS_CACHE = "./knowledge_base/news_cache.json"
NEWS_DIR = "./knowledge_base/news"

SOURCES = [
    {"name": "SecurityWeek", "url": "https://www.securityweek.com/feed/"},
    {
        "name": "CISA",
        "url": "https://www.cisa.gov/news-events/cybersecurity-advisories.xml",
    },
]


def fetch_news(force=False):
    """Получить новости"""
    cache = {"news": [], "last": None}

    if os.path.exists(NEWS_CACHE):
        try:
            with open(NEWS_CACHE, "r") as f:
                cache = json.load(f)
        except:
            pass

    # Проверить кэш (1 час)
    if not force and cache.get("last"):
        last_time = datetime.fromisoformat(cache["last"])
        if (datetime.now() - last_time).seconds < 3600:
            return cache["news"]

    news = []
    for src in SOURCES:
        try:
            r = requests.get(
                src["url"], timeout=10, headers={"User-Agent": "Mozilla/5.0"}
            )
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")
            for item in items[:5]:
                title = item.find("title")
                link = item.find("link")
                desc = item.find("description") or item.find("summary")
                if title and title.string:
                    news.append(
                        {
                            "title": str(title.string)[:100],
                            "link": str(link.string) if link and link.string else "",
                            "desc": str(desc.string)[:200]
                            if desc and desc.string
                            else "",
                            "source": src["name"],
                        }
                    )
        except Exception:
            pass

    cache["news"] = news[:10]
    cache["last"] = datetime.now().isoformat()

    os.makedirs(NEWS_DIR, exist_ok=True)
    with open(NEWS_CACHE, "w") as f:
        json.dump(cache, f)

    return news


def get_news_text():
    """Получить текст новостей"""
    news = fetch_news()

    if not news:
        return """Пока нет новостей. Но вот что важно знать:

1. SQL-инъекции - классика, но всё ещё работают
2. XSS - в каждом втором сайте
3. Социальная инженерия - самый слабый элемент
4. Обновляй софт! Большинство взломов - через известные уязвимости

Спроси меня о любой из этих тем!"""

    text = "НОВОСТИ:\n\n"
    for n in news:
        text += f"- {n['title']}\n"
        if n.get("desc"):
            text += f"  {n['desc']}\n"
        if n.get("link"):
            text += f"  Ссылка: {n['link']}\n"
    text += "\nСпроси меня подробнее о любой новости!"
    return text
