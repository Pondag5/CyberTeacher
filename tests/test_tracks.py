"""Tests for path-based learning tracks (M-29)"""
# isort: skip_file

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import yaml

from track_engine import Track, TrackTopic, TrackEngine
from state import AppState


class TestTrackModel(unittest.TestCase):
    """Tests for Track, TrackTopic dataclasses"""

    def test_track_topic_creation(self):
        topic = TrackTopic(
            topic_id="sql-injection",
            order=1,
            title="SQL Injection",
            description="Test desc",
            required=True,
            linked_course="web-basics",
            min_score=70.0,
        )
        self.assertEqual(topic.topic_id, "sql-injection")
        self.assertEqual(topic.order, 1)
        self.assertEqual(topic.required, True)
        self.assertEqual(topic.min_score, 70.0)

    def test_track_creation(self):
        topics = [
            TrackTopic("t1", 1, "Topic 1", "Desc", True),
            TrackTopic("t2", 2, "Topic 2", "Desc", False),
        ]
        track = Track(
            id="test-track",
            name="Test Track",
            description="A test track",
            level="beginner",
            prerequisites=["pre-req"],
            topics=topics,
            adaptive=True,
            estimated_hours=5,
        )
        self.assertEqual(track.id, "test-track")
        self.assertEqual(track.level, "beginner")
        self.assertEqual(len(track.topics), 2)
        self.assertTrue(track.adaptive)

    def test_track_get_next_topic_first(self):
        topics = [
            TrackTopic("t1", 1, "Topic 1", "Desc", True),
            TrackTopic("t2", 2, "Topic 2", "Desc", True),
            TrackTopic("t3", 3, "Topic 3", "Desc", False),
        ]
        track = Track("test", "Test", "Test", "beginner", topics=topics)
        next_topic = track.get_next_topic([], 0)
        self.assertEqual(next_topic.topic_id, "t1")

    def test_track_get_next_topic_skip_completed(self):
        topics = [
            TrackTopic("t1", 1, "Topic 1", "Desc", True),
            TrackTopic("t2", 2, "Topic 2", "Desc", True),
        ]
        track = Track("test", "Test", "Test", "beginner", topics=topics)
        next_topic = track.get_next_topic(["t1"], 0)
        self.assertEqual(next_topic.topic_id, "t2")

    def test_track_get_next_topic_beyond_end_returns_none(self):
        topics = [TrackTopic("t1", 1, "Topic 1", "Desc", True)]
        track = Track("test", "Test", "Test", "beginner", topics=topics)
        next_topic = track.get_next_topic(["t1"], 1)
        self.assertIsNone(next_topic)

    def test_track_is_completed(self):
        topics = [
            TrackTopic("t1", 1, "Topic 1", "Desc", True),
            TrackTopic("t2", 2, "Topic 2", "Desc", True),
            TrackTopic("t3", 3, "Topic 3", "Desc", False),
        ]
        track = Track("test", "Test", "Test", "beginner", topics=topics)
        # Completed only required
        self.assertTrue(track.is_completed(["t1", "t2"]))
        # Not all required
        self.assertFalse(track.is_completed(["t1"]))
        # All topics including optional
        self.assertTrue(track.is_completed(["t1", "t2", "t3"]))

    def test_track_progress_counts_only_required(self):
        topics = [
            TrackTopic("t1", 1, "Topic 1", "Desc", True),
            TrackTopic("t2", 2, "Topic 2", "Desc", True),
            TrackTopic("t3", 3, "Topic 3", "Desc", False),
        ]
        track = Track("test", "Test", "Test", "beginner", topics=topics)
        completed, total = track.progress(["t1", "t3"])
        self.assertEqual(completed, 1)
        self.assertEqual(total, 2)

    def test_track_get_topic_by_id(self):
        topics = [
            TrackTopic("sql", 1, "SQLi", "Desc"),
            TrackTopic("xss", 2, "XSS", "Desc"),
        ]
        track = Track("test", "Test", "Test", "beginner", topics=topics)
        topic = track.get_topic_by_id("xss")
        self.assertIsNotNone(topic)
        self.assertEqual(topic.title, "XSS")
        self.assertIsNone(track.get_topic_by_id("nonexistent"))


