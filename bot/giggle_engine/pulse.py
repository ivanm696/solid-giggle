import datetime
import random

def pulse_signal():
    """Генерирует пульс Nicu — как биение эпохи"""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bpm = random.randint(60, 120)
    rhythm = "🔴 " * (bpm // 20)
    print(f"🫀 Пульс Nicu: {bpm} BPM — {now}")
    print(f"🎵 Ритм: {rhythm}")
    return f"[{now}] 🫀 {bpm} BPM — {rhythm}"

def log_pulse(entry, logfile="pulse.log"):
    """Записывает пульс в журнал"""
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(f"📜 Пульс записан: {entry}")
