from collections import deque

# 🧠 simple conversation memory
CONTEXT_WINDOW = deque(maxlen=10)


def add_context(role, text):
    CONTEXT_WINDOW.append({
        "role": role,
        "text": text
    })


def get_context():
    return list(CONTEXT_WINDOW)


def clear_context():
    CONTEXT_WINDOW.clear()
