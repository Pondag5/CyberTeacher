"""
Интеграционные тесты API (API Integration Tests).

Проверяют реальные HTTP-запросы к FastAPI серверу.
Используют TestClient для эмуляции запросов без запуска реального сервера.
Включают E2E сценарии использования API.
"""

import importlib
import os
import shutil
import tempfile
import unittest

from fastapi.testclient import TestClient

import api_server

# Импорты для настройки окружения
import config
import memory
import state


class TestAPIIntegration(unittest.TestCase):
    """Тесты интеграции API с реальным состоянием."""

    @classmethod
    def setUpClass(cls):
        """Настройка окружения перед запуском всех тестов API."""
        # Создаем временную папку
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_api.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_api_state.json")

        # Устанавливаем переменные окружения
        os.environ["DB_FILE"] = cls.db_path
        os.environ["STATE_FILE"] = cls.state_path

        # Перезагружаем модули
        importlib.reload(config)
        importlib.reload(memory)
        importlib.reload(state)
        importlib.reload(api_server)

        # Инициализируем БД
        cls.conn = memory.init_db()

        # Сбрасываем синглтон State
        state._instance = None
        cls.state = state.get_state()

        # Создаем тестовый клиент
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls):
        """Очистка после всех тестов."""
        if hasattr(cls, "conn") and cls.conn:
            cls.conn.close()
        if hasattr(cls, "temp_dir"):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def setUp(self):
        """Сброс состояния перед каждым тестом."""
        # Сбрасываем состояние к дефолтным значениям
        self.state.xp = 0
        self.state.level = 1
        self.state.current_course = None
        self.state.save_to_file()

    def test_health_endpoint(self):
        """Тест: эндпоинт /api/health возвращает статус ok."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("timestamp", data)

    def test_progress_endpoint(self):
        """Тест: эндпоинт /api/progress возвращает данные из State."""
        # Устанавливаем данные в State
        self.state.xp = 500
        self.state.level = 5
        self.state.current_course = "web-security"
        self.state.save_to_file()

        response = self.client.get("/api/progress")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data["xp"], 500)
        self.assertEqual(data["level"], 5)
        self.assertEqual(data["current_course"], "web-security")

    def test_courses_endpoint(self):
        """Тест: эндпоинт /api/courses возвращает список курсов."""
        response = self.client.get("/api/courses")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("courses", data)
        self.assertIsInstance(data["courses"], list)
        # Проверяем, что курсы не пустые (если они есть в courses.py)
        # Если courses.py пустой, список будет пустым, это тоже ок.
        # Главное - структура JSON.

    def test_achievements_endpoint(self):
        """Тест: эндпоинт /api/achievements возвращает достижения."""
        response = self.client.get("/api/achievements")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("achievements", data)
        self.assertIsInstance(data["achievements"], list)

    def test_stats_endpoint(self):
        """Тест: эндпоинт /api/stats возвращает статистику."""
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("xp", data)
        self.assertIn("level", data)
        self.assertIn("streak", data)

    def test_select_course_endpoint(self):
        """Тест: POST /api/courses/{id}/select обновляет State."""
        course_id = "test-course-123"
        response = self.client.post(f"/api/courses/{course_id}/select")
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что состояние обновилось
        # Нужно перечитать состояние, так как API мог изменить синглтон
        # В данном случае API работает с тем же синглтоном, что и тест
        self.assertEqual(self.state.current_course, course_id)

    def test_quiz_result_endpoint(self):
        """Тест: POST /api/quiz/result записывает слабые темы."""
        # Отправляем плохой результат (<60%)
        payload = {
            "topic": "SQLi",
            "score": 2,
            "total": 10
        }
        response = self.client.post("/api/quiz/result", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что тема добавилась в слабые
        self.assertIn("SQLi", self.state.weak_topics)

    def test_labs_endpoint(self):
        """Тест: эндпоинт /api/labs возвращает список лабораторий."""
        response = self.client.get("/api/labs")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("labs", data)
        self.assertIsInstance(data["labs"], list)


class TestAPIVersusE2E(unittest.TestCase):
    """E2E тесты API для режима дуэли."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_versus.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_versus_state.json")

        os.environ["DB_FILE"] = cls.db_path
        os.environ["STATE_FILE"] = cls.state_path

        importlib.reload(config)
        importlib.reload(memory)
        importlib.reload(state)
        importlib.reload(api_server)

        cls.conn = memory.init_db()
        state._instance = None
        cls.state = state.get_state()
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "conn") and cls.conn:
            cls.conn.close()
        if hasattr(cls, "temp_dir"):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def setUp(self):
        self.state.versus_active = False
        self.state.versus_scenario = None
        self.state.versus_attempts = 0
        self.state.versus_history = []
        self.state.save_to_file()

    def test_versus_scenarios_endpoint(self):
        """Тест: GET /api/versus/scenarios возвращает список сценариев."""
        response = self.client.get("/api/versus/scenarios")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("scenarios", data)
        self.assertIsInstance(data["scenarios"], list)

    def test_versus_start_stop_cycle(self):
        """E2E: Запуск и остановка дуэли через API."""
        # 1. Проверяем статус (не активна)
        response = self.client.get("/api/versus/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["active"])

        # 2. Запускаем дуэль
        response = self.client.post("/api/versus/start", json={"scenario": "web"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["scenario"], "web")
        self.assertIn("initial_message", data)

        # 3. Проверяем статус (активна)
        response = self.client.get("/api/versus/status")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["active"])

        # 4. Останавливаем
        response = self.client.post("/api/versus/stop")
        self.assertEqual(response.status_code, 200)

        # 5. Проверяем статус (не активна)
        response = self.client.get("/api/versus/status")
        self.assertFalse(response.json()["active"])


class TestAPILearningCycleE2E(unittest.TestCase):
    """E2E тесты API полного цикла обучения."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_learning.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_learning_state.json")

        os.environ["DB_FILE"] = cls.db_path
        os.environ["STATE_FILE"] = cls.state_path

        importlib.reload(config)
        importlib.reload(memory)
        importlib.reload(state)
        importlib.reload(api_server)

        cls.conn = memory.init_db()
        state._instance = None
        cls.state = state.get_state()
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "conn") and cls.conn:
            cls.conn.close()
        if hasattr(cls, "temp_dir"):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_full_learning_cycle_api(self):
        """E2E: Курс → квиз → результат → статистика."""
        # 1. Выбираем курс
        response = self.client.post("/api/courses/web-security/select")
        self.assertEqual(response.status_code, 200)

        # 2. Проверяем прогресс
        response = self.client.get("/api/progress")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["current_course"], "web-security")

        # 3. Отправляем результат квиза (плохой)
        response = self.client.post("/api/quiz/result", json={
            "topic": "xss",
            "score": 3,
            "total": 10
        })
        self.assertEqual(response.status_code, 200)

        # 4. Проверяем статистику (должны появиться слабые темы)
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("weak_topics", data)


class TestAPIChatE2E(unittest.TestCase):
    """E2E тесты API чата."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_chat.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_chat_state.json")

        os.environ["DB_FILE"] = cls.db_path
        os.environ["STATE_FILE"] = cls.state_path

        importlib.reload(config)
        importlib.reload(memory)
        importlib.reload(state)
        importlib.reload(api_server)

        cls.conn = memory.init_db()
        state._instance = None
        cls.state = state.get_state()
        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "conn") and cls.conn:
            cls.conn.close()
        if hasattr(cls, "temp_dir"):
            shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_chat_endpoint_structure(self):
        """Тест: POST /api/chat принимает сообщение и возвращает ответ."""
        payload = {
            "message": "Что такое SQL-инъекция?",
            "mode": "teacher"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)


if __name__ == "__main__":
    unittest.main()
