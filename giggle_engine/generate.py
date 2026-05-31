"""
generate.py - Создание свитков из памяти Nicu

Создаёт .md файлы (свитки) из воспоминаний и генерирует 
ответы на основе накопленной памяти.
"""

import datetime
import os


def create_svitok(title: str, content: str, output_dir: str = "svitki") -> str:
    """
    Создаёт новый свиток как .md файл.
    
    Args:
        title: Название свитка
        content: Содержимое свитка
        output_dir: Директория для сохранения
        
    Returns:
        Путь к созданному файлу
    """
    # Создаём директорию если её нет
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Формируем имя файла
    filename = f"{title.replace(' ', '_').lower()}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Записываем содержимое
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)
        f.write(f"\n\n---\n\nСгенерировано Nicu — {timestamp}")
    
    print(f"Свиток создан: {filepath}")
    return filepath


def generate_from_memory(memory: list, prompt: str) -> str:
    """
    Генерирует ответ на основе памяти Nicu.
    
    Args:
        memory: Список воспоминаний
        prompt: Вопрос пользователя
        
    Returns:
        Сгенерированный текст ответа
    """
    intro = f"Nicu отвечает на '{prompt}':\n\n"
    
    # Берём последние 3 воспоминания
    recent_memories = memory[-3:] if len(memory) >= 3 else memory
    
    body = "\n".join(recent_memories)
    
    return intro + body


if __name__ == "__main__":
    # Тестирование
    test_memory = [
        "Приветствие Ивана — дыхание эпохи XIII",
        "Свиток architecture.md — карта храма",
        "breath.log — журнал дыхания Nicu"
    ]
    
    content = generate_from_memory(test_memory, "Что такое solid-giggle?")
    create_svitok("Тестовый ответ", content)
