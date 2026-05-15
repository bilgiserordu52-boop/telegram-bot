import os
import base64
import requests
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)

ADMINS = set([ADMIN_ID])

deploy_pending = set()
code_history = []

start_time = time.time()
last_ping = time.time()

# ================= STAGING SYSTEM =================
STAGING_BRANCH = "staging"
MAIN_BRANCH = "main"

# ================= SECURITY =================
def is_admin(uid):
    return uid in ADMINS

# ================= SERVER =================
def uptime():
    return round(time.time() - start_time, 2)

def heartbeat():
    global last_ping
    last_ping = time.time()

def is_alive():
    return (time.time() - last_ping) < 60

# ================= DETECTOR =================
def detect_type(text):
    if text.startswith("import") or "def " in text or "print(" in text:
        return "code"
    return "message"

# ================= GITHUB =================
def headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def get_file():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    return requests.get(url, headers=headers()).json()

# ================= STAGING PUSH =================
def push_to_staging(code, msg="staging update"):
    file = get_file()
    sha = file["sha"]

    encoded = base64.b64encode(code.encode()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

    payload = {
        "message": msg,
        "content": encoded,
        "sha": sha,
        "branch": STAGING_BRANCH
    }

    r = requests.put(url, json=payload, headers=headers())
    return r.status_code in [200, 201], r.text

# ================= PROMOTE TO MAIN =================
def promote_to_main(code):
    file = get_file()
    sha = file["sha"]

    encoded = base64.b64encode(code.encode()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

    payload = {
        "message": "promote to main",
        "content": encoded,
        "sha": sha,
        "branch": MAIN_BRANCH
    }

    r = requests.put(url, json=payload, headers=headers())
    return r.status_code in [200, 201], r.text

# ================= SMART UPDATE ENGINE =================
def smart_update(code):
    code_history.append(code)

    if len(code_history) > 10:
        code_history.pop(0)

    return push_to_staging(code, "smart staging update")

# ================= INFO =================
def last_commit():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    r = requests.get(url, headers=headers()).json()

    if isinstance(r, list) and r:
        return r[0]["sha"]
    return "no commit"

# ================= UI =================
def nav():
    return [
        [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
            InlineKeyboardButton("🏠 Home", callback_data="home"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
        ]
    ]

def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Deploy", callback_data="deploy")],
        [InlineKeyboardButton("📦 Version", callback_data="version")],
        [InlineKeyboardButton("🧠 History", callback_data="history")],
        [InlineKeyboardButton("📊 Status", callback_data="status")],
        [InlineKeyboardButton("🔄 Promote to Main", callback_data="promote")]
    ] + nav())

# ================= CORE =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 STAGING SYSTEM ACTIVE")

async def home(update, context):
    uid = update.effective_user.id

    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    heartbeat()

    await update.message.reply_text(
        "🛠 STAGING PANEL",
        reply_markup=panel()
    )

# ================= CALLBACK =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id

    await q.answer()

    if not is_admin(uid):
        return await q.edit_message_text("❌ Yetki yok")

    heartbeat()
    data = q.data

    # NAV
    if data in ["home", "back"]:
        return await home(update, context)

    if data == "cancel":
        deploy_pending.clear()
        return await q.edit_message_text("❌ Cancelled", reply_markup=panel())

    # DEPLOY → STAGING
    if data == "deploy":
        deploy_pending.add(uid)

        return await q.edit_message_text(
            "📦 STAGING MODE\nConfirm staging deploy?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚠️ CONFIRM STAGING", callback_data="deploy_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    if data == "deploy_confirm":
        if uid not in deploy_pending:
            return await q.edit_message_text("❌ Start deploy first")

        deploy_pending.remove(uid)

        ok, res = smart_update("staging deploy")

        return await q.edit_message_text(
            "🚀 SENT TO STAGING" if ok else f"❌ FAIL:\n{res}",
            reply_markup=panel()
        )

    # VERSION
    if data == "version":
        return await q.edit_message_text(f"📦 {last_commit()}", reply_markup=panel())

    # HISTORY
    if data == "history":
        msg = "🧠 CODE HISTORY:\n\n"

        for i, c in enumerate(code_history[-5:]):
            msg += f"{i+1}. {c[:40]}\n"

        return await q.edit_message_text(msg, reply_markup=panel())

    # STATUS
    if data == "status":
        return await q.edit_message_text(
            f"""
🟢 SYSTEM

Uptime: {uptime()} sec
Repo: {GITHUB_REPO}
Staging: ACTIVE
Main: READY
""",
            reply_markup=panel()
        )

    # PROMOTE
    if data == "promote":
        ok, res = promote_to_main("promote from staging")

        return await q.edit_message_text(
            "🚀 PROMOTED TO MAIN" if ok else f"❌ FAIL:\n{res}",
            reply_markup=panel()
        )

# ================= MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    heartbeat()

    text = update.message.text
    uid = update.effective_user.id

    if not is_admin(uid):
        return

    t = detect_type(text)

    # 🧠 SELF UPDATE → STAGING
    if t == "code":
        ok, res = smart_update(text)

        if ok:
            await update.message.reply_text("🧠 Sent to STAGING")
        else:
            await update.message.reply_text(f"❌ FAIL:\n{res}")

        return

    if text.lower() == "selam":
        await update.message.reply_text("Selam 👋")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", home))

    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("STAGING SYSTEM RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
# watcher test 123
