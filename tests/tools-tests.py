import unittest
from ..tools import decode_text  # Используем относительный импорт

class TestTools(unittest.TestCase):
    def test_decode_base64(self):
        data = "SGVsbG8gV29ybGQ="
        format_type = "base64"
        success, decoded_text = decode_text(data, format_type)
        self.assertTrue(success)
        self.assertEqual(decoded_text, "Hello world")

    def test_decode_hex(self):
        data = "68656c6c6f"
        format_type = "hex"
        success, decoded_text = decode_text(data, format_type)
        self.assertTrue(success)
        self.assertEqual(decoded_text, "hello")

    def test_decode_url(self):
        data = "%73%6f%6d%20%68%65%79%21"
        format_type = "url"
        success, decoded_text = decode_text(data, format_type)
        self.assertTrue(success)
        self.assertEqual(decoded_text, "som hay!")

    def test_decode_rot13(self):
        data = "Uryyb Jbeyq"
        format_type = "rot13"
        success, decoded_text = decode_text(data, format_type)
        self.assertTrue(success)
        self.assertEqual(decoded_text, "Hello World")

    def test_decode_binary(self):
        data = "0100010001000100010001000100010001000100010001000100010001000100"
        format_type = "binary"
        success, decoded_text = decode_text(data, format_type)
        self.assertTrue(success)
        self.assertEqual(decoded_text, "\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01")

if __name__ == '__main__':
    unittest.main()
