from core.ai.local_ai import generate_reply


# =========================
# PERSONA SYSTEM
# =========================
def apply_persona(text, mode):

    if mode == "cool":
        return "😎 " + text

    if mode == "serious":
        return "⚙️ " + text

    return text


# =========================
# HYBRID ENGINE
# =========================
def generate_hybrid_reply(user_id, text, mode="normal"):

    base = generate_reply(user_id, text)

    return apply_persona(base, mode)
