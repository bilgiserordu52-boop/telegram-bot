import random


# =========================
# USER STATES
# =========================
USER_STATE = {}


# =========================
# GET STATE
# =========================
def get_state(user_id):

    if str(user_id) not in USER_STATE:

        USER_STATE[str(user_id)] = {
            "mood": "neutral",
            "energy": 50,
            "bond": 0,
            "last_intent": None
        }

    return USER_STATE[str(user_id)]


# =========================
# DETECT INTENT
# =========================
def detect_intent(text):

    text = text.lower()


    # greeting
    if any(x in text for x in [
        "selam",
        "merhaba",
        "sa",
        "naber"
    ]):
        return "greeting"


    # emotional
    if any(x in text for x in [
        "üzgün",
        "kötü",
        "moralim",
        "yalnız"
    ]):
        return "emotion"


    # funny
    if any(x in text for x in [
        "jsjs",
        "dhdh",
        "🤣",
        "😂"
    ]):
        return "fun"


    # question
    if "?" in text:
        return "question"


    return "normal"


# =========================
# UPDATE STATE
# =========================
def update_state(user_id, intent):

    state = get_state(user_id)

    state["last_intent"] = intent


    # emotion
    if intent == "emotion":

        state["mood"] = "supportive"

        state["bond"] += 2


    # fun
    elif intent == "fun":

        state["mood"] = "playful"

        state["energy"] += 5


    # greeting
    elif intent == "greeting":

        state["mood"] = "friendly"

        state["bond"] += 1


    else:

        state["mood"] = "neutral"


    # limits
    if state["bond"] > 100:
        state["bond"] = 100

    if state["energy"] > 100:
        state["energy"] = 100


# =========================
# RESPONSE MODE
# =========================
def generate_style(user_id):

    state = get_state(user_id)

    mood = state["mood"]


    if mood == "friendly":

        return random.choice([
            "😄",
            "👋",
            "🔥"
        ])


    if mood == "playful":

        return random.choice([
            "🤣",
            "😎",
            "dhdhdh"
        ])


    if mood == "supportive":

        return random.choice([
            "🫂",
            "💙",
            "Yanındayım
