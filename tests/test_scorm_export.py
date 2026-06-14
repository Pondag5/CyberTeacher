"""Tests for SCORM export functionality."""

import os
import tempfile
import unittest
import zipfile


class TestSCORMExport(unittest.TestCase):
    """Test SCORM package generation."""

    def test_list_courses(self) -> None:
        """Should list all exportable courses."""
        from scorm_export import list_exportable_courses

        courses = list_exportable_courses()
        self.assertGreater(len(courses), 0)
        ids = [c["id"] for c in courses]
        self.assertIn("web-basics", ids)

    def test_export_creates_zip(self) -> None:
        """Export should create a valid zip file."""
        from scorm_export import export_scorm_package

        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_scorm_package("web-basics", tmpdir)
            self.assertTrue(os.path.exists(path))
            self.assertTrue(path.endswith(".zip"))
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                self.assertIn("imsmanifest.xml", names)
                self.assertIn("index.html", names)
                self.assertIn("css/style.css", names)
                self.assertIn("js/scorm_api.js", names)

    def test_manifest_is_valid_xml(self) -> None:
        """imsmanifest.xml should be valid SCORM 1.2."""
        from scorm_export import export_scorm_package

        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_scorm_package("web-basics", tmpdir)
            with zipfile.ZipFile(path) as zf:
                manifest = zf.read("imsmanifest.xml").decode("utf-8")
                self.assertIn("SCORM", manifest)
                self.assertIn("1.2", manifest)
                self.assertIn("organizations", manifest)
                self.assertIn("resources", manifest)

    def test_export_unknown_course_raises(self) -> None:
        """Unknown course should raise ValueError."""
        from scorm_export import export_scorm_package

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError):
                export_scorm_package("nonexistent_course", tmpdir)

    def test_all_courses_exportable(self) -> None:
        """All listed courses should export successfully."""
        from scorm_export import export_scorm_package, list_exportable_courses

        with tempfile.TemporaryDirectory() as tmpdir:
            for course in list_exportable_courses():
                path = export_scorm_package(course["id"], tmpdir)
                self.assertTrue(os.path.exists(path), f"Failed for {course['id']}")

    def test_scorm_api_js_present(self) -> None:
        """SCORM API wrapper JS should be in the package."""
        from scorm_export import export_scorm_package

        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_scorm_package("web-basics", tmpdir)
            with zipfile.ZipFile(path) as zf:
                js = zf.read("js/scorm_api.js").decode("utf-8")
                self.assertIn("LMSInitialize", js)
                self.assertIn("LMSSetValue", js)
                self.assertIn("cmi.core.lesson_status", js)

    def test_lessons_have_quiz(self) -> None:
        """Each lesson should have a corresponding quiz."""
        from scorm_export import export_scorm_package

        with tempfile.TemporaryDirectory() as tmpdir:
            path = export_scorm_package("web-basics", tmpdir)
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                lessons = [n for n in names if n.startswith("lesson_")]
                quizzes = [n for n in names if n.startswith("quiz_")]
                self.assertEqual(len(lessons), len(quizzes))


class TestSCORMAPI(unittest.TestCase):
    """Test SCORM API endpoints."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.mkdtemp()
        os.environ["DB_FILE"] = os.path.join(cls.temp_dir, "test.db")
        os.environ["STATE_FILE"] = os.path.join(cls.temp_dir, "state.json")
        from fastapi.testclient import TestClient
        import api_server

        cls.client = TestClient(api_server.app)

    @classmethod
    def tearDownClass(cls) -> None:
        import shutil

        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_scorm_courses_list(self) -> None:
        """GET /api/scorm/courses should return course list."""
        r = self.client.get("/api/scorm/courses")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("courses", data)
        self.assertGreater(len(data["courses"]), 0)

    def test_scorm_export_requires_course_id(self) -> None:
        """POST /api/scorm/export without course_id should 400."""
        r = self.client.post("/api/scorm/export")
        self.assertEqual(r.status_code, 400)

    def test_scorm_export_invalid_course(self) -> None:
        """POST /api/scorm/export with bad course_id should 404."""
        r = self.client.post("/api/scorm/export?course_id=nonexistent")
        self.assertEqual(r.status_code, 404)

    def test_scorm_export_valid_course(self) -> None:
        """POST /api/scorm/export should return a zip file."""
        r = self.client.post("/api/scorm/export?course_id=web-basics")
        self.assertEqual(r.status_code, 200)
        self.assertIn("zip", r.headers.get("content-type", ""))


if __name__ == "__main__":
    unittest.main()
