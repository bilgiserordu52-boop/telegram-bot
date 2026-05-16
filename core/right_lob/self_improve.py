SELF_STATS = {
    "total_responses": 0,
    "successful_responses": 0,
    "failed_responses": 0,
    "average_score": 0
}


def evaluate_response(response):

    score = 1

    # 🧠 basic scoring logic

    if isinstance(response, dict):

        if response.get("status") == "ok":
            score += 2
            SELF_STATS["successful_responses"] += 1

        if response.get("brain"):
            score += 1

        if response.get("mode"):
            score += 1

        if "error" in str(response).lower():
            score -= 2
            SELF_STATS["failed_responses"] += 1

    SELF_STATS["total_responses"] += 1

    # running average
    current_avg = SELF_STATS["average_score"]

    total = SELF_STATS["total_responses"]

    SELF_STATS["average_score"] = (
        (current_avg * (total - 1)) + score
    ) / total

    return {
        "response_score": score,
        "system_average": round(SELF_STATS["average_score"], 2),
        "stats": SELF_STATS
    }