class TestTrackEngine(unittest.TestCase):
    """Tests for TrackEngine"""

    def setUp(self):
        # Create temporary directory for test YAML tracks
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tracks_dir = self.temp_dir.name

        # Create a sample track YAML file
        self.sample_track_data = {
            "id": "sample-track",
            "name": "Sample Track",
            "description": "A sample track for testing",
            "level": "beginner",
            "adaptive": False,
            "estimated_hours": 3,
            "prerequisites": [],
            "topics": [
                {
                    "topic_id": "topic1",
                    "order": 1,
                    "title": "Topic 1",
                    "description": "First topic",
                    "required": True,
                    "linked_course": "course1",
                    "quiz_topic": "quiz1",
                    "lab_id": "lab1",
                    "min_score": 70.0,
                },
                {
                    "topic_id": "topic2",
                    "order": 2,
                    "title": "Topic 2",
                    "description": "Second topic",
                    "required": False,
                },
            ],
        }
        self.yaml_path = os.path.join(self.tracks_dir, "sample.yaml")
        with open(self.yaml_path, "w") as f:
            yaml.dump(self.sample_track_data, f)

        # Patch TRACKS_DIR in module
        self.engine_patcher = patch("track_engine.TRACKS_DIR", self.tracks_dir)
        self.engine_patcher.start()
        # Reset global engine
        import track_engine

        track_engine._engine = None

    def tearDown(self):
        self.engine_patcher.stop()
        self.temp_dir.cleanup()

    def test_engine_loads_tracks(self):
        engine = TrackEngine(self.tracks_dir)
        self.assertIn("sample-track", engine.tracks)
        track = engine.tracks["sample-track"]
        self.assertEqual(track.name, "Sample Track")
        self.assertEqual(len(track.topics), 2)

    def test_engine_get_track(self):
        engine = TrackEngine(self.tracks_dir)
        track = engine.get_track("sample-track")
        self.assertIsNotNone(track)
        self.assertEqual(track.id, "sample-track")
        self.assertIsNone(engine.get_track("nonexistent"))

    def test_engine_list_tracks(self):
        engine = TrackEngine(self.tracks_dir)
        tracks = engine.list_tracks()
        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].id, "sample-track")

    def test_get_available_tracks_without_prereqs(self):
        engine = TrackEngine(self.tracks_dir)
        available = engine.get_available_tracks([])
        self.assertEqual(len(available), 1)

    def test_get_available_tracks_prereqs_not_met(self):
        track_with_prereq = {
            "id": "track2",
            "name": "Track 2",
            "description": "Needs sample-track",
            "level": "intermediate",
            "prerequisites": ["sample-track"],
            "topics": [{"topic_id": "t", "order": 1, "title": "T", "description": "t"}],
        }
        yaml_path2 = os.path.join(self.tracks_dir, "track2.yaml")
        with open(yaml_path2, "w") as f:
            yaml.dump(track_with_prereq, f)
        # Reload engine
        from track_engine import TrackEngine

        engine = TrackEngine(self.tracks_dir)
        available = engine.get_available_tracks([])  # no completed
        self.assertNotIn("track2", [t.id for t in available])

        available2 = engine.get_available_tracks(["sample-track"])
        self.assertIn("track2", [t.id for t in available2])

    def test_recommend_tracks_by_weak_topics(self):
        engine = TrackEngine(self.tracks_dir)
        weak_topics = [
            {
                "topic": "topic1",
                "success_rate": 50.0,
                "attempts": 2,
                "total_score": 5,
                "max_score": 10,
            },
            {"topic": "unknown", "success_rate": 40.0},
        ]
        completed_tracks = []
        recommendations = engine.recommend_tracks(weak_topics, completed_tracks)
        self.assertGreater(len(recommendations), 0)
        top_track, score = recommendations[0]
        self.assertEqual(top_track.id, "sample-track")
        # Score should be higher because topic1 is covered
        self.assertGreater(score, 0)

    def test_recommend_tracks_beginner_when_no_weak(self):
        engine = TrackEngine(self.tracks_dir)
        recommendations = engine.recommend_tracks([], [])
        self.assertGreater(len(recommendations), 0)

    def test_validate_topic_completion(self):
        track = Track(
            "test",
            "Test",
            "Test",
            "beginner",
            topics=[
                TrackTopic("t1", 1, "T1", "Desc", min_score=75.0),
            ],
        )
        engine = TrackEngine.__new__(TrackEngine)
        # Without score, considered complete
        self.assertTrue(engine.validate_topic_completion(track, "t1"))
        self.assertTrue(engine.validate_topic_completion(track, "t1", score=80.0))
        self.assertFalse(engine.validate_topic_completion(track, "t1", score=60.0))
        self.assertFalse(engine.validate_topic_completion(track, "nonexistent"))


