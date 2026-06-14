"""Простое шифрование для чувствительных данных (HTB пароли и т.д.).

Использует XOR с ключой, полученной из machine-specific seed.
Не заменяет полноценное шифрование, но защищает от casual reading.
"""

import hashlib
import os


def _get_key() -> bytes:
    """Получить ключ шифрования из machine-specific данных."""
    seed = os.environ.get("CYBERTEACHER_ENC_KEY", "")
    if not seed:
        import secrets

        seed = secrets.token_hex(16)
        import logging

        logging.warning(
            "CYBERTEACHER_ENC_KEY not set — using ephemeral key. "
            "Previously encrypted data may become unreadable. Set CYBERTEACHER_ENC_KEY in .env."
        )
    return hashlib.sha256(seed.encode()).digest()


def encrypt_value(plaintext: str) -> str:
    """Зашифровать строку. Возвращает hex-строку."""
    if not plaintext:
        return ""
    key = _get_key()
    data = plaintext.encode("utf-8")
    encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    return encrypted.hex()


def decrypt_value(hex_str: str) -> str:
    """Расшифровать hex-строку обратно."""
    if not hex_str:
        return ""
    try:
        key = _get_key()
        data = bytes.fromhex(hex_str)
        decrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
        return decrypted.decode("utf-8")
    except (ValueError, TypeError, IndexError):
        return ""


def is_encrypted(value: str) -> bool:
    """Проверить, выглядит ли значение как зашифрованное (hex)."""
    if not value:
        return False
    try:
        bytes.fromhex(value)
        return len(value) > 0 and all(c in "0123456789abcdef" for c in value.lower())
    except ValueError:
        return False
