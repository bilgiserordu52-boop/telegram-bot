from core.ai.bond import get_bond, add_bond
from core.ai.personality import set_persona


# =========================
# BOND LEVEL SYSTEM
# =========================
def calculate_level(bond):

    if bond < 5:
        return "stranger"

    if bond < 15:
        return "known"

    if bond < 30:
        return "friend"

    return "close"


# =========================
# UPDATE PERSONALITY BY BOND
# =========================
def update_persona_by_bond(user_id):

    bond = get_bond(user_id)
    level = calculate_level(bond)

    if level == "stranger":
        set_persona(user_id, "robot")

    elif level == "known":
        set_persona(user_id, "default")

    elif level == "friend":
        set_persona(user_id, "friendly")

    else:
        set_persona(user_id, "cool")

    return level


# =========================
# MAIN HOOK
# =========================
def process_bond(user_id):

    new_bond = add_bond(user_id, 1)
    level = update_persona_by_bond(user_id)

    return new_bond, level
