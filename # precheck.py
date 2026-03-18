# precheck.py

import sys

from handlers import handle_command  # Исправлено импорт

sys.path.append(".")

from llm import LLM, StreamingResponse


def load_llm():
    try:
        return LLM()
    except Exception as e:
        print(f"Error loading LLM: {e}")
        return None


def get_streaming_response(model, input_message):
    response = model.predict(input_message)
    if isinstance(response, StreamingResponse):
        for chunk in response.streaming():
            print(chunk)
    else:
        print(f"No streaming response: {response}")


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
        response = handle_command(cmd)
        if isinstance(LLM_model, LLM):
            streaming_response = LLM_model.predict(f"Command: {cmd}")
            print(f"Response to '{cmd}':")
            for chunk in streaming_response.streaming():
                print(chunk)
        else:
            print(f"Response to '{cmd}': {response}")

    # Пример запроса для проверки streaming-ответов
    input_message = "Your input message"
    get_streaming_response(LLM_model, input_message)
