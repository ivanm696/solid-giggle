from giggle_engine.learn import NicuAI
from giggle_engine.generate import create_svitok, generate_from_memory
from giggle_engine.ritual import activate_ritual, log_breath

if __name__ == "__main__":
    # 🌿 Запуск ритуала
    entry = activate_ritual("main.py")
    log_breath(entry)

    # 📜 Инициализация Nicu
    nicu = NicuAI()

    # 🧩 Обучение на свитках
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    # 🔁 Воспоминание
    nicu.recall()

    # 🎼 Генерация ответа
    prompt = "Что такое solid-giggle?"
    content = generate_from_memory(nicu.memory, prompt)

    # 📜 Запись в свиток
    create_svitok("Ответ Nicu", content)
