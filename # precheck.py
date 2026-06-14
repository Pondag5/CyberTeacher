# precheck.py

import sys

from handlers import handle_commands  # Исправлено импорт

sys.path.append(".")


def load_llm():
    try:
        from config import get_llm

        return get_llm()
    except Exception as e:
        print(f"Error loading LLM: {e}")
        return None


def get_streaming_response(model, input_message):
    if hasattr(model, "predict"):
        response = model.predict(input_message)
        print(f"Response: {response}")
    else:
        print(f"No model to get response from: {model}")


if __name__ == "__main__":
    # Проверка загрузки модели
    LLM_model = load_llm()
    if LLM_model is not None:
        print("LLM model loaded successfully")
    else:
        print("Failed to load LLM model")

    # Проверка обработки команд
    command_tests = ["help", "quiz", "stats"]
    for cmd in command_tests:
        result = handle_commands(cmd, None, lambda: LLM_model)
        print(f"Response to '{cmd}': {result}")

    # Пример запроса для проверки streaming-ответов
    input_message = "Your input message"
    get_streaming_response(LLM_model, input_message)
