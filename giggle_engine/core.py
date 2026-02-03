# giggle_engine/core.py
import importlib
import pkgutil
import os
from typing import Dict, Any

# Словарь для зарегистрированных плагинов
PLUGINS: Dict[str, Any] = {}

def load_plugins(plugin_package: str = "giggle_engine.plugins"):
    """
    Автоматически загружает все модули из папки plugins.
    Каждый модуль должен иметь функцию register() → возвращает {'name': ..., 'handler': func}
    """
    package_path = importlib.import_module(plugin_package).__path__[0]
    
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        full_module_name = f"{plugin_package}.{module_name}"
        module = importlib.import_module(full_module_name)
        
        if hasattr(module, "register"):
            plugin_info = module.register()
            PLUGINS[plugin_info["name"]] = plugin_info["handler"]
            print(f"Загружен плагин: {plugin_info['name']}")
        else:
            print(f"Модуль {module_name} без register() — пропущен")

# Пример использования в оркестраторе
def process_file(file_path: str, task_type: str = "analyze"):
    if task_type not in PLUGINS:
        raise ValueError(f"Нет плагина для задачи '{task_type}'")
    
    handler = PLUGINS[task_type]
    return handler(file_path)  # каждый плагин возвращает результат
