import base64
import binascii
import codecs
from urllib.parse import unquote


def decode_text(data: str, format_type: str) -> tuple[bool, str]:
    """Декодирование строки"""
    try:
        if format_type in ["base64", "b64"]:
            decoded = base64.b64decode(data).decode("utf-8", errors="replace")
            return True, decoded

        elif format_type in ["hex"]:
            clean_data = data.replace(" ", "").replace("0x", "")
            if len(clean_data) % 2 != 0:
                return False, "❌ Проблема с форматом hex"
            decoded = binascii.unhexlify(clean_data).decode("utf-8", errors="replace")
            return True, decoded

        elif format_type in ["url"]:
            decoded = unquote(data)
            return True, decoded

        elif format_type in ["rot13"]:
            decoded = codecs.encode(data, "rot_13")
            return True, decoded

        elif format_type in ["binary", "bin"]:
            clean_data = data.replace(" ", "")
            if len(clean_data) % 8 != 0:
                return False, "❌ Проблема с форматом bin"
            # Assuming binary string is a sequence of 8-bit characters
            decoded = "".join(
                chr(int(clean_data[i : i + 8], 2)) for i in range(0, len(clean_data), 8)
            )
            return True, decoded

        else:
            return False, f"❌ Неизвестный формат: {format_type}"

    except Exception as e:
        return False, f"❌ Ошибка декодирования: {e!s}"
