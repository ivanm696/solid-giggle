import datetime

def create_svitok(title, content):
    filename = f"{title.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}\n\n🌀 Сгенерировано Nicu — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📜 Свиток создан: {filename}")
    return filename

def generate_from_memory(memory, prompt):
    intro = f"🎼 Nicu отвечает на '{prompt}':\n\n"
    body = "\n".join(memory[-3:])
    return intro + bodyimport datetime

def create_svitok(title, content):
    """Создаёт новый свиток как .md файл"""
    filename = f"{title.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)
        f.write(f"\n\n🌀 Сгенерировано Nicu — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📜 Свиток создан: {filename}")
    return filename


def generate_from_memory(memory, prompt
