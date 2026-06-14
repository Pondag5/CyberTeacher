"""Tests for Auth, Roles, Course Management."""

import os
import tempfile
import time
import unittest


class TestAuth(unittest.TestCase):
    """Tests for auth system."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.users_file = os.path.join(self.tmpdir, "users.json")
        import auth

        auth.USERS_FILE = self.users_file

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_create_user(self):
        from auth import create_user

        result = create_user("testuser", "pass1234", "Test User")
        self.assertNotIn("error", result)
        self.assertEqual(result["username"], "testuser")
        self.assertEqual(result["role"], "admin")

    def test_duplicate_user(self):
        from auth import create_user

        create_user("testuser", "pass1234")
        result = create_user("testuser", "other")
        self.assertIn("error", result)

    def test_authenticate(self):
        from auth import create_user, authenticate

        create_user("testuser", "pass1234")
        result = authenticate("testuser", "pass1234")
        self.assertIn("token", result)
        self.assertEqual(result["role"], "admin")

    def test_authenticate_wrong_password(self):
        from auth import create_user, authenticate

        create_user("testuser", "pass1234")
        result = authenticate("testuser", "wrongpass")
        self.assertIn("error", result)

    def test_jwt_token(self):
        from auth import create_user, authenticate, verify_token

        create_user("testuser", "pass1234")
        auth_result = authenticate("testuser", "pass1234")
        payload = verify_token(auth_result["token"])
        self.assertIsNotNone(payload)
        self.assertEqual(payload["username"], "testuser")
        self.assertEqual(payload["role"], "admin")

    def test_invalid_token(self):
        from auth import verify_token

        self.assertIsNone(verify_token("invalid.token.here"))

    def test_get_user(self):
        from auth import create_user, get_user

        create_user("testuser", "pass1234")
        user = get_user("user_testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "testuser")
        self.assertNotIn("password_hash", user)

    def test_update_user(self):
        from auth import create_user, update_user, get_user

        create_user("testuser", "pass1234")
        update_user("user_testuser", display_name="New Name", avatar="🤖")
        user = get_user("user_testuser")
        self.assertEqual(user["display_name"], "New Name")
        self.assertEqual(user["avatar"], "🤖")


class TestRoles(unittest.TestCase):
    """Tests for role-based access."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.users_file = os.path.join(self.tmpdir, "users.json")
        import auth

        auth.USERS_FILE = self.users_file

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_set_role(self):
        from auth import create_user, set_role

        create_user("testuser", "pass1234")
        self.assertTrue(set_role("user_testuser", "teacher"))

    def test_invalid_role(self):
        from auth import create_user, set_role

        create_user("testuser", "pass1234")
        self.assertFalse(set_role("user_testuser", "hacker"))

    def test_permissions(self):
        from auth import create_user, authenticate, has_permission

        create_user("student1", "pass1234", role="student")
        create_user("teacher1", "pass1234", role="teacher")
        create_user("admin1", "pass1234", role="admin")

        student = authenticate("student1", "pass1234")
        teacher = authenticate("teacher1", "pass1234")
        admin = authenticate("admin1", "pass1234")

        self.assertFalse(has_permission(student["token"], "manage_users"))
        self.assertFalse(has_permission(teacher["token"], "manage_users"))
        self.assertTrue(has_permission(admin["token"], "manage_users"))

        self.assertTrue(has_permission(student["token"], "chat"))
        self.assertTrue(has_permission(teacher["token"], "manage_courses"))
        self.assertTrue(has_permission(admin["token"], "manage_config"))

    def test_list_users(self):
        from auth import create_user, list_users

        create_user("user1", "pass1234", role="student")
        create_user("user2", "pass1234", role="teacher")
        users = list_users()
        self.assertEqual(len(users), 2)
        for u in users:
            self.assertNotIn("password_hash", u)


