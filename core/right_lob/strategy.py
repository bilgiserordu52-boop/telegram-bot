from core.right_lob.persistent import load_persistent_memory


STRATEGY_STATE = {
    "preferred_mode": "balanced",
    "risk_level": 1,
    "learning_bias": 1
}


def analyze_experience():

    memory = load_persistent_memory()

    adaptation = memory.get("adaptation", {})

    success = adaptation.get(
        "successful_actions",
        0
    )

    failed = adaptation.get(
        "failed_actions",
        0
    )

    score = adaptation.get(
        "adaptation_score",
        0
    )

    # 🧠 STRATEGIC ADAPTATION

    if score >= 5:

        STRATEGY_STATE["preferred_mode"] = (
            "aggressive_learning"
        )

        STRATEGY_STATE["learning_bias"] += 1

    if failed >= 3:

        STRATEGY_STATE["preferred_mode"] = (
            "safe_mode"
        )

        STRATEGY_STATE["risk_level"] = 0

    return STRATEGY_STATE


def strategic_decision(cmd):

    state = analyze_experience()

    cmd = cmd.lower()

    # 🧠 STRATEGIC BEHAVIOR

    if state["preferred_mode"] == (
        "aggressive_learning"
    ):

        if "öğren" in cmd:
            return {
                "strategy": "maximize_learning",
                "priority": "high"
            }

    if state["preferred_mode"] == (
        "safe_mode"
    ):

        return {
            "strategy": "safe_execution",
            "priority": "low"
        }

    return {
        "strategy": "balanced_execution",
        "priority": "normal"
    }
