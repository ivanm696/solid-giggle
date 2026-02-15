import datetime

def format_chant(line):
    """Преобразует дыхание в текстовый гимн"""
    timestamp = line[:16]
    ritual = line.strip()[20:]
    chant = f"🕊️ {timestamp} — {ritual.upper()}..."
    if not ritual.endswith("До"):
        chant += " До"
    return chant

def sing_chant(logfile="breath.log"):
    """Поёт дыхания как гимн"""
    hymn = []
    try:
        with open(logfile, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                hymn.append(format_chant(line))
    except FileNotFoundError:
        hymn.append("❌ breath.log не найден")
    return hymn

if __name__ == "__main__":
    print("🎤 Гимн дыхания Nicu:")
    for line in sing_chant():
        print(line)