class TestCourseManager(unittest.TestCase):
    """Tests for course management."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.courses_file = os.path.join(self.tmpdir, "courses.json")
        import course_manager

        course_manager.COURSES_FILE = self.courses_file

    def tearDown(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_default_courses(self):
        from course_manager import get_courses

        courses = get_courses()
        self.assertEqual(len(courses), 6)

    def test_create_course(self):
        from course_manager import create_course, get_courses

        create_course(
            "Advanced Reverse Engineering", "Deep RE techniques", difficulty="expert"
        )
        courses = get_courses()
        self.assertEqual(len(courses), 7)

    def test_update_course(self):
        from course_manager import create_course, update_course, get_course

        create_course("Test Course", "Original desc")
        result = update_course("test_course", description="Updated desc")
        self.assertIsNotNone(result)
        course = get_course("test_course")
        self.assertEqual(course["description"], "Updated desc")

    def test_delete_custom_course(self):
        from course_manager import create_course, delete_course, get_courses

        create_course("Temp Course")
        self.assertTrue(delete_course("temp_course"))
        courses = get_courses()
        self.assertEqual(len(courses), 6)  # back to defaults

    def test_cannot_delete_default(self):
        from course_manager import delete_course

        self.assertFalse(delete_course("web_security"))

    def test_add_remove_topic(self):
        from course_manager import create_course, add_topic, remove_topic, get_course

        create_course("Test Course")
        add_topic("test_course", "new_topic")
        course = get_course("test_course")
        self.assertIn("new_topic", course["topics"])
        remove_topic("test_course", "new_topic")
        course = get_course("test_course")
        self.assertNotIn("new_topic", course["topics"])


class TestAtmosphere(unittest.TestCase):
    """Tests for atmosphere engine (ghost logs, echo, doubt)."""

    def test_ghost_log_probability(self):
        from atmosphere import AtmosphereEngine

        eng = AtmosphereEngine()
        # Should return False most of the time at normal level
        results = [eng.should_show_ghost_log("normal") for _ in range(100)]
        true_count = sum(results)
        self.assertLess(true_count, 30, "Ghost logs should be rare at normal")

    def test_ghost_log_more_frequent_at_dangerous(self):
        from atmosphere import AtmosphereEngine

        eng = AtmosphereEngine()
        # Reset and test that dangerous has higher probability
        eng._ghost_interval = 0
        eng._last_ghost_time = 0
        count = 0
        for _ in range(50):
            eng._last_ghost_time = 0
            eng._ghost_interval = 0
            if eng.should_show_ghost_log("dangerous"):
                count += 1
        self.assertGreater(count, 5, "Ghost logs should be more frequent at dangerous")

    def test_echo_returns_none_no_events(self):
        from atmosphere import AtmosphereEngine

        eng = AtmosphereEngine()
        result = eng.get_echo([])
        self.assertIsNone(result)

    def test_doubt_increases_with_stress(self):
        from atmosphere import AtmosphereEngine

        eng = AtmosphereEngine()
        low_stress = sum(1 for _ in range(500) if eng.should_show_doubt(10, 10))
        high_stress = sum(1 for _ in range(500) if eng.should_show_doubt(80, 80))
        self.assertGreater(high_stress, low_stress)


class TestAdaptiveUI(unittest.TestCase):
    """Tests for adaptive difficulty system."""

    def test_beginner_config(self):
        from adaptive_ui import get_difficulty_config, is_command_available

        config = get_difficulty_config("beginner")
        self.assertFalse(config["cyberpsychosis_enabled"])
        self.assertTrue(is_command_available("quiz", "beginner"))
        self.assertFalse(is_command_available("ctf", "beginner"))

    def test_hardcore_config(self):
        from adaptive_ui import get_difficulty_config, is_command_available

        config = get_difficulty_config("hardcore")
        self.assertTrue(config["cyberpsychosis_enabled"])
        self.assertTrue(is_command_available("ctf", "hardcore"))

    def test_auto_promotion(self):
        from adaptive_ui import check_auto_promotion

        class MockState:
            def __init__(self):
                self.difficulty_level = "beginner"
                self.xp = 600
                self.quizzes_taken = 12
                self.labs_started = 4

        state = MockState()
        result = check_auto_promotion(state)
        self.assertEqual(result, "intermediate")

    def test_no_promotion_when_below_threshold(self):
        from adaptive_ui import check_auto_promotion

        class MockState:
            def __init__(self):
                self.difficulty_level = "beginner"
                self.xp = 100
                self.quizzes_taken = 2
                self.labs_started = 1

        state = MockState()
        result = check_auto_promotion(state)
        self.assertIsNone(result)

    def test_system_prompt_prefix(self):
        from adaptive_ui import get_system_prompt_prefix

        beginner = get_system_prompt_prefix("beginner")
        self.assertIn("BEGINNER", beginner)
        hardcore = get_system_prompt_prefix("hardcore")
        self.assertIn("HARDCORE", hardcore)
        intermediate = get_system_prompt_prefix("intermediate")
        self.assertEqual(intermediate, "")


class TestSmartHints(unittest.TestCase):
    """Tests for smart hints and tutorial."""

    def test_suggest_close_command(self):
        from smart_hints import suggest_command

        result = suggest_command("quz")
        self.assertIsNotNone(result)
        self.assertIn("quiz", result)

    def test_no_suggestion_for_correct_command(self):
        from smart_hints import suggest_command

        result = suggest_command("quiz")
        self.assertIsNone(result)

    def test_tutorial_steps(self):
        from smart_hints import get_tutorial_step, get_total_tutorial_steps

        self.assertEqual(get_total_tutorial_steps(), 4)
        step = get_tutorial_step(0)
        self.assertIsNotNone(step)
        self.assertIn("command", step)
        self.assertIsNone(get_tutorial_step(99))


class TestQuizMultiplayer(unittest.TestCase):
    """Tests for multiplayer quiz system."""

    def test_create_room(self):
        from quiz_multiplayer import create_room, get_room, delete_room

        room = create_room("TEST", "Host")
        self.assertIsNotNone(room)
        self.assertEqual(room.room_id, "TEST")
        self.assertEqual(room.host_name, "Host")
        found = get_room("TEST")
        self.assertEqual(found, room)
        delete_room("TEST")
        self.assertIsNone(get_room("TEST"))

    def test_add_player(self):
        from quiz_multiplayer import create_room, delete_room

        room = create_room("T1", "Host")
        room.add_player("Alice", None)
        room.add_player("Bob", None)
        self.assertEqual(len(room.players), 2)
        delete_room("T1")

    def test_submit_answer(self):
        from quiz_multiplayer import create_room, delete_room

        room = create_room("T2", "Host")
        room.add_player("Alice", None)
        room.set_questions(
            [
                {
                    "question": "2+2=?",
                    "options": ["3", "4", "5"],
                    "correct": 1,
                    "explanation": "Math",
                }
            ]
        )
        room.started = True
        room.current_question = 0
        result = room.submit_answer("Alice", 1)
        self.assertTrue(result["correct"])
        self.assertEqual(room.players["Alice"]["score"], 12)  # 10 + streak bonus 2
        self.assertEqual(room.players["Alice"]["streak"], 1)
        delete_room("T2")

    def test_leaderboard(self):
        from quiz_multiplayer import create_room, delete_room

        room = create_room("T3", "Host")
        room.add_player("Alice", None)
        room.add_player("Bob", None)
        room.players["Alice"]["score"] = 20
        room.players["Bob"]["score"] = 30
        lb = room.get_leaderboard()
        self.assertEqual(lb[0]["name"], "Bob")
        self.assertEqual(lb[0]["score"], 30)
        delete_room("T3")


class TestReportGenerator(unittest.TestCase):
    """Tests for HTML report generation."""

    def test_report_contains_metrics(self):
        from report_generator import generate_report_html

        class MockState:
            xp = 1000
            level = 5
            handle = "Хакер"
            reputation = 150
            quizzes_taken = 20
            labs_started = 8
            total_flags_collected = 5
            skills = {"web_security": {"level": 3, "xp": 150}}
            earned_achievements = ["quiz_taker", "first_flag"]
            weak_topics = [{"topic": "crypto", "success_rate": 45}]

        html = generate_report_html(MockState())
        self.assertIn("1000", html)
        self.assertIn("Хакер", html)
        self.assertIn("web_security", html)
        self.assertIn("quiz_taker", html)
        self.assertIn("crypto", html)


if __name__ == "__main__":
    unittest.main()
