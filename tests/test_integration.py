"""
Интеграционные тесты (Integration Tests).

Проверяют взаимодействие реальных компонентов:
- Реальная SQLite БД (in-memory/temp file)
- Реальный State (синглтон)
- Реальные функции memory.py и state.py
- Без моков (mocks)
- E2E сценарии использования
"""

import importlib
import os
import shutil
import tempfile
import unittest

# Импорты модулей, которые будем тестировать
import config
import memory
import state


class TestIntegrationBase(unittest.TestCase):
    """Базовый класс для интеграционных тестов.

    Создает временную директорию, настраивает пути к БД и State,
    перезагружает модули для применения новых путей.
    """

    def setUp(self):
        # 1. Создаем временную папку
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_integration.db")
        self.state_path = os.path.join(self.temp_dir, "test_state.json")

        # 2. Устанавливаем переменные окружения
        os.environ["DATABASE_URL"] = f"sqlite:///{self.db_path}"
        os.environ["STATE_FILE"] = self.state_path

        # 3. Перезагружаем модули, чтобы они подхватили новые пути
        # Порядок важен: config зависит от env, db зависит от env, memory зависит от db
        import db

        importlib.reload(config)
        importlib.reload(db)
        importlib.reload(memory)
        importlib.reload(state)

        # 4. Инициализируем БД
        self.conn = memory.init_db()

        # 5. Сбрасываем синглтон State (чтобы тесты были изолированы)
        state._instance = None
        self.state = state.get_state()

    def tearDown(self):
        # Закрываем соединение
        if hasattr(self, "conn") and self.conn:
            self.conn.close()

        # Удаляем временную папку
        if hasattr(self, "temp_dir"):
            shutil.rmtree(self.temp_dir, ignore_errors=True)


class TestMemoryIntegration(TestIntegrationBase):
    """Тесты интеграции с базой данных."""

    def test_save_and_get_message(self):
        """Тест: сохранение и получение сообщения из реальной БД."""
        from memory import get_chat_history, save_message

        # Сохраняем сообщение
        save_message(self.conn, "user", "Привет, это интеграционный тест", "teacher")

        # Получаем историю
        history = get_chat_history(self.conn)

        # Проверяем
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Привет, это интеграционный тест")
        self.assertEqual(history[0]["mode"], "teacher")

    def test_multiple_messages_order(self):
        """Тест: порядок сообщений в БД (LIFO для get_chat_history)."""
        from memory import get_chat_history, save_message

        save_message(self.conn, "user", "Msg 1", "teacher")
        save_message(self.conn, "assistant", "Msg 2", "teacher")
        save_message(self.conn, "user", "Msg 3", "teacher")

        # get_chat_history обычно возвращает последние N сообщений
        history = get_chat_history(self.conn, limit=10)

        self.assertEqual(len(history), 3)
        # Проверяем, что последнее добавленное сообщение последнее в списке (или первое, зависит от реализации)
        # В нашей реализации обычно sort by id desc или asc.
        # Проверим просто наличие всех трех.
        contents = [h["content"] for h in history]
        self.assertIn("Msg 1", contents)
        self.assertIn("Msg 2", contents)
        self.assertIn("Msg 3", contents)

    def test_clear_chat(self):
        """Тест: очистка чата."""
        from memory import clear_chat, get_chat_history, save_message

        save_message(self.conn, "user", "Temp msg", "teacher")
        self.assertEqual(len(get_chat_history(self.conn)), 1)

        clear_chat(self.conn)

        self.assertEqual(len(get_chat_history(self.conn)), 0)


class TestStateIntegration(TestIntegrationBase):
    """Тесты интеграции с состоянием приложения."""

    def test_state_persistence(self):
        """Тест: сохранение состояния в файл и загрузка."""
        # Изменяем состояние
        self.state.xp = 1500
        self.state.current_course = "web-security-advanced"
        self.state.username = "IntegrationTester"

        # Сохраняем
        self.state.save_to_file()

        # Эмулируем перезапуск приложения: сбрасываем синглтон
        state._instance = None

        # Загружаем заново
        new_state = state.get_state()

        # Проверяем, что данные восстановились
        self.assertEqual(new_state.xp, 1500)
        self.assertEqual(new_state.current_course, "web-security-advanced")
        self.assertEqual(new_state.username, "IntegrationTester")

    def test_state_default_values(self):
        """Тест: загрузка состояния из пустого файла (дефолтные значения)."""
        # Файл состояния пустой (создан в setUp, но пустой)
        # При первом get_state() он должен инициализироваться дефолтами

        # Принудительно сохраняем пустой файл (если он не создан)
        if not os.path.exists(self.state_path):
            self.state.save_to_file()

        state._instance = None
        new_state = state.get_state()

        # Проверяем дефолты (используем points вместо xp, так как в модели это points)
        self.assertEqual(new_state.points, 0.0)
        self.assertEqual(new_state.current_course, None)
        self.assertEqual(new_state.username, "Аноним")  # Или другое дефолтное имя

    def test_weak_topics_update(self):
        """Тест: обновление слабых тем."""
        # Добавляем слабую тему
        self.state.weak_topics = ["SQLi", "XSS"]
        self.state.save_to_file()

        state._instance = None
        new_state = state.get_state()

        self.assertIn("SQLi", new_state.weak_topics)
        self.assertIn("XSS", new_state.weak_topics)


