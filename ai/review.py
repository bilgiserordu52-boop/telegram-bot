def ai_review(code: str):
    score = 0
    reasons = []

    risky_keywords = [
        "os.system",
        "eval(",
        "exec(",
        "subprocess",
        "rm -rf"
    ]

    for r in risky_keywords:
        if r in code:
            score += 50
            reasons.append(r)

    if "while True" in code:
        score += 20

    if len(code.strip()) < 5:
        score += 10

    level = "SAFE"

    if score >= 80:
        level = "DANGEROUS"
    elif score >= 50:
        level = "RISKY"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }
