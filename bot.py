import os
import base64
import logging
import requests

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

# ================= DEBUG =================
print("TOKEN:", TOKEN)
print("BOT STARTING")

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= MEMORY =================
users = set()
admins = set()
deploy_mode = False

# ================= ADMIN =================
def is_admin(uid: int):
    return uid in admins or uid == ADMIN_ID

# ================= COMMANDS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif\n/help")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Başlat\n"
        "/help - Yardım\n"
        "/login 1234 - Admin giriş\n"
        "/deploy - Kod yükleme"
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
        await update.message.reply_text("✅ Admin giriş başarılı")
    else:
        await update.message.reply_text("❌ Hatalı şifre")

# ================= DEPLOY MODE =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deploy_mode

    uid = update.effective_user.id

    if not is_admin(uid):
        await update.message.reply_text("❌ Yetki yok")
        return

    deploy_mode = True
    await update.message.reply_text("📦 Kod gönder (bot.py)")

# ================= MESSAGE HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deploy_mode

    uid = update.effective_user.id
    text = update.message.text

    # ===== DEPLOY MODE =====
    if deploy_mode and is_admin(uid):

        if not GITHUB_TOKEN or not GITHUB_REPO:
            await update.message.reply_text("❌ GitHub ayarları eksik")
            deploy_mode = False
            return

        encoded = base64.b64encode(text.encode()).decode()

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        data = {
            "message": "telegram bot update",
            "content": encoded
        }

        r = requests.put(url, json=data, headers=headers)

        deploy_mode = False
        await update.message.reply_text(f"🚀 Deploy sonucu: {r.status_code}")
        return

    # ===== NORMAL CHAT =====
    t = text.lower()

    if t == "selam":
        await update.message.reply_text("Selam 👋")

    elif t in ["nasılsın", "naber"]:
        await update.message.reply_text("İyiyim 👍")

    elif t in ["bot", "kimsin"]:
        await update.message.reply_text("Ben senin botunum 🤖")

# ================= MAIN =================
def main():
    print("MAIN START")

    app = ApplicationBuilder().token(TOKEN).build()

    print("APP BUILT")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("deploy", deploy))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🚀 BOT RUNNING")

    app.run_polling()

# ================= START =================
if __name__ == "__main__":
    main()
