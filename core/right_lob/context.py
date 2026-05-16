from collections import deque

# 🧠 conversation memory (PHASE 10 CORE)
_CONTEXT = deque(maxlen=10)


def add_context(role, text):
    _CONTEXT.append({
        "role": role,
        "text": text
    })


def get_context():
    return list(_CONTEXT)


def clear_context():
    _CONTEXT.clear()
