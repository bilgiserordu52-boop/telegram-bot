import os
import time
import base64
import logging
import requests
from fastapi import FastAPI, Form
from threading import Thread

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= ENV =================
TOKEN = os.getenv("TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

VERSION = time.strftime("%Y.%m.%d-%H%M")

logging.basicConfig(level=logging.INFO)

# ================= TELEGRAM =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🤖 Bot aktif\n📦 {VERSION}")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == "selam":
        await update.message.reply_text("Selam 👋")

    elif text == "version":
        await update.message.reply_text(VERSION)

# ================= FASTAPI PANEL =================
app = FastAPI()

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
    if not code or len(code) < 10:
        return {"ok": False, "error": "kod boş"}

    try:
        encoded = base64.b64encode(code.encode()).decode()
        sha = get_sha()

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        data = {
            "message": f"panel deploy {VERSION}",
            "content": encoded,
            "sha": sha
        }

        r = requests.put(url, json=data, headers=headers)

        if r.status_code in [200, 201]:
            return {"ok": True, "msg": f"🚀 Deploy başarılı\n📦 {VERSION}"}

        return {"ok": False, "error": r.text}

    except Exception as e:
        return {"ok": False, "error": str(e)}

# ================= RUN BOT =================
def run_bot():
    app_tg = ApplicationBuilder().token(TOKEN).build()

    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")
    app_tg.run_polling()

# ================= RUN API =================
def run_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

# ================= MAIN =================
if __name__ == "__main__":
    Thread(target=run_api).start()
    run_bot()
