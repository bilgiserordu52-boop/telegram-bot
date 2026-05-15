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

# ================= VERSION =================
VERSION = "v1.2"

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= STATE =================
admins = set()
deploy_mode = {}

# ================= ADMIN =================
def is_admin(uid: int):
    return uid in admins or uid == ADMIN_ID

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🤖 Bot aktif\n🚀 Versiyon: {VERSION}"
    )

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
        await update.message.reply_text("✅ Admin giriş başarılı")
    else:
        await update.message.reply_text("❌ Hatalı şifre")

# ================= SHA =================
def get_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.json()["sha"]

# ================= DEPLOY =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_admin(uid):
        await update.message.reply_text("❌ Yetki yok")
        return

    deploy_mode[uid] = True
    await update.message.reply_text("📦 Kod gönder (bot.py)")

# ================= MESSAGE =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    # ===== DEPLOY MODE =====
    if deploy_mode.get(uid):

        if not GITHUB_TOKEN or not GITHUB_REPO:
            await update.message.reply_text("❌ GitHub eksik")
            deploy_mode[uid] = False
            return

        try:
            encoded = base64.b64encode(text.encode()).decode()
            sha = get_sha()

            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }

            data = {
                "message": f"telegram update {VERSION}",
                "content": encoded,
                "sha": sha
            }

            r = requests.put(url, json=data, headers=headers)

            deploy_mode[uid] = False

            if r.status_code in [200, 201]:
                await update.message.reply_text("🚀 Deploy başarılı")
            else:
                await update.message.reply_text(f"❌ Deploy hata: {r.text}")

        except Exception as e:
            deploy_mode[uid] = False
            await update.message.reply_text(f"❌ Error: {str(e)}")

        return

    # ===== TEST =====
    if text.strip() == "1+1":
        await update.message.reply_text("2")
        return

    # ===== NORMAL CHAT =====
    t = text.lower()

    if t == "selam":
        await update.message.reply_text("Selam 👋")

    elif t in ["nasılsın", "naber"]:
        await update.message.reply_text("İyiyim 👍")

    elif t in ["bot", "kimsin"]:
        await update.message.reply_text("Ben senin botunum 🤖")

# ================= RESTART MSG (SYNC FIX) =================
def notify_restart():
    try:
        if TOKEN and ADMIN_ID:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            requests.post(url, data={
                "chat_id": ADMIN_ID,
                "text": f"🚀 Bot yeniden başladı!\n📦 Versiyon: {VERSION}"
            })
    except:
        pass

# ================= MAIN =================
def main():
    if not TOKEN:
        print("❌ TOKEN YOK")
        return

    print("BOT STARTING")

    notify_restart()

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
