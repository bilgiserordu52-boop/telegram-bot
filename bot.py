import os
import base64
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= ENV =================
TOKEN = os.getenv("TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))

# ================= LOG =================
logging.basicConfig(level=logging.INFO)

# ================= STATE =================
admins = set()
deploy_mode = set()

# ================= SECURITY =================
def is_admin(uid: int):
    return uid == ADMIN_ID or uid in admins

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif\n/login <password>")

# ================= LOGIN =================
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    parts = update.message.text.split()

    if len(parts) < 2:
        await update.message.reply_text("Kullanım: /login 1234")
        return

    if parts[1] == ADMIN_PASSWORD and uid == ADMIN_ID:
        admins.add(uid)
        await update.message.reply_text("✅ Admin giriş başarılı")
    else:
        await update.message.reply_text("❌ Hatalı şifre veya yetkisiz")

# ================= DEPLOY MODE =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if not is_admin(uid):
        await update.message.reply_text("❌ Yetki yok")
        return

    deploy_mode.add(uid)
    await update.message.reply_text("📦 bot.py kodunu gönder")

# ================= GET SHA =================
def get_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.json()["sha"]

# ================= HANDLE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    # ---------------- DEPLOY MODE ----------------
    if uid in deploy_mode:
        deploy_mode.remove(uid)

        if len(text) < 20:
            await update.message.reply_text("❌ Kod çok kısa")
            return

        try:
            encoded = base64.b64encode(text.encode()).decode()
            sha = get_sha()

            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

            data = {
                "message": "telegram deploy update",
                "content": encoded,
                "sha": sha
            }

            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json"
            }

            r = requests.put(url, json=data, headers=headers)

            if r.status_code in [200, 201]:
                await update.message.reply_text("🚀 Deploy başarılı")
            else:
                await update.message.reply_text(f"❌ GitHub error: {r.text}")

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

        return

    # ---------------- NORMAL CHAT ----------------
    t = text.lower()

    if t == "selam":
        await update.message.reply_text("Selam 👋")

    elif t == "naber":
        await update.message.reply_text("İyiyim 👍")

    elif t == "version":
        await update.message.reply_text("📦 Bot çalışıyor")

# ================= MAIN =================
def main():
    if not TOKEN:
        print("TOKEN YOK")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("deploy", deploy))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
