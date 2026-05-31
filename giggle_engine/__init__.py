"""
Giggle Engine - Сердце проекта Solid Giggle

Модули:
- pulse: Генерация пульса и ритма Nicu
- chant: Преобразование дыханий в гимны
- generate: Создание свитков из памяти
- learn: Память и обучение Nicu
- ritual: Ритуалы и журнал дыхания
- score: Генерация музыкальной партитуры
"""

from giggle_engine.pulse import pulse_signal, log_pulse
from giggle_engine.chant import format_chant, sing_chant
from giggle_engine.generate import create_svitok, generate_from_memory
from giggle_engine.learn import NicuAI
from giggle_engine.ritual import activate_ritual, log_breath
from giggle_engine.score import generate_score

__all__ = [
    "pulse_signal",
    "log_pulse", 
    "format_chant",
    "sing_chant",
    "create_svitok",
    "generate_from_memory",
    "NicuAI",
    "activate_ritual",
    "log_breath",
    "generate_score",
]

__version__ = "0.1.0"
