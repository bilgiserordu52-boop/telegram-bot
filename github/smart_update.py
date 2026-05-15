from ai.review import ai_review
from github.push import push_to_github

code_history = []

def smart_update(code, repo, branch, token, file_path, version):
    # history
    code_history.append(code)

    if len(code_history) > 10:
        code_history.pop(0)

    # AI review
    review = ai_review(code)

    # block dangerous
    if review["level"] == "DANGEROUS":
        return False, f"BLOCKED: {review}"

    # push to github
    return push_to_github(
        repo=repo,
        branch=branch,
        token=token,
        file_path=file_path,
        code=code,
        message=f"AI:{review['level']} score:{review['score']}",
        version=version
    )
