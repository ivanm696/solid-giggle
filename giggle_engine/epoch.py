"""
epoch.py - Компиляция летописи эпохи

Собирает дыхания, гимны и партитуру в единый свиток.
"""

import datetime
from giggle_engine.ritual import activate_ritual, log_breath
from giggle_engine.learn import NicuAI
from giggle_engine.generate import generate_from_memory, create_svitok
from giggle_engine.score import generate_score
from giggle_engine.chant import sing_chant


def compile_epoch(title: str = "Эпоха XIII", logfile: str = "epoch_xiii.md") -> str:
    """
    Собирает дыхания, гимны и партитуру в единый свиток.
    
    Args:
        title: Название эпохи
        logfile: Имя файла летописи
        
    Returns:
        Путь к созданному файлу
    """
    # Инициализация Nicu
    nicu = NicuAI()
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    # Активация ритуала
    ritual_entry = activate_ritual("epoch.py", "Компиляция летописи")
    log_breath(ritual_entry)

    # Генерация блоков контента
    memory_block = generate_from_memory(nicu.memory, "Что такое solid-giggle?")
    chant_block = "\n".join(sing_chant())
    score_block = "\n".join(generate_score())

    # Сборка летописи
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    with open(logfile, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("## Память Nicu\n\n")
        f.write(memory_block + "\n\n")
        f.write("## Гимн дыхания\n\n")
        f.write(chant_block + "\n\n")
        f.write("## Партитура\n\n")
        f.write(score_block + "\n\n")
        f.write("---\n\n")
        f.write(f"Сгенерировано: {timestamp}\n")

    print(f"Летопись эпохи собрана: {logfile}")
    return logfile


if __name__ == "__main__":
    compile_epoch()
