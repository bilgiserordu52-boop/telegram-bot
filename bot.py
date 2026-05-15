import os
import base64
import requests
import logging
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
user_state = {}

# ================= SECURITY =================
def is_admin(uid):
    return uid in ADMINS

# ================= GITHUB =================
def headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def get_file():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    r = requests.get(url, headers=headers())
    return r.json()

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

def last_commit():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    r = requests.get(url, headers=headers()).json()

    if isinstance(r, list) and r:
        return r[0]["sha"]
    return "no commit"

def ci_status():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
    r = requests.get(url, headers=headers()).json()

    runs = r.get("workflow_runs", [])
    if not runs:
        return "NO CI", "UNKNOWN"

    last = runs[0]
    return last["status"], last["conclusion"]

def last_logs():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
    r = requests.get(url, headers=headers()).json()

    runs = r.get("workflow_runs", [])[:3]

    msg = "📜 LAST RUNS:\n\n"
    for run in runs:
        msg += f"{run['name']} | {run['status']} | {run['conclusion']}\n"

    return msg

def rollback_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/commits"
    r = requests.get(url, headers=headers()).json()

    if isinstance(r, list) and len(r) > 1:
        return r[1]["sha"]
    return None

# ================= NAVIGATION =================
def nav():
    return [
        [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
            InlineKeyboardButton("🏠 Home", callback_data="home"),
            InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
        ]
    ]

def panel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Deploy", callback_data="deploy")],
        [InlineKeyboardButton("📦 Version", callback_data="version")],
        [InlineKeyboardButton("🧪 CI Status", callback_data="ci")],
        [InlineKeyboardButton("📜 Logs", callback_data="logs")],
        [InlineKeyboardButton("↩️ Rollback", callback_data="rollback")],
        [InlineKeyboardButton("📊 Status", callback_data="status")],
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh")]
    ] + nav())

# ================= CORE =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif")

async def home(update, context):
    uid = update.effective_user.id

    if not is_admin(uid):
        return await update.message.reply_text("❌ Yetki yok")

    user_state[uid] = "home"

    await update.message.reply_text(
        "🛠 MAIN DASHBOARD",
        reply_markup=panel_keyboard()
    )

# ================= CALLBACK ENGINE =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id

    await q.answer()

    if not is_admin(uid):
        return await q.edit_message_text("❌ Yetki yok")

    data = q.data

    # 🔙 BACK
    if data == "back":
        return await home(update, context)

    # 🏠 HOME
    if data == "home":
        return await home(update, context)

    # ❌ CANCEL
    if data == "cancel":
        deploy_pending.discard(uid)
        user_state[uid] = "home"
        return await q.edit_message_text(
            "❌ İptal edildi",
            reply_markup=panel_keyboard()
        )

    # 🚀 DEPLOY MODE
    if data == "deploy":
        deploy_pending.add(uid)
        user_state[uid] = "deploy"

        return await q.edit_message_text(
            "📦 Deploy mode\nOnaylamak için confirm bas",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚠️ Confirm Deploy", callback_data="deploy_confirm")],
                *nav()
            ])
        )

    # ⚠️ CONFIRM DEPLOY
    if data == "deploy_confirm":
        if uid not in deploy_pending:
            return await q.edit_message_text("❌ Önce deploy başlat")

        deploy_pending.discard(uid)

        ok, res = push_code("deploy from panel", "deploy")

        return await q.edit_message_text(
            "🚀 Deploy OK" if ok else f"❌ FAIL:\n{res}",
            reply_markup=panel_keyboard()
        )

    # 📦 VERSION
    if data == "version":
        return await q.edit_message_text(
            f"📦 Last commit:\n{last_commit()}",
            reply_markup=panel_keyboard()
        )

    # 🧪 CI
    if data == "ci":
        s, c = ci_status()
        return await q.edit_message_text(
            f"🧪 CI STATUS\n{s} / {c}",
            reply_markup=panel_keyboard()
        )

    # 📜 LOGS
    if data == "logs":
        return await q.edit_message_text(
            last_logs(),
            reply_markup=panel_keyboard()
        )

    # 📊 STATUS
    if data == "status":
        return await q.edit_message_text(
            f"🟢 SYSTEM\nRepo: {GITHUB_REPO}\nAdmins: {len(ADMINS)}",
            reply_markup=panel_keyboard()
        )

    # ↩️ ROLLBACK
    if data == "rollback":
        sha = rollback_sha()

        if not sha:
            return await q.edit_message_text("❌ No rollback point")

        ok, res = push_code(f"rollback {sha}", "rollback")

        return await q.edit_message_text(
            "↩️ Rollback OK" if ok else f"❌ FAIL:\n{res}",
            reply_markup=panel_keyboard()
        )

    # 🔄 REFRESH
    if data == "refresh":
        return await home(update, context)

# ================= MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.lower() == "selam":
        await update.message.reply_text("Selam 👋")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", home))

    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("PRO MAX UI BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
# watcher test 123
