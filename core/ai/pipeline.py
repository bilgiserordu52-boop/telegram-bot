from core.ai.engine_ai import generate
from core.ai.memory_db import add_memory, get_memory


def run_ai(user_id, text):

    history = get_memory(user_id)

    # basit context injection
    context_text = text

    if history:
        last = history[-1]
        context_text = f"{last['text']} | {text}"

    reply = generate(context_text)

    add_memory(user_id, text, reply)

    return reply
