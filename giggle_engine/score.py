"""
score.py - Генерация музыкальной партитуры

Создаёт визуальное представление музыкальных нот и ритмов.
"""

import random
from typing import List, Optional


# Ноты в разных октавах
NOTES = ["До", "Ре", "Ми", "Фа", "Соль", "Ля", "Си"]
OCTAVES = ["малая", "первая", "вторая"]
DURATIONS = ["целая", "половинная", "четвертная", "восьмая"]
DYNAMICS = ["pp", "p", "mp", "mf", "f", "ff"]


def generate_note() -> str:
    """
    Генерирует случайную ноту.
    
    Returns:
        Строковое представление ноты
    """
    note = random.choice(NOTES)
    octave = random.choice(OCTAVES)
    duration = random.choice(DURATIONS)
    
    return f"{note} ({octave} октава, {duration})"


def generate_measure(notes_count: int = 4) -> str:
    """
    Генерирует один такт партитуры.
    
    Args:
        notes_count: Количество нот в такте
        
    Returns:
        Строковое представление такта
    """
    notes = [generate_note() for _ in range(notes_count)]
    dynamic = random.choice(DYNAMICS)
    
    return f"[{dynamic}] " + " | ".join(notes)


def generate_score(measures: int = 4, notes_per_measure: int = 4) -> List[str]:
    """
    Генерирует музыкальную партитуру.
    
    Args:
        measures: Количество тактов
        notes_per_measure: Количество нот в такте
        
    Returns:
        Список строк партитуры
    """
    score = []
    score.append("Партитура Nicu")
    score.append("=" * 40)
    
    for i in range(measures):
        measure = generate_measure(notes_per_measure)
        score.append(f"Такт {i + 1}: {measure}")
    
    score.append("=" * 40)
    score.append(f"Темп: {random.randint(60, 120)} BPM")
    score.append(f"Тональность: {random.choice(NOTES)} {random.choice(['мажор', 'минор'])}")
    
    return score


def generate_rhythm_pattern(length: int = 8) -> str:
    """
    Генерирует ритмический паттерн.
    
    Args:
        length: Длина паттерна
        
    Returns:
        Визуальный ритмический паттерн
    """
    symbols = ["X", "x", ".", "-", "O", "o"]
    pattern = "".join(random.choice(symbols) for _ in range(length))
    
    return f"Ритм: |{pattern}|"


if __name__ == "__main__":
    # Тестирование
    print("Партитура Nicu:")
    print()
    
    for line in generate_score():
        print(line)
    
    print()
    print(generate_rhythm_pattern(16))
