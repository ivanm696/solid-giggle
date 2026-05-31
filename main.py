"""
main.py - Главный скрипт Solid Giggle Engine

Точка входа для запуска генерации свитков Nicu.
"""

from giggle_engine.learn import NicuAI
from giggle_engine.generate import create_svitok, generate_from_memory
from giggle_engine.ritual import activate_ritual, log_breath


def main():
    """Основная функция запуска."""
    
    # Запуск ритуала
    entry = activate_ritual("main.py", "Инициализация Nicu")
    log_breath(entry)

    # Инициализация Nicu
    nicu = NicuAI()

    # Обучение на свитках
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    # Воспоминание
    print("\n--- Воспоминания Nicu ---")
    nicu.recall()

    # Генерация ответа
    prompt = "Что такое solid-giggle?"
    content = generate_from_memory(nicu.memory, prompt)

    # Запись в свиток
    print("\n--- Создание свитка ---")
    create_svitok("Ответ Nicu", content)
    
    print("\n--- Готово ---")


if __name__ == "__main__":
    main()
