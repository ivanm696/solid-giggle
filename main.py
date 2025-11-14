from giggle_engine.learn import NicuAI
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
