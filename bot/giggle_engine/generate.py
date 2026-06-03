import datetime

def create_svitok(title: str, content: str) -> str:
    """Создаёт новый свиток как .md файл"""
    filename = f"{title.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)
        f.write(f"\n\n🌀 Сгенерировано Nicu — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📜 Свиток создан: {filename}")
    return filename


def generate_from_memory(memory: list, prompt: str) -> str:
    """Генерирует ответ на основе памяти Nicu"""
    intro = f"🎼 Nicu отвечает на '{prompt}':\n\n"
    body = "\n".join(memory[-3:]) if memory else "Память пуста."
    return intro + body
