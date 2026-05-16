import random


# =========================
# PERSONALITY MODES
# =========================
PERSONALITIES = {
    "default": {
        "prefix": "",
        "suffix": ""
    },
    "cool": {
        "prefix": "😎 ",
        "suffix": ""
    },
    "serious": {
        "prefix": "⚙️ ",
        "suffix": ""
    },
    "friendly": {
        "prefix": "😊 ",
        "suffix": " dostum"
    },
    "robot": {
        "prefix": "🤖 ",
        "suffix": " [SYSTEM]"
    }
}


USER_PERSONA = {}


def get_persona(user_id):
    if user_id not in USER_PERSONA:
        USER_PERSONA[user_id] = "default"
    return USER_PERSONA[user_id]


def set_persona(user_id, mode):
    if mode in PERSONALITIES:
        USER_PERSONA[user_id] = mode


def apply_persona(user_id, text):

    mode = get_persona(user_id)
    p = PERSONALITIES[mode]

    return f"{p['prefix']}{text}{p['suffix']}"
