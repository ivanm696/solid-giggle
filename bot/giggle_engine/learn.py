class NicuAI:
    """Система памяти и обучения Nicu"""

    def __init__(self):
        self.memory: list[str] = []

    def learn(self, text: str) -> None:
        """Учится на свитках, дыханиях и аккордах"""
        self.memory.append(text)
        print(f"🌿 Nicu вдохнул: {text[:50]}...")

    def recall(self) -> None:
        """Выводит все дыхания из памяти"""
        print("📜 Nicu вспоминает:")
        for i, m in enumerate(self.memory, 1):
            print(f"{i}. {m}")

    def generate(self, prompt: str) -> str:
        """Создаёт новый свиток на основе памяти"""
        result = f"🎼 Nicu отвечает на '{prompt}':\n"
        result += " ".join(self.memory[-3:])  # последние три дыхания
        return result
