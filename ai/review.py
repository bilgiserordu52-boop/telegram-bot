def ai_review(code: str):
    score = 0
    reasons = []

    if "while True" in code:
        score += 40
        reasons.append("Infinite loop risk")

    risky = ["os.system", "eval(", "exec(", "subprocess"]
    for r in risky:
        if r in code:
            score += 50
            reasons.append(f"Danger: {r}")

    if len(code.strip()) < 5:
        score += 20
        reasons.append("Too short")

    level = "SAFE"
    if score >= 50:
        level = "RISKY"
    if score >= 80:
        level = "DANGEROUS"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }
