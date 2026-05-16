import random

from core.ai.local_ai import generate_reply
from core.ai.memory_db import load_memory, add_memory


def search_memory(user_id, text):

    data = load_memory()
    uid = str(user_id)

    if uid not in data:
        return None

    for item in reversed(data[uid]):
        if text in item["text"]:
            return item["reply"]

    return None


def generate_evolving_reply(user_id, text):

    memory_reply = search_memory(user_id, text)
    if memory_reply:
        return memory_reply + " 🔁"

    reply = generate_reply(user_id, text)

    add_memory(user_id, text, reply)

    if random.random() > 0.7:
        reply += " 🤖"

    return reply
