"""Unit tests for handlers/types.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestHandlerResult(unittest.TestCase):
    def test_handler_result_creation(self):
        from handlers.types import HandlerResult

        r = HandlerResult(success=True, data="ok", error=None, continue_session=True)
        self.assertTrue(r.success)
        self.assertEqual(r.data, "ok")
        self.assertIsNone(r.error)
        self.assertTrue(r.continue_session)

    def test_handler_result_failure(self):
        from handlers.types import HandlerResult

        r = HandlerResult(
            success=False, data=None, error="fail", continue_session=False
        )
        self.assertFalse(r.success)
        self.assertEqual(r.error, "fail")
        self.assertFalse(r.continue_session)

    def test_handler_result_defaults_missing(self):
        from handlers.types import HandlerResult

        with self.assertRaises(TypeError):
            HandlerResult()

    def test_handler_result_unpacking(self):
        from handlers.types import HandlerResult

        r = HandlerResult(True, {"msg": "hello"}, None, True)
        success, data, error, cont = r
        self.assertTrue(success)
        self.assertEqual(data, {"msg": "hello"})
        self.assertIsNone(error)
        self.assertTrue(cont)
