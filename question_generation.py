"""
Генерация вопросов и задач
"""

import random

QUIZ_TOPICS = {
    "sql": {
        "question": "Что такое SQL-инъекция?",
        "answer": "Внедрение SQL кода в запрос",
        "key_points": ["внедрение SQL", "небезопасный ввод", "обход аутентификации"],
    },
    "xss": {
        "question": "Что такое XSS?",
        "answer": "Межсайтовый скриптинг",
        "key_points": ["внедрение скрипта", "выполнение в браузере", "cookie кража"],
    },
    "network": {
        "question": "Что такое TCP и UDP?",
        "answer": "Протоколы передачи данных",
        "key_points": ["TCP надежный", "UDP быстрый", "порты"],
    },
    "crypto": {
        "question": "Что такое хеширование?",
        "answer": "Преобразование в строку фикс длины",
        "key_points": ["односторонняя функция", " MD5 SHA", "верификация"],
    },
    "linux": {
        "question": "Какие права доступа в Linux?",
        "answer": "rwx для владельца/группы/остальных",
        "key_points": ["read write execute", "chmod", "владелец файл"],
    },
    "cloud": {
        "question": "Что такое модель ответственности в облаке (Shared Responsibility Model)?",
        "answer": "Провайдер отвечает за инфраструктуру, клиент — за данные и конфигурацию",
        "key_points": ["провайдер инфраструктура", "клиент данные", "IAM конфигурация", "S3 публичный доступ"],
    },
    "mobile": {
        "question": "Какие основные угрозы для мобильных приложений (OWASP Mobile Top 10)?",
        "answer": "Небезопасное хранение данных, слабая криптография, improper platform usage",
        "key_points": ["хранилище данных", "кейлоггинг", "jailbreak root", "SSL pinning", "deep links"],
    },
    "iot": {
        "question": "Почему IoT устройства уязвимы по умолчанию?",
        "answer": "Дефолтные пароли, отсутствие обновлений, незащищённые протоколы",
        "key_points": ["дефолтные пароли", "нет обновлений", "telnet", "hardcoded credentials", "ботнеты"],
    },
    "blockchain": {
        "question": "Какие уязвимости характерны для смарт-контрактов?",
        "answer": "Reentrancy, integer overflow, access control flaws",
        "key_points": ["reentrancy", "overflow underflow", "access control", "flash loan", "front-running"],
    },
    "api": {
        "question": "Что такое BOLA/IDOR в API безопасности?",
        "answer": "Broken Object Level Authorization — доступ к объектам другого пользователя через изменение ID",
        "key_points": ["авторизация", "ID пользователя", "горизонтальный доступ", "OWASP API1"],
    },
    "phishing": {
        "question": "Какие признаки фишингового письма?",
        "answer": "Поддельный отправитель, срочность, подозрительные ссылки, вложения",
        "key_points": ["spoofing", "срочность угроза", "ссылка домен", "вложения макросы", "social engineering"],
    },
    "forensics": {
        "question": "Что такое цепочка сохранности (Chain of Custody) в цифровой криминалистике?",
        "answer": "Документированная история обработки доказательств от изъятия до суда",
        "key_points": ["документирование", "хеш образ", "неизменность", "кто когда доступ"],
    },
}


def generate_open_quiz(conn=None, topic=""):
    """Генерация вопроса"""
    if not topic:
        topic = random.choice(list(QUIZ_TOPICS.keys()))
    elif topic.lower() not in QUIZ_TOPICS:
        # Ищем похожий
        for k in QUIZ_TOPICS:
            if k in topic.lower():
                topic = k
                break
        else:
            topic = random.choice(list(QUIZ_TOPICS.keys()))

    q = QUIZ_TOPICS[topic]
    return {
        "question": q["question"],
        "answer": q["answer"],
        "key_points": q["key_points"],
        "topic": topic,
    }


def check_open_answer(question, user_answer, key_points, topic="общий"):
    """Проверка ответа с помощью LLM для понимания смысла"""
    from config import LazyLoader

    llm = LazyLoader.get_llm()

    prompt = f"""Ты - учитель кибербезопасности. Оцени ответ ученика на вопрос квиза.
Вопрос: {question}
Правильный ответ должен содержать: {", ".join(key_points)}
Ответ ученика: {user_answer}

Оцени ответ по 10-балльной шкале.
Если ответ верный по смыслу, ставь высокий балл, даже если слова не совпадают.
Верни ТОЛЬКО JSON в формате:
{{"score": число, "feedback": "краткий комментарий на русском в стиле хакера из 90-х"}}
"""
    try:
        # Используем наш OllamaClient
        response = llm.invoke(prompt)
        import json
        import re

        # Ищем JSON в ответе
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            # Парсим JSON и очищаем от возможных лишних кавычек
            res_str = match.group()
            result = json.loads(res_str)
            return {
                "score": result.get("score", 0),
                "feedback": result.get("feedback", "Неплохо..."),
                "matched": [],  # В этой версии не требуется
            }
    except Exception as e:
        print(f"Ошибка проверки LLM: {e}")

    # Фолбек на старую проверку если LLM упал
    user_lower = user_answer.lower()
    score = 0
    for point in key_points:
        if point.lower() in user_lower:
            score += 3

    return {
        "score": min(score, 10),
        "feedback": "Проверка (fallback): перечитай материал."
        if score < 5
        else "Пойдет.",
        "matched": [],
    }


# Для обратной совместимости
generate_quiz = generate_open_quiz
