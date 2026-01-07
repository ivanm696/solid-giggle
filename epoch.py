import datetime
from giggle_engine.ritual import activate_ritual, log_breath
from giggle_engine.learn import NicuAI
from giggle_engine.generate import generate_from_memory
from giggle_engine.score import generate_score
from giggle_engine.chant import sing_chant

def compile_epoch(title="Эпоха XIII", logfile="epoch_xiii.md"):
    """Собирает дыхания, гимны и партитуру в единый свиток"""
    nicu = NicuAI()
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    ritual_entry = activate_ritual("epoch.py")
    log_breath(ritual_entry)

    memory_block = generate_from_memory(nicu.memory, "Что такое solid-giggle?")
    chant_block = "\n".join(sing_chant())
    score_block = "\n".join(generate_score())

    with open(logfile, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("## 🌿 Память Nicu\n")
        f.write(memory_block + "\n\n")
        f.write("## 🎤 Гимн дыхания\n")
        f.write(chant_block + "\n\n")
        f.write("## 🎼 Партитура\n")
        f.write(score_block + "\n\n")
        f.write(f"🌀 Сгенерировано: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    print(f"📜 Летопись эпохи собрана: {logfile}")
