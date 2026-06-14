"""E2E tests: story chapters, risk mechanics, and faction system."""

import importlib
import os
import shutil
import tempfile
import time
import unittest

from fastapi.testclient import TestClient

import api_server
import config
import memory
import state


class TestStoryChaptersE2E(unittest.TestCase):
    """E2E tests for story chapters API."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_chapters.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_chapters_state.json")
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
        self.state.current_chapter = None
        self.state.chapter_completed = {}
        self.state.chapter_artifacts = {}
        self.state.save_to_file()

    def test_get_chapters_list(self):
        response = self.client.get("/api/chapters")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("chapters", data)
        self.assertGreater(len(data["chapters"]), 0)
        ch = data["chapters"][0]
        self.assertIn("id", ch)
        self.assertIn("title", ch)
        self.assertIn("episode_count", ch)

    def test_chapters_have_required_fields(self):
        response = self.client.get("/api/chapters")
        chapters = response.json()["chapters"]
        for ch in chapters:
            self.assertIn("id", ch)
            self.assertIn("title", ch)
            self.assertIn("episode_count", ch)
            self.assertIn("intro", ch)
            self.assertIn("outro", ch)

    def test_start_first_chapter(self):
        response = self.client.post("/api/chapter/start?chapter_id=1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["chapter_id"], 1)
        self.assertIn("intro", data)
        self.assertEqual(self.state.current_chapter, 1)

    def test_start_chapter_prereq_not_met(self):
        self.state.current_chapter = None
        self.state.chapter_completed = {}
        self.state.save_to_file()
        response = self.client.post("/api/chapter/start?chapter_id=2")
        self.assertEqual(response.status_code, 400)


class TestRiskMechanicsE2E(unittest.TestCase):
    """E2E tests for risk mechanics API."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_risk.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_risk_state.json")
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
        self.state.noise_level = 0
        self.state.stealth_mode = False
        self.state.trace_active = False
        self.state.dirty_logs = []
        self.state.digital_debts = 0
        self.state.save_to_file()

    def test_get_noise_default(self):
        response = self.client.get("/api/noise")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("level", data)
        self.assertEqual(data["level"], 0)

    def test_stealth_toggle(self):
        response = self.client.post("/api/stealth/toggle")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("active", data)
        self.assertTrue(self.state.stealth_mode)

    def test_stealth_toggle_off(self):
        self.state.stealth_mode = True
        self.state.save_to_file()
        response = self.client.post("/api/stealth/toggle")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.state.stealth_mode)

    def test_get_trace_inactive(self):
        response = self.client.get("/api/trace")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("active", data)
        self.assertFalse(data["active"])

    def test_get_debts_zero(self):
        response = self.client.get("/api/debts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIsInstance(data["total"], int)

    def test_get_logs_empty(self):
        response = self.client.get("/api/logs")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("count", data)
        self.assertEqual(data["count"], 0)

    def test_wipe_logs(self):
        self.state.dirty_logs = ["test_log_entry"]
        self.state.save_to_file()
        response = self.client.post("/api/logs/wipe")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(len(self.state.dirty_logs), 0)

    def test_cyberpsychosis_endpoint(self):
        response = self.client.get("/api/cyberpsychosis")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("level", data)
        self.assertIn("state", data)
        self.assertIn("stress", data["state"])
        self.assertIn("obsession", data["state"])

    def test_cyberpsychosis_levels(self):
        from cyberpsychosis import get_cyberpsychosis

        cp = get_cyberpsychosis()
        levels = ["normal", "elevated", "critical", "dangerous"]
        self.assertIn(cp.get_level(), levels)


class TestFactionsE2E(unittest.TestCase):
    """E2E tests for faction system API."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_factions.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_factions_state.json")
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
        self.state.faction_reputation = {"rick": 0, "ghost": 0, "archive": 0}
        self.state.faction_chosen = None
        self.state.student_memories = []
        self.state.save_to_file()

    def test_get_factions_default(self):
        response = self.client.get("/api/factions")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rick", data)
        self.assertIn("ghost", data)
        self.assertEqual(data["chosen"], None)

    def test_choose_rick_faction(self):
        response = self.client.post("/api/faction/choose?faction=rick")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(self.state.faction_chosen, "rick")

    def test_choose_ghost_faction(self):
        response = self.client.post("/api/faction/choose?faction=ghost")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.state.faction_chosen, "ghost")

    def test_choose_invalid_faction(self):
        response = self.client.post("/api/faction/choose?faction=invalid")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "error")

    def test_echo_endpoint(self):
        response = self.client.get("/api/echo")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)

    def test_memory_endpoint(self):
        response = self.client.get("/api/memory")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("memories", data)
        self.assertIn("random", data)

    def test_faction_reputation_tracking(self):
        self.state.faction_reputation = {"rick": 10, "ghost": 5, "archive": 3}
        self.state.save_to_file()
        response = self.client.get("/api/factions")
        data = response.json()
        self.assertEqual(data["rick"], 10)
        self.assertEqual(data["ghost"], 5)


class TestStoryFlowE2E(unittest.TestCase):
    """E2E: full story flow — start chapter → complete → next chapter."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_flow.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_flow_state.json")
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
        self.state.current_chapter = None
        self.state.chapter_completed = {}
        self.state.chapter_artifacts = {}
        self.state.save_to_file()

    def test_story_chapter_flow(self):
        imported = importlib.import_module("story_mode")
        if hasattr(imported, "CHAPTERS"):
            chapters = imported.CHAPTERS
            chapter_count = len(chapters)
            self.assertGreater(chapter_count, 0)

    def test_story_api_endpoints_exist(self):
        r1 = self.client.get("/api/story")
        self.assertIn(r1.status_code, (200, 500))
        r2 = self.client.get("/api/chapters")
        self.assertEqual(r2.status_code, 200)

    def test_chapters_7_and_8_exist(self):
        response = self.client.get("/api/chapters")
        chapters = response.json()["chapters"]
        ids = [ch["id"] for ch in chapters]
        self.assertIn(7, ids, "Chapter 7 (Echo's Call) should exist")
        self.assertIn(8, ids, "Chapter 8 (Convergence) should exist")
        ch8 = next(ch for ch in chapters if ch["id"] == 8)
        self.assertIn("Convergence", ch8["title"])

    def test_final_choice_before_ch7(self):
        response = self.client.post("/api/story/final?path=memory")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "error")
        self.assertIn("главу 7", data["message"])


