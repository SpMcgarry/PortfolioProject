import json
import os

MEMORY_FILE = "memory/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    os.makedirs("memory", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def add_memory(entry):
    memory = load_memory()
    memory.append(entry)
    save_memory(memory)

def search_memory(query):
    memory = load_memory()
    results = [m for m in memory if query.lower() in m["content"].lower()]
    return results
