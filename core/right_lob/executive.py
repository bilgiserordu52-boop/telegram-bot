EXECUTIVE_STATE = {
    "focus_mode": False,
    "deep_thoughts": 0,
    "ignored_inputs": 0
}


def executive_control(cmd, cognition):

    score = cognition["priority_score"]

    result = {
        "mode": "fast",
        "depth": 1,
        "ignore_noise": False
    }

    # 🧠 HIGH ATTENTION
    if score >= 6:

        EXECUTIVE_STATE["focus_mode"] = True
        EXECUTIVE_STATE["deep_thoughts"] += 1

        result = {
            "mode": "deep",
            "depth": 3,
            "ignore_noise": True
        }

    # 🧠 MEDIUM ATTENTION
    elif score >= 4:

        result = {
            "mode": "balanced",
            "depth": 2,
            "ignore_noise": False
        }

    # 🧠 LOW ATTENTION
    else:

        EXECUTIVE_STATE["ignored_inputs"] += 1

    result["executive_state"] = EXECUTIVE_STATE

    return result
