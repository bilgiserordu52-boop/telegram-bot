import requests

def headers(github_token):
    return {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

def get_file(repo, branch, token):
    url = f"https://api.github.com/repos/{repo}/contents/bot.py?ref={branch}"

    try:
        r = requests.get(url, headers=headers(token), timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}