class TestHandlersTracks(unittest.TestCase):
    """Tests for handlers/tracks.py"""

    def setUp(self):
        # Mock state
        self.state_patcher = patch("handlers.tracks.get_state")
        self.mock_get_state = self.state_patcher.start()
        self.mock_state = MagicMock(spec=AppState)
        self.mock_state.tracks_enrolled = []
        self.mock_state.track_progress = {}
        self.mock_state.learning_context = {}
        self.mock_state.points = 0.0
        self.mock_state.save_to_file = MagicMock()
        self.mock_get_state.return_value = self.mock_state

        # Mock track engine
        self.engine_patcher = patch("handlers.tracks.get_track_engine")
        self.mock_get_engine = self.engine_patcher.start()
        self.mock_engine = MagicMock(spec=TrackEngine)
        self.mock_get_engine.return_value = self.mock_engine

        # Sample track
        self.sample_track = Track(
            id="test-track",
            name="Test Track",
            description="Test track",
            level="beginner",
            topics=[
                TrackTopic(
                    "t1", 1, "Topic 1", "Desc", lab_id="lab1", quiz_topic="quiz1"
                ),
                TrackTopic("t2", 2, "Topic 2", "Desc"),
            ],
        )
        self.mock_engine.get_track.return_value = self.sample_track
        self.mock_engine.list_tracks.return_value = [self.sample_track]

        # Patch yaml loading for example tracks if needed
        self.track_engine_patcher = patch("track_engine.TrackEngine.load_all_tracks")
        self.mock_load_all = self.track_engine_patcher.start()
        self.mock_load_all.return_value = None

    def tearDown(self):
        self.state_patcher.stop()
        self.engine_patcher.stop()
        self.track_engine_patcher.stop()

    def test_cmd_tracks_list_empty(self):
        from handlers.tracks import cmd_tracks_list

        self.mock_engine.list_tracks.return_value = []
        success, msg, _ = cmd_tracks_list()
        self.assertTrue(success)
        self.assertIn("не найдены", msg.lower())

    def test_cmd_tracks_list_shows_tracks(self):
        from handlers.tracks import cmd_tracks_list

        success, msg, _ = cmd_tracks_list()
        self.assertTrue(success)
        self.assertIsNotNone(msg)
        # msg is a Panel, we can check that it's truthy
        self.assertTrue(bool(msg))

    def test_cmd_track_start_success(self):
        from handlers.tracks import cmd_track_start

        # Prereqs ok
        self.mock_state.tracks_enrolled = []
        success, msg, _ = cmd_track_start("test-track")
        self.assertTrue(success)
        self.assertIn("ТРЕК НАЧАТ", msg)
        self.assertIn("test-track", self.mock_state.tracks_enrolled)
        self.mock_state.save_to_file.assert_called_once()

    def test_cmd_track_start_missing_id(self):
        from handlers.tracks import cmd_track_start

        success, msg, _ = cmd_track_start("")
        self.assertFalse(success)
        self.assertIn("Укажи ID", msg)

    def test_cmd_track_start_unknown(self):
        from handlers.tracks import cmd_track_start

        self.mock_engine.get_track.return_value = None
        success, msg, _ = cmd_track_start("unknown")
        self.assertFalse(success)
        self.assertIn("не найден", msg.lower())

    def test_cmd_track_start_prereqs_missing(self):
        from handlers.tracks import cmd_track_start

        self.sample_track.prerequisites = ["missing-track"]
        self.mock_state.tracks_enrolled = []
        success, msg, _ = cmd_track_start("test-track")
        self.assertFalse(success)
        self.assertIn("prereq", msg.lower())

    def test_cmd_track_start_already_enrolled(self):
        from handlers.tracks import cmd_track_start

        self.mock_state.tracks_enrolled = ["test-track"]
        self.mock_state.track_progress = {"test-track": {}}
        success, msg, _ = cmd_track_start("test-track")
        self.assertTrue(success)
        self.assertIn("уже начат", msg.lower())

    def test_cmd_track_progress_no_enrolled(self):
        from handlers.tracks import cmd_track_progress

        self.mock_state.tracks_enrolled = []
        success, msg, _ = cmd_track_progress()
        self.assertFalse(success)
        self.assertIn("трека", msg)

    def test_cmd_track_progress_summary(self):
        from handlers.tracks import cmd_track_progress

        self.mock_state.tracks_enrolled = ["test-track"]
        self.mock_state.track_progress = {
            "test-track": {"completed_topics": ["t1"], "current_topic_idx": 1}
        }
        self.sample_track.topics = [
            TrackTopic("t1", 1, "T1", ""),
            TrackTopic("t2", 2, "T2", ""),
        ]
        success, msg, _ = cmd_track_progress()
        self.assertTrue(success)
        # Should show progress 1/2 in the Panel somewhere; we can check msg is truthy
        self.assertTrue(bool(msg))

    def test_cmd_track_next_returns_first_topic(self):
        from handlers.tracks import cmd_track_next

        self.mock_state.tracks_enrolled = ["test-track"]
        self.mock_state.track_progress = {
            "test-track": {"current_topic_idx": 0, "completed_topics": []}
        }
        self.mock_state.learning_context = {}
        success, msg, _ = cmd_track_next()
        self.assertTrue(success)
        self.assertIn("ТЕМА 1", msg)
        self.assertIn("Topic 1", msg)

    def test_cmd_track_next_skips_completed(self):
        from handlers.tracks import cmd_track_next

        self.mock_state.tracks_enrolled = ["test-track"]
        # completed t1, current idx 1 -> should give t2
        self.mock_state.track_progress = {
            "test-track": {"current_topic_idx": 1, "completed_topics": ["t1"]}
        }
        self.mock_state.learning_context = {}
        success, msg, _ = cmd_track_next()
        self.assertTrue(success)
        self.assertIn("ТЕМА 2", msg)
        self.assertIn("Topic 2", msg)

    def test_cmd_track_complete_topic_updates_progress(self):
        from handlers.tracks import cmd_track_complete_topic

        self.mock_state.tracks_enrolled = ["test-track"]
        self.mock_state.track_progress = {
            "test-track": {"completed_topics": [], "current_topic_idx": 0}
        }
        self.mock_state.learning_context = {"current_track": "test-track"}
        success, _, __ = cmd_track_complete_topic("t1")
        self.assertTrue(success)
        # Check that topic was added to completed list
        self.assertIn(
            "t1", self.mock_state.track_progress["test-track"]["completed_topics"]
        )

    def test_cmd_track_recommend(self):
        from handlers.tracks import cmd_track_recommend

        self.mock_state.get_weak_topics.return_value = [
            {
                "topic": "sql",
                "success_rate": 50.0,
                "attempts": 1,
                "total_score": 5,
                "max_score": 10,
            }
        ]
        self.mock_state.tracks_enrolled = []
        # Engine returns recommendations sorted
        self.mock_engine.recommend_tracks.return_value = [(self.sample_track, 5.0)]
        success, msg, _ = cmd_track_recommend()
        self.assertTrue(success)
        self.assertIn("РЕКОМЕНДАЦИИ", msg)
        self.assertIn("Test Track", msg)

    def test_cmd_track_status_no_active(self):
        from handlers.tracks import cmd_track_status

        self.mock_state.learning_context = {}
        self.mock_state.tracks_enrolled = []
        success, msg, _ = cmd_track_status()
        self.assertFalse(success)
        self.assertIn("Нет активного трека", msg)

    def test_cmd_track_status_shows_current(self):
        from handlers.tracks import cmd_track_status

        self.mock_state.learning_context = {"current_track": "test-track"}
        self.mock_state.tracks_enrolled = ["test-track"]
        self.mock_state.track_progress = {
            "test-track": {"current_topic_idx": 0, "completed_topics": []}
        }
        success, msg, _ = cmd_track_status()
        self.assertTrue(success)
        self.assertIn("Test Track", msg)
        self.assertIn("Прогресс", msg)

    def test_cmd_track_reset_removes_progress(self):
        from handlers.tracks import cmd_track_reset

        self.mock_state.tracks_enrolled = ["test-track"]
        self.mock_state.track_progress = {"test-track": {"current_topic_idx": 1}}
        success, _, __ = cmd_track_reset("test-track")
        self.assertTrue(success)
        self.assertNotIn("test-track", self.mock_state.tracks_enrolled)
        self.assertNotIn("test-track", self.mock_state.track_progress)
        self.mock_state.save_to_file.assert_called()


if __name__ == "__main__":
    unittest.main()