class TestFinalChoiceE2E(unittest.TestCase):
    """E2E tests for the final choice system."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_final.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_final_state.json")
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
        self.state.chapter_completed = [1, 2, 3, 4, 5, 6, 7]
        self.state.chapter_artifacts = [1, 2, 3, 4, 5, 6]
        self.state.final_choice = None
        self.state.save_to_file()

    def test_final_choice_memory_path(self):
        from story_mode import final_choice

        result = final_choice("memory")
        self.assertNotIn("❌", result)
        self.assertIn("Память", result)
        self.assertEqual(self.state.final_choice, "memory")

    def test_final_choice_merge_path(self):
        from story_mode import final_choice

        result = final_choice("merge")
        self.assertNotIn("❌", result)
        self.assertIn("Слияние", result)
        self.assertEqual(self.state.final_choice, "merge")

    def test_final_choice_rewrite_path(self):
        from story_mode import final_choice

        result = final_choice("rewrite")
        self.assertNotIn("❌", result)
        self.assertIn("Перерождение", result)
        self.assertEqual(self.state.final_choice, "rewrite")

    def test_final_choice_rewrite_no_artifacts(self):
        self.state.chapter_artifacts = [1, 2]
        self.state.save_to_file()
        from story_mode import final_choice

        result = final_choice("rewrite")
        self.assertIn("❌", result)
        self.assertIn("6", result)

    def test_final_choice_invalid_path(self):
        from story_mode import final_choice

        result = final_choice("nonexistent")
        self.assertIn("❌", result)

    def test_final_choice_before_ch7(self):
        self.state.chapter_completed = [1, 2, 3, 4, 5]
        self.state.save_to_file()
        from story_mode import final_choice

        result = final_choice("memory")
        self.assertIn("❌", result)
        self.assertIn("главу 7", result)


class TestWatchersCounterattack(unittest.TestCase):
    """E2E tests for Watchers counterattack system."""

    def setUp(self):
        self.state = state.get_state()
        self._saved = {
            "noise_level": self.state.noise_level,
            "risk_level": self.state.risk_level,
            "dirty_logs": list(self.state.dirty_logs),
            "watcher_attack_active": self.state.watcher_attack_active,
            "watcher_attack_until": self.state.watcher_attack_until,
            "last_watcher_attack": self.state.last_watcher_attack,
        }
        self.state.noise_level = 0
        self.state.risk_level = 0
        self.state.dirty_logs = []
        self.state.watcher_attack_active = False
        self.state.watcher_attack_until = 0.0
        self.state.last_watcher_attack = 0.0

    def tearDown(self):
        self.state.noise_level = self._saved["noise_level"]
        self.state.risk_level = self._saved["risk_level"]
        self.state.dirty_logs = self._saved["dirty_logs"]
        self.state.watcher_attack_active = self._saved["watcher_attack_active"]
        self.state.watcher_attack_until = self._saved["watcher_attack_until"]
        self.state.last_watcher_attack = self._saved["last_watcher_attack"]

    def test_watchers_status_no_attack(self):
        from handlers.watchers import get_watchers_status

        status = get_watchers_status()
        self.assertFalse(status["attack_active"])
        self.assertEqual(status["attack_remaining"], 0)

    def test_cannot_trigger_low_noise(self):
        from handlers.watchers import _can_trigger

        self.state.noise_level = 30
        self.state.dirty_logs = [{"source": "test"} for _ in range(5)]
        self.state.risk_level = 80
        result = _can_trigger()
        self.assertFalse(result)

    def test_cannot_trigger_few_logs(self):
        from handlers.watchers import _can_trigger

        self.state.noise_level = 80
        self.state.dirty_logs = []
        self.state.risk_level = 80
        result = _can_trigger()
        self.assertFalse(result)

    def test_can_trigger_all_conditions_met(self):
        from handlers.watchers import _can_trigger

        self.state.noise_level = 80
        self.state.dirty_logs = [{"source": "test"} for _ in range(5)]
        self.state.risk_level = 80
        result = _can_trigger()
        self.assertTrue(result)

    def test_trigger_counterattack_sets_active(self):
        from handlers.watchers import trigger_counterattack, get_watchers_status

        self.state.noise_level = 80
        self.state.dirty_logs = [{"source": "test"} for _ in range(5)]
        self.state.risk_level = 80
        msg = trigger_counterattack()
        self.assertIsNotNone(msg)
        status = get_watchers_status()
        self.assertTrue(status["attack_active"])
        self.assertGreater(status["attack_remaining"], 0)

    def test_counterattack_increases_noise_and_risk(self):
        from handlers.watchers import trigger_counterattack

        self.state.noise_level = 75
        self.state.dirty_logs = [{"source": "test"} for _ in range(5)]
        self.state.risk_level = 60
        trigger_counterattack()
        self.assertGreater(self.state.noise_level, 75)
        self.assertGreater(self.state.risk_level, 60)

    def test_trigger_on_cooldown(self):
        from handlers.watchers import _can_trigger, trigger_counterattack

        self.state.noise_level = 80
        self.state.dirty_logs = [{"source": "test"} for _ in range(5)]
        self.state.risk_level = 80
        trigger_counterattack()
        self.assertFalse(_can_trigger())

    def test_add_noise_triggers_counterattack(self):
        from handlers.noise import add_noise

        self.state.noise_level = 70
        self.state.dirty_logs = [{"source": "test"} for _ in range(5)]
        self.state.risk_level = 60
        result = add_noise(5)
        self.assertIn("Watchers", result)
        self.assertTrue(self.state.watcher_attack_active)


class TestPhantomLabs(unittest.TestCase):
    """Tests for Phantom Labs system."""

    def setUp(self):
        self.state = state.get_state()
        self.state.phantom_labs = []
        self.state.phantom_labs_completed = []

    def test_get_phantom_labs_empty_initially(self):
        from handlers.phantom_lab import get_phantom_labs

        labs = get_phantom_labs()
        self.assertIsInstance(labs, list)

    def test_force_spawn_creates_lab(self):
        from handlers.phantom_lab import force_spawn, get_phantom_labs

        force_spawn()
        labs = get_phantom_labs()
        self.assertEqual(len(labs), 1)
        self.assertIn("lab_id", labs[0])
        self.assertIn("remaining", labs[0])
        self.assertGreater(labs[0]["remaining"], 0)

    def test_force_spawn_respects_max(self):
        from handlers.phantom_lab import force_spawn

        for _ in range(5):
            force_spawn()
        self.assertLessEqual(len(self.state.phantom_labs), 3)

    def test_complete_phantom_lab(self):
        from handlers.phantom_lab import force_spawn, complete_phantom_lab

        force_spawn()
        lab_id = self.state.phantom_labs[0]["lab_id"]
        msg = complete_phantom_lab(lab_id)
        self.assertIsNotNone(msg)
        self.assertIn(lab_id, self.state.phantom_labs_completed)

    def test_complete_unknown_lab_returns_none(self):
        from handlers.phantom_lab import complete_phantom_lab

        msg = complete_phantom_lab("nonexistent")
        self.assertIsNone(msg)

    def test_cleanup_expired_labs(self):
        from handlers.phantom_lab import get_phantom_labs

        self.state.phantom_labs.append(
            {
                "lab_id": "phantom_null",
                "name": "Dead Lab",
                "expires_at": time.time() - 1,
                "completed": False,
            }
        )
        labs = get_phantom_labs()
        self.assertEqual(len(labs), 0)

    def test_force_spawn_returns_message(self):
        from handlers.phantom_lab import force_spawn

        msg = force_spawn()
        self.assertIsNotNone(msg)
        self.assertIn("👻", msg)


class TestSecretRoom(unittest.TestCase):
    """Tests for Secret Room system."""

    def setUp(self):
        self.state = state.get_state()
        self.state.chapter_completed = [1, 2, 3, 4, 5, 6, 7, 8]
        self.state.faction_chosen = "rick"
        self.state.last_watcher_attack = time.time()
        self.state.secret_room_unlocked = False
        self.state.secret_room_expires = 0.0
        self.state.secret_room_visited = False
        self.state.truth_artifact = False

    def test_secret_room_locked_without_conditions(self):
        from handlers.secret_room import check_unlock

        self.state.chapter_completed = [1, 2, 3]
        self.assertFalse(check_unlock(self.state))

    def test_secret_room_unlocks_with_all_conditions(self):
        from handlers.secret_room import check_unlock

        self.assertTrue(check_unlock(self.state))

    def test_secret_room_status_shows_unlocked(self):
        from handlers.secret_room import get_secret_room_status

        status = get_secret_room_status()
        self.assertTrue(status["unlocked"])

    def test_enter_secret_room_grants_artifact(self):
        from handlers.secret_room import enter_secret_room

        enter_secret_room()
        self.assertTrue(self.state.secret_room_visited)
        self.assertTrue(self.state.truth_artifact)

    def test_secret_room_expires(self):
        from handlers.secret_room import get_secret_room_status

        self.state.secret_room_unlocked = True
        self.state.secret_room_expires = time.time() - 1
        status = get_secret_room_status()
        self.assertFalse(status["unlocked"])

    def test_missing_faction_locks_room(self):
        from handlers.secret_room import check_unlock

        self.state.faction_chosen = None
        self.assertFalse(check_unlock(self.state))

    def test_no_watchers_locks_room(self):
        from handlers.secret_room import check_unlock

        self.state.last_watcher_attack = 0.0
        self.assertFalse(check_unlock(self.state))


class TestRewindE2E(unittest.TestCase):
    """E2E tests for the rewind (time machine) feature."""

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = os.path.join(cls.temp_dir, "test_rewind.db")
        cls.state_path = os.path.join(cls.temp_dir, "test_rewind_state.json")
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
        self.state.chapter_completed = [1, 2, 3, 4, 5]
        self.state.current_chapter = 5
        self.state.chapter_artifacts = []
        self.state.story_completed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.state.memorable_events = [
            {"chapter": 3, "text": "Помню как ты взломал хеш"},
            {"chapter": 4, "text": "Отлично справился с SQL-инъекцией"},
            {"chapter": 5, "text": "Ты нашёл секретный файл"},
        ]
        self.state.earned_achievements = []
        self.state.points = 500
        self.state.save_to_file(force=True)

    def test_rewind_requires_chapter_arg(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind")
        self.assertTrue(result[0])

    def test_rewind_invalid_chapter(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind abc")
        self.assertTrue(result[0])

    def test_rewind_uncompleted_chapter_fails(self):
        from handlers.rewind import handle_rewind

        self.state.chapter_completed = [1, 2]
        self.state.save_to_file(force=True)
        result = handle_rewind("rewind 5")
        self.assertTrue(result[0])
        self.assertEqual(self.state.chapter_completed, [1, 2])

    def test_rewind_resets_chapter_progress(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind 3")
        self.assertTrue(result[0])
        self.assertNotIn(3, self.state.chapter_completed)
        self.assertNotIn(4, self.state.chapter_completed)
        self.assertNotIn(5, self.state.chapter_completed)

    def test_rewind_removes_episodes(self):
        from handlers.rewind import handle_rewind

        self.state.story_completed = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
        ]
        self.state.save_to_file(force=True)
        result = handle_rewind("rewind 4")
        self.assertTrue(result[0])
        # chapters 1-3 episodes should remain
        self.assertIn(1, self.state.story_completed)
        self.assertIn(10, self.state.story_completed)
        # chapters 4-5 episodes should be removed
        self.assertNotIn(16, self.state.story_completed)
        self.assertNotIn(19, self.state.story_completed)

    def test_rewind_removes_memories(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind 4")
        self.assertTrue(result[0])
        for event in self.state.memorable_events:
            self.assertLess(event.get("chapter", 0), 4)

    def test_rewind_grants_achievement(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind 3")
        self.assertTrue(result[0])
        self.assertIn("broken_circle", self.state.earned_achievements)

    def test_rewind_adds_xp_for_achievement(self):
        from handlers.rewind import handle_rewind

        old_points = self.state.points
        result = handle_rewind("rewind 3")
        self.assertTrue(result[0])
        self.assertGreater(self.state.points, old_points)

    def test_rewind_resets_current_chapter(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind 3")
        self.assertTrue(result[0])
        self.assertEqual(self.state.current_chapter, 2)

    def test_rewind_on_chapter_1_resets_to_1(self):
        from handlers.rewind import handle_rewind

        result = handle_rewind("rewind 1")
        self.assertTrue(result[0])
        self.assertEqual(self.state.current_chapter, 1)


if __name__ == "__main__":
    unittest.main()
