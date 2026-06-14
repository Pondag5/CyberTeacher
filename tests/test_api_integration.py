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
        course_id = "web-basics"
        response = self.client.post(f"/api/courses/{course_id}/select")
        self.assertEqual(response.status_code, 200)

        # Проверяем, что состояние обновилось
        self.assertEqual(self.state.current_course, course_id)

    def test_quiz_result_endpoint(self):
        """Тест: POST /api/quiz/result записывает слабые темы."""
        # Отправляем плохой результат (<60%)
        payload = {"topic": "SQLi", "score": 2, "total": 10}
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
    """E2E тесты API для полного цикла обучения."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_cycle.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_cycle_state.json")

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
        # 1. Выбираем курс (должен существовать в COURSES)
        response = self.client.post("/api/courses/web-basics/select")
        self.assertEqual(response.status_code, 200)

        # 2. Проверяем прогресс
        response = self.client.get("/api/progress")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["current_course"], "web-basics")

        # 3. Отправляем результат квиза (плохой)
        response = self.client.post(
            "/api/quiz/result", json={"topic": "xss", "score": 3, "total": 10}
        )
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
        payload = {"message": "Что такое SQL-инъекция?", "mode": "teacher"}
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)


class TestAPIFeatureFlagsE2E(unittest.TestCase):
    """E2E тесты API переключения feature flags."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_features.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_features_state.json")

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
        self.state.feature_flags = {}
        self.state.save_to_file()

    def test_feature_flags_toggle_cycle(self):
        """E2E: Включение/выключение feature flag через API."""
        feature_id = "voice"

        # 1. Проверяем начальное состояние (нет в config)
        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        config_before = response.json()
        self.assertIn("feature_flags", config_before)
        flags = config_before["feature_flags"]
        self.assertNotIn(feature_id, flags)

        # 2. Выключаем feature
        response = self.client.post(f"/api/features/toggle?feature={feature_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["feature"], feature_id)
        self.assertFalse(data["enabled"])

        # 3. Проверяем что сохранилось в state
        self.assertIn(feature_id, self.state.feature_flags)
        self.assertFalse(self.state.feature_flags[feature_id])

        # 4. Проверяем что config отражает изменение
        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["feature_flags"].get(feature_id, True))

        # 5. Включаем обратно
        response = self.client.post(f"/api/features/toggle?feature={feature_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["enabled"])

    def test_feature_flags_multiple(self):
        """Тест: переключение нескольких feature flags."""
        features = ["voice", "hints", "news", "sandbox", "shop"]
        for i, feat in enumerate(features):
            enabled = i % 2 == 0
            self.state.feature_flags[feat] = enabled
        self.state.save_to_file()

        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        flags = response.json()["feature_flags"]
        for i, feat in enumerate(features):
            expected = i % 2 == 0
            self.assertEqual(flags.get(feat, True), expected)


class TestAPIQuizFallbackE2E(unittest.TestCase):
    """E2E тесты генерации квиза с fallback (без LLM)."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_quiz_fb.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_quiz_fb_state.json")

        os.environ["DB_FILE"] = cls.db_path
        os.environ["STATE_FILE"] = cls.state_path
        os.environ["LLM_PROVIDER"] = "mock"

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

    def test_quiz_generate_fallback_local(self):
        """E2E: Генерация квиза возвращает локальные вопросы (source=local)."""
        response = self.client.post(
            "/api/quiz/generate", json={"topic": "general", "count": 3}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("questions", data)
        self.assertEqual(len(data["questions"]), 3)
        self.assertIn("source", data)
        # LLM mock отсутствует → должен быть local fallback
        self.assertIn(data["source"], ("local", "local_fallback"))
        for q in data["questions"]:
            self.assertIn("question", q)
            self.assertIn("options", q)
            self.assertIn("correct", q)
            self.assertIn("explanation", q)

    def test_quiz_generate_networking_topic(self):
        """Тест: генерация квиза по теме networking."""
        response = self.client.post(
            "/api/quiz/generate", json={"topic": "networking", "count": 2}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["questions"]), 2)
        self.assertIn("source", data)

    def test_quiz_generate_invalid_topic_fallback(self):
        """Тест: неизвестная тема падает на general fallback."""
        response = self.client.post(
            "/api/quiz/generate", json={"topic": "nonexistent_topic_xyz", "count": 1}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["questions"]), 1)


class TestAPIContextBudgetE2E(unittest.TestCase):
    """E2E тесты Context Budget Manager через API."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_budget.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_budget_state.json")

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

    def test_context_budget_get_stats(self):
        """E2E: GET /api/context/budget возвращает статистику."""
        response = self.client.get("/api/context/budget")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("available", data)
        self.assertIn("stats", data)
        stats = data["stats"]
        self.assertIn("max_tokens", stats)
        self.assertIn("total_calls", stats)
        self.assertIn("total_trims", stats)
        self.assertIn("history_budget", stats)

    def test_context_budget_configure(self):
        """E2E: POST /api/context/budget изменяет конфигурацию."""
        new_config = {
            "max_tokens": 4000,
            "system_prompt_tokens": 1000,
            "rag_context_tokens": 1000,
            "response_reserve": 512,
        }
        response = self.client.post("/api/context/budget", json=new_config)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        config = data["config"]
        self.assertEqual(config["max_tokens"], 4000)
        self.assertEqual(config["system_prompt_tokens"], 1000)

        # Verify via GET
        response = self.client.get("/api/context/budget")
        self.assertEqual(response.json()["stats"]["max_tokens"], 4000)

    def test_context_history_endpoint(self):
        """E2E: GET /api/context/history возвращает историю."""
        response = self.client.get("/api/context/history?limit=5")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("history", data)
        self.assertIn("budget", data)
        self.assertIsInstance(data["history"], list)


if __name__ == "__main__":
    unittest.main()
