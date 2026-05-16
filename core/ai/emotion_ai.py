import random
import time


# =========================
# USER MOOD MEMORY
# =========================
MOOD = {}  # user_id -> mood


MOODS = ["calm", "happy", "busy", "lazy"]


def get_mood(user_id):

    if user_id not in MOOD:
        MOOD[user_id] = random.choice(MOODS)

    return MOOD[user_id]


def update_mood(user_id):

    # random mood shift
    if random.random() > 0.7:
        MOOD[user_id] = random.choice(MOODS)

    return MOOD[user_id]


# =========================
# EMOTION WRAPPER
# =========================
def apply_emotion(user_id, text):

    mood = update_mood(user_id)

    if mood == "happy":
        return "😊 " + text

    if mood == "busy":
        return "⚙️ " + text + " (meşgul mod)"

    if mood == "lazy":
        return "😴 " + text

    return "🧠 " + text
