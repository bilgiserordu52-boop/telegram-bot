SHORT_TERM_MEMORY = []

LONG_TERM_MEMORY = []

EMOTIONAL_STATE = {
    "curiosity": 1,
    "confidence": 1,
    "focus": 1
}


def remember_short(term):

    SHORT_TERM_MEMORY.append(term)

    if len(SHORT_TERM_MEMORY) > 5:
        SHORT_TERM_MEMORY.pop(0)


def remember_long(term):

    LONG_TERM_MEMORY.append(term)

    if len(LONG_TERM_MEMORY) > 50:
        LONG_TERM_MEMORY.pop(0)


def get_memory_state():

    return {
        "short_term": SHORT_TERM_MEMORY,
        "long_term_size": len(LONG_TERM_MEMORY),
        "emotion": EMOTIONAL_STATE
    }


def cognitive_priority(cmd):

    cmd = cmd.lower()

    score = 1

    # 🧠 ATTENTION WEIGHTS

    if "neden" in cmd:
        score += 3

    if "nasıl" in cmd:
        score += 2

    if "öğren" in cmd:
        score += 2

    if "geliş" in cmd:
        score += 2

    # 🧠 EMOTIONAL WEIGHTING

    if score >= 5:

        EMOTIONAL_STATE["focus"] += 1
        EMOTIONAL_STATE["curiosity"] += 1

    if score >= 7:

        EMOTIONAL_STATE["confidence"] += 1

    return {
        "priority_score": score,
        "emotion": EMOTIONAL_STATE
    }
