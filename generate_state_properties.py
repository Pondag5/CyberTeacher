#!/usr/bin/env python3
"""
Генератор свойств для AppState.
Сканирует модели ProgressState, UserState, SettingsState, MetricsState
и создаёт файл state_properties.py со всеми делегирующими свойствами.
"""

import ast
import os
from pathlib import Path

MODELS_DIR = Path("models")
OUTPUT_FILE = Path("state_properties.py")

# Модели и соответствующие им имена файлов (без .py)
MODEL_FILES = {
    "ProgressState": "progress_state",
    "UserState": "user_state",
    "SettingsState": "settings_state",
    "MetricsState": "metrics_state",
}

def get_fields_from_model(model_path: Path) -> dict[str, str]:
    """Извлекает имена полей из Pydantic модели."""
    if not model_path.exists():
        return {}
    with open(model_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    fields = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Находим класс модели (например, ProgressState)
            for body_node in node.body:
                if isinstance(body_node, ast.AnnAssign) and isinstance(body_node.target, ast.Name):
                    field_name = body_node.target.id
                    if field_name.startswith("model_config") or field_name.startswith("_"):
                        continue
                    fields[field_name] = "Any"
                elif isinstance(body_node, ast.Assign):
                    for target in body_node.targets:
                        if isinstance(target, ast.Name) and not target.id.startswith("_"):
                            fields[target.id] = "Any"
    return fields

def generate_properties():
    properties = []
    # Добавляем импорты
    imports = [
        "from typing import Any",
        "",
    ]
    
    total_fields = 0
    for model_name, file_stem in MODEL_FILES.items():
        model_file = MODELS_DIR / f"{file_stem}.py"
        if not model_file.exists():
            print(f"Warning: {model_file} not found, skipping {model_name}")
            continue
        fields = get_fields_from_model(model_file)
        if not fields:
            print(f"Warning: no fields found in {model_file} for {model_name}")
            continue
        
        # Определяем, какой атрибут в AppState соответствует этой модели
        # По соглашению: ProgressState -> progress, UserState -> user, etc.
        attr_name = model_name.replace("State", "").lower()
        
        for field_name in fields:
            prop = f"""    @property
    def {field_name}(self) -> Any:
        return self.{attr_name}.{field_name}
    
    @{field_name}.setter
    def {field_name}(self, value: Any) -> None:
        self.{attr_name}.{field_name} = value
"""
            properties.append(prop)
            total_fields += 1
    
    # Добавим дополнительные свойства/методы из user_state, которые могут понадобиться
    extra = """
    @property
    def get_handle(self) -> str:
        return self.user.get_handle()
    
    @property
    def HANDLES(self) -> list[tuple[int, str]]:
        return self.user.HANDLES
"""
    properties.append(extra)
    
    # Собираем итоговый файл
    content = "# AUTO-GENERATED FILE. DO NOT EDIT.\n"
    content += "# Run 'python generate_state_properties.py' to regenerate.\n\n"
    content += "\n".join(imports) + "\n\n"
    content += "class StatePropertiesMixin:\n"
    content += "".join(properties)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Generated {OUTPUT_FILE} with {total_fields} properties.")

if __name__ == "__main__":
    generate_properties()