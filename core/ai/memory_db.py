import json
import os

DB_FILE = "memory.json"


def load_memory():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_memory(user_id, text, reply):

    data = load_memory()
    uid = str(user_id)

    if uid not in data:
        data[uid] = []

    data[uid].append({
        "text": text,
        "reply": reply
    })

    data[uid] = data[uid][-50:]

    save_memory(data)
