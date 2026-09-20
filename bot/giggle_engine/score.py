import datetime

def map_to_note(text):
    """Преобразует текст в музыкальные ноты"""
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    return [notes[ord(c) % len(notes)] for c in text if c.isalpha()]

def generate_score(logfile="breath.log"):
    """Создаёт партитуру из дыханий"""
    score = []
    try:
        with open(logfile, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                timestamp = line[:16]
                ritual = line.strip()[20:]
                notes = map_to_note(ritual)
                score.append(f"{timestamp} 🎵 {'-'.join(notes)}")
    except FileNotFoundError:
        print("❌ breath.log не найден")
    return score

if __name__ == "__main__":
    print("🎼 Партитура дыхания Nicu:")
    for line in generate_score():
        print(line)