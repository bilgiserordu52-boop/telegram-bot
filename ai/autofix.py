import re
from ai.review import ai_review


def auto_fix(code: str):

    review = ai_review(code)

    fixed = code

    # 1. eval remove
    fixed = re.sub(r"eval\((.*?)\)", "# removed eval()", fixed)

    # 2. exec remove
    fixed = re.sub(r"exec\((.*?)\)", "# removed exec()", fixed)

    # 3. while True patch
    fixed = fixed.replace("while True", "while False  # auto-fixed")

    return {
        "original_score": review["score"],
        "level": review["level"],
        "fixed_code": fixed,
        "safe": review["score"] < 50
    }
