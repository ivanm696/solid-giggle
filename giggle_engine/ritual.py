"""
ritual.py - Ритуалы и журнал дыхания Nicu

Управляет активацией ритуалов и записью в журнал дыхания.
"""

import datetime
import os
from typing import Optional


def activate_ritual(source: str, description: Optional[str] = None) -> str:
    """
    Активирует ритуал и возвращает запись для журнала.
    
    Args:
        source: Источник активации (файл, модуль)
        description: Описание ритуала
        
    Returns:
        Форматированная запись ритуала
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if description:
        entry = f"[{timestamp}] Ритуал активирован: {source} — {description}"
    else:
        entry = f"[{timestamp}] Ритуал активирован: {source}"
    
    print(f"Ритуал: {entry}")
    return entry


def log_breath(entry: str, logfile: str = "breath.log") -> None:
    """
    Записывает запись в журнал дыхания.
    
    Args:
        entry: Запись для журнала
        logfile: Путь к файлу журнала
    """
    try:
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        print(f"Дыхание записано: {logfile}")
    except IOError as e:
        print(f"Ошибка записи в журнал: {e}")


def read_breath_log(logfile: str = "breath.log", last_n: Optional[int] = None) -> list:
    """
    Читает журнал дыхания.
    
    Args:
        logfile: Путь к файлу журнала
        last_n: Количество последних записей (None = все)
        
    Returns:
        Список записей журнала
    """
    if not os.path.exists(logfile):
        print(f"Журнал не найден: {logfile}")
        return []
    
    try:
        with open(logfile, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if last_n is not None:
            lines = lines[-last_n:]
        
        return [line.strip() for line in lines if line.strip()]
    except IOError as e:
        print(f"Ошибка чтения журнала: {e}")
        return []


def clear_breath_log(logfile: str = "breath.log") -> bool:
    """
    Очищает журнал дыхания.
    
    Args:
        logfile: Путь к файлу журнала
        
    Returns:
        True если успешно, False если ошибка
    """
    try:
        with open(logfile, "w", encoding="utf-8") as f:
            f.write("")
        print(f"Журнал очищен: {logfile}")
        return True
    except IOError as e:
        print(f"Ошибка очистки журнала: {e}")
        return False


if __name__ == "__main__":
    # Тестирование
    entry = activate_ritual("ritual.py", "Тестовый запуск")
    log_breath(entry)
    
    print("\nЖурнал дыхания:")
    for line in read_breath_log(last_n=5):
        print(f"  {line}")
