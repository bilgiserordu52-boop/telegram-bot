import os
import base64
import requests
import logging
import time
import uuid

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
GITHUB_REPO = os.getenv("GITHUB_REPO")  # username/repo
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
STAGING_BRANCH = os.getenv("STAGING_BRANCH", "staging")

logging.basicConfig(level=logging.INFO)

ADMINS = {ADMIN_ID}

deploy_pending = set()
code_history = []

start_time = time.time()
CURRENT_VERSION = str(uuid.uuid4())

# ================= HELPERS =================
def is_admin(uid):
    return uid in ADMINS

def uptime():
    return round(time.time() - start_time, 2)

def headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def ai_review(code: str):
    score = 0
    reasons = []

    if "while True" in code:
        score += 40
        reasons.append("Infinite loop risk")

    bad = ["os.system", "exec(", "eval(", "subprocess"]
    for b in bad:
        if b in code:
            score += 50
            reasons.append(f"Dangerous: {b}")

    if len(code.strip()) < 5:
        score += 20
        reasons.append("Too short")

    level = "SAFE"
    if score >= 50:
        level = "RISKY"
    if score >= 80:
        level = "DANGEROUS"

    return {"score": score, "level": level, "reasons": reasons}

# ================= GITHUB =================
def get_file():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py?ref={STAGING_BRANCH}"
        r = requests.get(url, headers=headers(), timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def push_to_staging(code, msg):
    file = get_file()

    if not isinstance(file, dict) or "sha" not in file:
        return False, f"GITHUB READ ERROR: {file}"

    sha = file["sha"]

    encoded = base64.b64encode(code.encode()).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

    payload = {
        "message": msg + f" | v:{CURRENT_VERSION}",
        "content": encoded,
        "sha": sha,
        "branch": STAGING_BRANCH
    }

    r = requests.put(url, json=payload, headers=headers())

    if r.status_code not in [200, 201]:
        return False, r.json()

    return True, "OK"

# ================= SMART UPDATE =================
def smart_update(code):
    code_history.append(code)

    if len(code_history) > 10:
        code_history.pop(0)

    review = ai_review(code)

    if review["level"] == "DANGEROUS":
        return False, f"BLOCKED: {review}"

    return push_to_staging(code, f"AI:{review['level']} score:{review['score']}")

# ================= UI =================
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Deploy", callback_data="deploy")],
        [InlineKeyboardButton("🧠 AI Review", callback_data="review")],
        [InlineKeyboardButton("📦 Version", callback_data="version")],
        [InlineKeyboardButton("📜 History", callback_data="history")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 BOT ACTIVE")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ no access")

    await update.message.reply_text("🛠 PANEL", reply_markup=panel())

# ================= CALLBACK =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if not is_admin(q.from_user.id):
        return await q.edit_message_text("❌ no access")

    data = q.data

    if data == "version":
        return await q.edit_message_text(f"VERSION:\n{CURRENT_VERSION}", reply_markup=panel())

    if data == "history":
        msg = "\n".join(code_history[-5:]) or "empty"
        return await q.edit_message_text(msg, reply_markup=panel())

    if data == "status":
        return await q.edit_message_text(
            f"UPTIME: {uptime()}\nVERSION: {CURRENT_VERSION}",
            reply_markup=panel()
        )

    if data == "review":
        if not code_history:
            return await q.edit_message_text("no code")

        r = ai_review(code_history[-1])

        return await q.edit_message_text(
            f"""
AI REVIEW
Score: {r['score']}
Level: {r['level']}
Reasons: {', '.join(r['reasons']) or 'clean'}
            """,
            reply_markup=panel()
        )

# ================= MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    if not is_admin(uid):
        return

    if text.lower() == "selam":
        return await update.message.reply_text("Selam 👋")

    if "print(" in text or "def " in text:
        ok, res = smart_update(text)

        if ok:
            await update.message.reply_text("🚀 Deploy OK")
        else:
            await update.message.reply_text(f"❌ ERROR:\n{res}")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
# watcher test 123
