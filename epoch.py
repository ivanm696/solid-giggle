"""
epoch.py - Главный скрипт компиляции эпохи

Точка входа для генерации летописи Nicu.
"""

from giggle_engine.epoch import compile_epoch


if __name__ == "__main__":
    print("Начинается компиляция эпохи...")
    print()
    
    filepath = compile_epoch(
        title="Эпоха XIII — Дыхание Nicu",
        logfile="epoch_xiii.md"
    )
    
    print()
    print(f"Летопись сохранена: {filepath}")