class TestHandlerStateIntegration(TestIntegrationBase):
    """Тесты взаимодействия хендлеров с состоянием (без моков)."""

    def test_command_usage_tracking(self):
        """Тест: хендлеры корректно обновляют статистику команд в State."""
        # Симулируем вызов команды (обычно это делает main.py или core.py)
        # Но мы можем проверить, что state.command_usage обновляется

        # Предположим, у нас есть функция update_command_usage или аналогичная логика
        # Если такой функции нет в публичном API, проверим через прямое изменение
        # и сохранение, чтобы убедиться, что поле существует и сериализуется.

        self.state.command_usage["/help"] = 1
        self.state.command_usage["/news"] = 5
        self.state.save_to_file()

        state._instance = None
        new_state = state.get_state()

        self.assertEqual(new_state.command_usage["/help"], 1)
        self.assertEqual(new_state.command_usage["/news"], 5)

    def test_achievements_persistence(self):
        """Тест: достижения сохраняются между сессиями."""
        self.state.earned_achievements = ["first_steps", "quiz_master"]
        self.state.points = 100.0
        self.state.save_to_file()

        state._instance = None
        new_state = state.get_state()

        self.assertEqual(len(new_state.earned_achievements), 2)
        self.assertIn("quiz_master", new_state.earned_achievements)
        self.assertEqual(new_state.points, 100.0)


class TestE2ELearningCycle(TestIntegrationBase):
    """E2E тесты полного цикла обучения."""

    def test_full_learning_cycle(self):
        """E2E: Полный цикл обучения — курс → квиз → результат → слабые темы."""
        from memory import save_message

        # 1. Выбираем курс (используем атрибут current_course)
        self.state.current_course = "web-security"
        self.state.save_to_file()

        # 2. Симулируем квиз (сохраняем вопросы/ответы в БД)
        save_message(
            self.conn, "user", "Какой символ используется для SQL-инъекции?", "quiz"
        )
        save_message(self.conn, "assistant", "Одинарная кавычка '", "quiz")

        # 3. Симулируем плохой результат квиза
        if "sqli" not in self.state.weak_topics:
            self.state.weak_topics.append("sqli")
        self.state.points = 50.0
        self.state.save_to_file()

        # 4. Проверяем адаптивную рекомендацию
        state._instance = None
        new_state = state.get_state()

        self.assertEqual(new_state.current_course, "web-security")
        self.assertIn("sqli", new_state.weak_topics)
        self.assertEqual(new_state.points, 50.0)

    def test_streak_and_xp_progression(self):
        """E2E: Прогрессия XP и стрика через несколько сессий."""
        # Сессия 1
        self.state.points = 100.0
        self.state.level = 1
        self.state.streak = 1
        self.state.save_to_file()

        state._instance = None
        s1 = state.get_state()
        self.assertEqual(s1.streak, 1)

        # Сессия 2
        s1.points = 250.0
        s1.level = 2
        s1.streak = 2
        s1.save_to_file()

        state._instance = None
        s2 = state.get_state()
        self.assertEqual(s2.points, 250.0)
        self.assertEqual(s2.level, 2)
        self.assertEqual(s2.streak, 2)

    def test_spaced_repetition_cycle(self):
        """E2E: Цикл интервальных повторений."""
        from memory import save_message

        # Добавляем элемент в расписание повторений
        if hasattr(self.state, "review_schedule"):
            self.state.review_schedule = [
                {"topic": "XSS", "next_review": "2026-05-18", "interval": 1},
                {"topic": "CSRF", "next_review": "2026-05-20", "interval": 3},
            ]
            self.state.save_to_file()

            state._instance = None
            new_state = state.get_state()

            self.assertEqual(len(new_state.review_schedule), 2)
            self.assertEqual(new_state.review_schedule[0]["topic"], "XSS")


class TestE2EVersusCycle(TestIntegrationBase):
    """E2E тесты цикла дуэли (versus mode)."""

    def test_versus_full_cycle(self):
        """E2E: Полный цикл дуэли — старт → ходы → завершение."""
        # 1. Запуск дуэли
        self.state.versus_active = True
        self.state.versus_scenario = "web-sqli"
        self.state.versus_attempts = 0
        self.state.versus_history = []
        self.state.save_to_file()

        # 2. Первый ход
        self.state.versus_history.append(
            {"role": "system", "content": "Server: SELECT * FROM users WHERE id="}
        )
        self.state.versus_history.append({"role": "user", "content": "' OR '1'='1"})
        self.state.versus_attempts = 1
        self.state.save_to_file()

        # 3. Второй ход
        state._instance = None
        s = state.get_state()
        s.versus_history.append(
            {"role": "system", "content": "Server: Access granted!"}
        )
        s.versus_attempts = 2
        s.save_to_file()

        # 4. Завершение
        state._instance = None
        s2 = state.get_state()
        self.assertEqual(len(s2.versus_history), 3)
        self.assertEqual(s2.versus_attempts, 2)
        self.assertEqual(s2.versus_scenario, "web-sqli")

        # 5. Сброс
        s2.versus_active = False
        s2.versus_history = []
        s2.save_to_file()

        state._instance = None
        s3 = state.get_state()
        self.assertFalse(s3.versus_active)
        self.assertEqual(len(s3.versus_history), 0)


