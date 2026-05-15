import os
import base64
import requests
from fastapi import FastAPI, Form

app = FastAPI()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
FILE_PATH = "bot.py"

def get_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.json()["sha"]

@app.get("/")
def home():
    return {"status": "ok", "msg": "panel aktif"}

@app.post("/deploy")
def deploy(code: str = Form(...)):
    encoded = base64.b64encode(code.encode()).decode()
    sha = get_sha()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "message": "web panel deploy",
        "content": encoded,
        "sha": sha
    }

    r = requests.put(url, json=data, headers=headers)

    if r.status_code in [200, 201]:
        return {"ok": True, "msg": "🚀 Deploy başarılı"}
    return {"ok": False, "error": r.text}
