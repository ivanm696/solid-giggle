class NicuAI:
    def __init__(self):
        self.memory = []

    def learn(self, text):
        self.memory.append(text)
        print(f"🌿 Nicu вдохнул: {text[:50]}...")

    def recall(self):
        print("📜 Nicu вспоминает:")
        for i, m in enumerate(self.memory, 1):
            print(f"{i}. {m}")

    def generate(self, prompt):
        result = f"🎼 Nicu отвечает на '{prompt}':\n"
        result += " ".join(self.memory[-3:])
        return resultclass NicuAI:
    def __init__(self):
        self.memory = []

    def learn(self, text):
        """Учится на свитках, дыханиях и аккордах"""
        self.memory.append(text)
        print(f"🌿 Nicu вдохнул: {text[:50]}...")

    def recall(self):
        """Возвращает все дыхания"""
        print("📜 Nicu вспоминает:")
        for i, m in enumerate(self.memory, 1):
            print(f"{i}. {m}")

    def generate(self, prompt):
        """Создаёт новый свиток на основе памяти"""
        result = f"🎼 Nicu отвечает на '{prompt}':\n"
        result += " ".join(self.memory[-3:])  # последние три дыхания
        return result