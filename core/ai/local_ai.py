import random


# =========================
# MEMORY SYSTEM
# =========================
MEMORY = {}


def remember(user_id, text):
    user_id = str(user_id)

    MEMORY.setdefault(user_id, []).append(text)
    MEMORY[user_id] = MEMORY[user_id][-5:]


def last(user_id):
    user_id = str(user_id)
    return MEMORY.get(user_id, [""])[-1]


# =========================
# BASIC RESPONSES
# =========================
RESPONSES = {
    "selam": [
        "👋 Selam!",
        "👋 Hey buradayım",
        "👋 Nasılsın?"
    ],
    "nasılsın": [
        "İyiyim 👍 sen?",
        "Fena değil ⚙️",
        "Gayet stabil 😎"
    ],
    "ne yapıyorsun": [
        "Seni dinliyorum 👀",
        "Sistem çalışıyor ⚙️",
        "Veri işliyorum 📡"
    ]
}


# =========================
# SMART REPLY ENGINE
# =========================
def generate_reply(user_id, text):

    text = text.lower().strip()
    user_id = str(user_id)

    remember(user_id, text)

    prev = last(user_id)

    # exact match
    if text in RESPONSES:
        return random.choice(RESPONSES[text])

    # partial match
    if "selam" in text:
        if "selam" in prev:
            return "👋 Yine selam 😄"
        return "👋 Selam, buradayım"

    if "nasıl" in text:
        return random.choice(RESPONSES["nasılsın"])

    if "ne yap" in text:
        return random.choice(RESPONSES["ne yapıyorsun"])

    # fallback AI style
    return random.choice([
        "Bunu tam anlayamadım 👀",
        "Biraz daha açık yazar mısın?",
        "İlginç... devam et"
    ])
