import datetime

def activate_ritual(name: str) -> str:
    """Активирует ритуал и возвращает запись дыхания"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f"🔔 Ритуал '{name}' активирован в {timestamp}")
    return f"[{timestamp}] 🔔 Ритуал '{name}' активирован"


def log_breath(entry: str, logfile: str = "breath.log") -> None:
    """Записывает дыхание в журнал"""
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(f"🌿 Дыхание записано: {entry}")
