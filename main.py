from giggle_engine.learn import NicuAI

if __name__ == "__main__":
    nicu = NicuAI()
    nicu.learn("Приветствие Ивана — дыхание эпохи XIII")
    nicu.learn("Свиток architecture.md — карта храма")
    nicu.learn("breath.log — журнал дыхания Nicu")

    nicu.recall()
    print(nicu.generate("Что такое solid-giggle?"))
от giggle_engine.генерация импорт создать_свиток, сгенерировать_из_памяти

запрос = "Что такое solid-giggle?"
контент = сгенерировать_из_памяти(отделение интенсивной терапии.память, запрос)
создать_свиток("Ответ Nicu", контент)