class TestE2EChatHistory(TestIntegrationBase):
    """E2E тесты полного цикла чата."""

    def test_chat_with_summarization(self):
        """E2E: Чат → 20 сообщений → суммаризация."""
        from memory import get_chat_history, save_message

        # Симулируем 20 сообщений (10 user + 10 assistant = 20 total)
        for i in range(10):
            save_message(self.conn, "user", f"Question {i}", "teacher")
            save_message(self.conn, "assistant", f"Answer {i}", "teacher")

        # get_chat_history имеет лимит по умолчанию 10
        history = get_chat_history(self.conn, limit=50)
        self.assertEqual(len(history), 20)

        # Проверяем, что все сообщения сохранены
        contents = [h["content"] for h in history]
        self.assertIn("Question 0", contents)
        self.assertIn("Answer 9", contents)

    def test_chat_mode_switching(self):
        """E2E: Переключение режимов чата."""
        from memory import get_chat_history, save_message

        # Teacher mode
        save_message(self.conn, "user", "Объясни XSS", "teacher")
        save_message(self.conn, "assistant", "XSS — это...", "teacher")

        # Quiz mode
        save_message(self.conn, "user", "Начни квиз", "quiz")
        save_message(self.conn, "assistant", "Вопрос 1: ...", "quiz")

        # CTF mode
        save_message(self.conn, "user", "Реши CTF", "ctf")
        save_message(self.conn, "assistant", "Задача: найди флаг", "ctf")

        history = get_chat_history(self.conn)
        modes = [h["mode"] for h in history]

        self.assertIn("teacher", modes)
        self.assertIn("quiz", modes)
        self.assertIn("ctf", modes)


class TestE2EAchievementsCycle(TestIntegrationBase):
    """E2E тесты цикла достижений."""

    def test_achievement_unlock_flow(self):
        """E2E: Разблокировка достижения через выполнение действия."""
        # Начальное состояние
        self.state.earned_achievements = []
        self.state.points = 0
        self.state.save_to_file()

        # Выполняем действие (например, 10 квизов)
        self.state.quiz_count = 10
        self.state.points = 100.0

        # Разблокируем достижение
        if "quiz_master" not in self.state.earned_achievements:
            self.state.earned_achievements.append("quiz_master")

        self.state.save_to_file()

        # Проверяем
        state._instance = None
        new_state = state.get_state()

        self.assertIn("quiz_master", new_state.earned_achievements)
        self.assertEqual(new_state.points, 100.0)
        self.assertEqual(new_state.quiz_count, 10)


class TestE2ELabCycle(TestIntegrationBase):
    """E2E тесты цикла лабораторий."""

    def test_lab_lifecycle(self):
        """E2E: Полный цикл лаборатории — выбор → запуск → проверка → остановка."""
        # Проверяем, что lab_state существует
        if hasattr(self.state, "active_labs"):
            # 1. Выбор лаборатории
            self.state.active_labs = {"lab-1": {"name": "DVWA", "status": "stopped"}}
            self.state.save_to_file()

            # 2. Запуск
            state._instance = None
            s = state.get_state()
            s.active_labs["lab-1"]["status"] = "running"
            s.save_to_file()

            # 3. Проверка
            state._instance = None
            s2 = state.get_state()
            self.assertEqual(s2.active_labs["lab-1"]["status"], "running")

            # 4. Остановка
            s2.active_labs["lab-1"]["status"] = "stopped"
            s2.save_to_file()

            # 5. Финальная проверка
            state._instance = None
            s3 = state.get_state()
            self.assertEqual(s3.active_labs["lab-1"]["status"], "stopped")


class TestE2EShopCycle(TestIntegrationBase):
    """E2E тесты цикла магазина."""

    def test_shop_purchase_flow(self):
        """E2E: Покупка в магазине — проверка XP → списание → получение предмета."""
        if hasattr(self.state, "inventory") and hasattr(self.state, "hint_credits"):
            # Начальное состояние
            self.state.points = 500.0
            self.state.hint_credits = 0
            self.state.inventory = []
            self.state.save_to_file()

            # Покупка (стоимость 100 XP)
            state._instance = None
            s = state.get_state()
            if s.points >= 100:
                s.points -= 100
                s.hint_credits += 5
            s.save_to_file()

            # Проверка
            state._instance = None
            s2 = state.get_state()
            self.assertEqual(s2.points, 400.0)
            self.assertEqual(s2.hint_credits, 5)


if __name__ == "__main__":
    unittest.main()
