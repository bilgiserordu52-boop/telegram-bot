import random

from core.ai.local_ai import generate_reply


# =========================
# WORD BANK (BASIC INTELLIGENCE)
# =========================
OPENERS = [
    "Hmm",
    "Şöyle diyebilirim ki",
    "Bence",
    "Bak",
    "Açıkçası"
]

MID = [
    "bu konuda",
    "şu durumda",
    "genel olarak",
    "mantık olarak",
    "sistem açısından"
]

ENDINGS = [
    "böyle görünüyor.",
    "bunu söyleyebilirim.",
    "öyle düşünüyorum.",
    "mantıklı olan bu.",
    "böyle ilerler."
]


# =========================
# SIMPLE CREATIVE MIX
# =========================
def mix(text):

    opener = random.choice(OPENERS)
    mid = random.choice(MID)
    end = random.choice(ENDINGS)

    return f"{opener}, {mid} {text} {end}"


# =========================
# CREATIVE ENGINE
# =========================
def generate_creative_reply(user_id, text):

    base = generate_reply(user_id, text)

    # %50 chance creative rewrite
    if random.random() > 0.5:
        return mix(base)

    return base
