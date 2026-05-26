import json
import os

MEMORY_FILE = "memory/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)


def add_to_memory(user_input, response):
    memory = load_memory()

    memory.append({
        "user": user_input,
        "assistant": response
    })

    save_memory(memory)


def get_last_context(limit=5):
    memory = load_memory()

    last = memory[-limit:]

    context = ""

    for msg in last:
        context += f"""
Пользователь: {msg['user']}
Ассистент: {msg['assistant']}
"""

    return context