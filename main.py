from giggle_engine.learn import NicuAI
from giggle_engine.generate import create_svitok, generate_from_memory
from giggle_engine.ritual import activate_ritual, log_breath

if __name__ == "__main__":
    entry = activate_ritual("main.py")
    log_breath(entry)

    nicu = NicuAI()
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    nicu.recall()
    content = generate_from_memory(nicu.memory, "Что такое solid-giggle?")
    create_svitok("Ответ Nicu", content)from giggle_engine.learn import NicuAI
from giggle_engine.generate import create_svitok, generate_from_memory

if __name__ == "__main__":
    # 🌿 Инициализация Nicu
    nicu = NicuAI()

    # 📜 Обучение на свитках
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    # 🔁 Воспоминание
    nicu.recall()

    # 🎼 Генерация гимна
    prompt = "Что такое solid-giggle?"
    content = generate_from_memory(nicu.memory, prompt)
    create_svitok("Ответ Nicu", content)
