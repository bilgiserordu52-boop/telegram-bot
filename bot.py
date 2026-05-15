import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)

admins = set()
deploy_mode = set()
history = []  # rollback için

# ================= HELPERS =================
def is_admin(uid):
    return uid == ADMIN_ID or uid in admins

def github_push(code: str, msg="auto deploy"):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers)
    sha = r.json()["sha"]

    import base64
    encoded = base64.b64encode(code.encode()).decode()

    data = {
        "message": msg,
        "content": encoded,
        "sha": sha
    }

    res = requests.put(url, json=data, headers=headers)
    return res.status_code in [200, 201], res.text

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
        await update.message.reply_text("✅ Admin giriş")
    else:
        await update.message.reply_text("❌ Hatalı")

# ================= DEPLOY =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    deploy_mode.add(uid)
    await update.message.reply_text("📦 Kod gönder")

# ================= VERSION =================
async def version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if history:
        await update.message.reply_text(f"📦 Last commit:\n{history[-1]}")
    else:
        await update.message.reply_text("📦 No history")

# ================= ROLLBACK =================
async def rollback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    if len(history) < 2:
        return await update.message.reply_text("❌ rollback yok")

    last = history[-2]

    ok, err = github_push(last, "rollback")
    if ok:
        await update.message.reply_text("↩️ Rollback başarılı")
    else:
        await update.message.reply_text(f"❌ hata: {err}")

# ================= MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if uid in deploy_mode:
        deploy_mode.remove(uid)

        code = text # artık direkt gelen mesaj kod

        history.append(code)
        if len(history) > 5:
            history.pop(0)

        ok, err = github_push(code, "deploy")

        if ok:
            await update.message.reply_text("🚀 Deploy OK")
        else:
            await update.message.reply_text(f"❌ GitHub error: {err}")

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
