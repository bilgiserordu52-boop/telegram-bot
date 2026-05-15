import os
import base64
import logging
import requests
import json

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= ENV =================
TOKEN = os.getenv("TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= ADMIN STORAGE =================
def load_admins():
    try:
        with open("admins.json", "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_admins():
    with open("admins.json", "w") as f:
        json.dump(list(admins), f)

admins = load_admins()
deploy_mode = {}

# ================= ADMIN CHECK =================
def is_admin(uid: int):
    return uid in admins or uid == ADMIN_ID

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif\n/help")

# ================= HELP =================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start\n"
        "/login <password>\n"
        "/deploy"
    )

# ================= LOGIN =================
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    parts = update.message.text.split()

    if len(parts) < 2:
        await update.message.reply_text("Kullanım: /login 1234")
        return

    if parts[1] == ADMIN_PASSWORD:
        admins.add(uid)
        save_admins()
        await update.message.reply_text("✅ Admin giriş başarılı")
    else:
        await update.message.reply_text("❌ Hatalı şifre")

# ================= GET SHA =================
def get_sha():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        r = requests.get(url, headers=headers)
        return r.json().get("sha")
    except:
        return None

# ================= DEPLOY COMMAND =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_admin(uid):
        await update.message.reply_text("❌ Yetki yok")
        return

    deploy_mode[uid] = True
    await update.message.reply_text("📦 bot.py kodunu gönder")

# ================= MESSAGE HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    # ===== DEPLOY MODE =====
    if deploy_mode.get(uid):

        deploy_mode[uid] = False

        if not GITHUB_TOKEN or not GITHUB_REPO:
            await update.message.reply_text("❌ GitHub env eksik")
            return

        if len(text.strip()) < 20:
            await update.message.reply_text("❌ Kod çok kısa")
            return

        try:
            sha = get_sha()
            if not sha:
                await update.message.reply_text("❌ SHA alınamadı")
                return

            encoded = base64.b64encode(text.encode()).decode()

            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }

            data = {
                "message": "telegram bot update",
                "content": encoded,
                "sha": sha
            }

            r = requests.put(url, json=data, headers=headers)

            if r.status_code in [200, 201]:
                await update.message.reply_text("🚀 Deploy başarılı")
            else:
                await update.message.reply_text(f"❌ Hata: {r.text}")

        except Exception as e:
            await update.message.reply_text(f"❌ Exception: {str(e)}")

        return

    # ===== NORMAL CHAT =====
    t = text.lower()

    if t == "selam":
        await update.message.reply_text("Selam 👋")

    elif t in ["nasılsın", "naber"]:
        await update.message.reply_text("İyiyim 👍")

    elif t in ["bot", "kimsin"]:
        await update.message.reply_text("Ben senin botunum 🤖")

    if text.strip() == "1+1":
        await update.message.reply_text("2")

# ================= MAIN =================
def main():
    if not TOKEN:
        print("❌ TOKEN YOK")
        return

    print("BOT STARTING")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("deploy", deploy))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("BOT RUNNING")

    app.run_polling()

# ================= RUN =================
if __name__ == "__main__":
    main()
