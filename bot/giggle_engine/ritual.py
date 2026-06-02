import datetime

def activate_ritual(name):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🔔 Ритуал '{name}' активирован в {timestamp}")
    return f"[{timestamp}] 🔔 Ритуал '{name}' активирован"

def log_breath(entry, logfile="breath.log"):
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(f"🌿 Дыхание записано: {entry}")import datetime

def activate_ritual(name):
    """Активирует ритуал и возвращает дыхание"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🔔 Ритуал '{name}' активирован в {timestamp}")
    return f"[{timestamp}] 🔔 Ритуал '{name}' активирован"

def log_breath(entry, logfile="breath.log"):
    """Записывает дыхание в журнал"""
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(f"🌿 Дыхание записано: {entry}")