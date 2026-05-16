def recursive_reflection(response):

    reflection = {
        "needs_retry": False,
        "reason": None,
        "improved_response": None
    }

    # 🧠 LOW QUALITY DETECTION

    if isinstance(response, dict):

        text = str(response).lower()

        # error based retry
        if response.get("status") == "error":
            reflection["needs_retry"] = True
            reflection["reason"] = "error_detected"

        # weak response detection
        elif "unknown" in text:
            reflection["needs_retry"] = True
            reflection["reason"] = "unknown_response"

        # short response detection
        elif len(text) < 40:
            reflection["needs_retry"] = True
            reflection["reason"] = "response_too_short"

    # 🧠 IMPROVED RESPONSE GENERATION

    if reflection["needs_retry"]:

        reflection["improved_response"] = {
            "status": "improved",
            "response": (
                "🧠 Recursive AI improved this response "
                "after self-analysis."
            ),
            "reflection_reason": reflection["reason"]
        }

    return reflection
