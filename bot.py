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

def push_code(code, msg="deploy"):
    file = get_file()
    sha = file["sha"]

    encoded = base64.b64encode(code.encode()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

    payload = {
        "message": msg,
        "content": encoded,
        "sha": sha
    }

    r = requests.put(url, json=payload, headers=headers())
    return r.status_code in [200, 201], r.text

def smart_update(code):
    code_history.append(code)

    if len(code_history) > 10:
        code_history.pop(0)

    return push_code(code, "smart update")

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
        [InlineKeyboardButton("🖥 Server", callback_data="server")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ] + nav())

# ================= CORE =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 PRO SELF UPDATE BOT ACTIVE")

async def home(update, context):
    uid = update.effective_user.id
    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    heartbeat()

    await update.message.reply_text(
        "🛠 DEVOPS PANEL",
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

    # DEPLOY
    if data == "deploy":
        deploy_pending.add(uid)
        return await q.edit_message_text(
            "📦 Deploy Mode\nConfirm or Cancel",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚠️ CONFIRM", callback_data="deploy_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )

    if data == "deploy_confirm":
        if uid not in deploy_pending:
            return await q.edit_message_text("❌ Start deploy first")

        deploy_pending.remove(uid)

        ok, res = push_code("manual deploy", "deploy")

        return await q.edit_message_text(
            "🚀 DEPLOY OK" if ok else f"❌ FAIL:\n{res}",
            reply_markup=panel()
        )

    # VERSION
    if data == "version":
        return await q.edit_message_text(f"📦 {last_commit()}", reply_markup=panel())

    # HISTORY
    if data == "history":
        msg = "🧠 LAST CODES:\n\n"
        for i, c in enumerate(code_history[-5:]):
            msg += f"{i+1}. {c[:40]}\n"

        return await q.edit_message_text(msg, reply_markup=panel())

    # SERVER
    if data == "server":
        status = "🟢 ONLINE" if is_alive() else "🔴 OFFLINE"

        return await q.edit_message_text(
            f"""
🖥 SERVER

Status: {status}
Uptime: {uptime()} sec
            """,
            reply_markup=panel()
        )

    # STATUS
    if data == "status":
        return await q.edit_message_text(
            f"""
🟢 SYSTEM

Repo: {GITHUB_REPO}
Admins: {len(ADMINS)}
Uptime: {uptime()} sec
            """,
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

    # 🧠 SELF UPDATE ENGINE
    if t == "code":
        ok, res = smart_update(text)

        if ok:
            await update.message.reply_text("🧠 Smart Update OK (GitHub)")
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

    print("PRO SELF UPDATE RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
# watcher test 123
