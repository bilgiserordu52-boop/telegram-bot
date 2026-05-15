import os
import base64
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
GITHUB_REPO = os.getenv("GITHUB_REPO")  # user/repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)

admins = set()
deploy_mode = set()

# ================= SECURITY =================
def is_admin(uid: int):
    return uid == ADMIN_ID or uid in admins

# ================= GITHUB HELPERS =================
def github_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def get_file():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    r = requests.get(url, headers=github_headers())
    return r.json()

def push_file(code: str, message="deploy"):
    data_old = get_file()
    sha = data_old["sha"]

    encoded = base64.b64encode(code.encode()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

    payload = {
        "message": message,
        "content": encoded,
        "sha": sha
    }

    r = requests.put(url, json=payload, headers=github_headers())
    return r.status_code in [200, 201], r.text

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif")

# ================= LOGIN =================
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    parts = update.message.text.split()

    if len(parts) < 2:
        await update.message.reply_text("Kullanım: /login 1234")
        return

    if parts[1] == "1234" and uid == ADMIN_ID:
        admins.add(uid)
        await update.message.reply_text("✅ Admin giriş başarılı")
    else:
        await update.message.reply_text("❌ Hatalı giriş")

# ================= DEPLOY =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    deploy_mode.add(uid)
    await update.message.reply_text("📦 Kod gönder (tek mesaj veya kısa kod)")

# ================= VERSION =================
def get_last_commit():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    r = requests.get(url, headers=github_headers())
    data = r.json()

    if isinstance(data, list) and len(data) > 0:
        return data[0]["sha"]
    return None

async def version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sha = get_last_commit()
    if sha:
        await update.message.reply_text(f"📦 Last commit:\n{sha}")
    else:
        await update.message.reply_text("❌ commit yok")

# ================= ROLLBACK =================
async def rollback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    r = requests.get(url, headers=github_headers())
    commits = r.json()

    if not isinstance(commits, list) or len(commits) < 2:
        return await update.message.reply_text("❌ rollback yok")

    file_data = get_file()

    # decode current content (safe rollback)
    content = base64.b64decode(file_data["content"]).decode()

    payload = {
        "message": "rollback",
        "content": base64.b64encode(content.encode()).decode(),
        "sha": file_data["sha"]
    }

    url_file = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    r2 = requests.put(url_file, json=payload, headers=github_headers())

    if r2.status_code in [200, 201]:
        await update.message.reply_text("↩️ Rollback OK")
    else:
        await update.message.reply_text("❌ rollback failed")

# ================= MESSAGE HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if uid in deploy_mode:
        deploy_mode.remove(uid)

        ok, res = push_file(text, "telegram deploy")

        if ok:
            await update.message.reply_text("🚀 Deploy OK")
        else:
            await update.message.reply_text(f"❌ GitHub error: {res}")
        return

    if text.lower() == "selam":
        await update.message.reply_text("Selam 👋")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("deploy", deploy))
    app.add_handler(CommandHandler("version", version))
    app.add_handler(CommandHandler("rollback", rollback))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
