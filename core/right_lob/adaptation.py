from core.right_lob.persistent import (
    update_adaptation_memory,
    add_experience
)

ADAPTATION_MEMORY = {
    "successful_actions": 0,
    "failed_actions": 0,
    "adaptation_score": 0
}


def adapt_from_result(action_result):

    if action_result.get("success"):

        ADAPTATION_MEMORY["successful_actions"] += 1
        ADAPTATION_MEMORY["adaptation_score"] += 2

    else:

        ADAPTATION_MEMORY["failed_actions"] += 1
        ADAPTATION_MEMORY["adaptation_score"] -= 1

    # 🧠 SAVE EXPERIENCE
    add_experience(action_result)

    # 🧠 SAVE PERSISTENT MEMORY
    update_adaptation_memory(
        ADAPTATION_MEMORY
    )

    return {
        "adaptation_memory": ADAPTATION_MEMORY
    }
