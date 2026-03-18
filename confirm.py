# confirm.py
def confirm(message):
    return input(f"{message} (y/n): ").lower() == "y"
