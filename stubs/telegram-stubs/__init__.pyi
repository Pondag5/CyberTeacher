# stubs/telegram-stubs/__init__.pyi
from typing import Any, Callable

class Update:
    message: "Message"

class Message:
    text: str
    chat: "Chat"
    def reply_text(self, text: str) -> Any: ...

class Chat:
    id: int

class Bot:
    def __init__(self, token: str) -> None: ...
    def send_message(self, chat_id: int, text: str) -> Any: ...   # без async

class ContextTypes:
    DEFAULT_TYPE: Any

class Application:
    @staticmethod
    def builder() -> "ApplicationBuilder": ...
    def add_handler(self, handler: Any) -> None: ...
    def run_polling(self) -> None: ...
    def stop(self) -> Any: ...   # без async

class ApplicationBuilder:
    def token(self, token: str) -> "ApplicationBuilder": ...
    def build(self) -> Application: ...

class CommandHandler:
    def __init__(self, command: str, callback: Callable[[Update, Any], Any]) -> None: ...

class MessageHandler:
    def __init__(self, filters: Any, callback: Callable[[Update, Any], Any]) -> None: ...

class filters:
    TEXT: Any
    COMMAND: Any