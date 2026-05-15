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
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)

ADMINS = set([ADMIN_ID])

# ================= STATE =================
deploy_pending = set()
code_history = []

start_time = time.time()
CURRENT_VERSION = str(uuid.uuid4())

STAGING_BRANCH = "staging"

# ================= SECURITY =================
def is_admin(uid):
    return uid in ADMINS

# ================= SYSTEM =================
def uptime():
    return round(time.time() - start_time, 2)

# ================= AI REVIEW =================
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
def headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

def get_file():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py?ref={STAGING_BRANCH}"
        r = requests.get(url, headers=headers(), timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# ================= PUSH =================
def push_to_staging(code: str, msg="deploy"):
    file = get_file()

    # 🔥 CRASH FIX
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

    try:
        r = requests.put(url, json=payload, headers=headers(), timeout=10)

        if r.status_code not in [200, 201]:
            return False, r.text

        return True, "OK"

    except Exception as e:
        return False, str(e)

# ================= SMART UPDATE =================
def smart_update(code):
    review = ai_review(code)

    if review["level"] == "DANGEROUS":
        return False, f"BLOCKED:\n{review}"

    code_history.append(code)

    if len(code_history) > 10:
        code_history.pop(0)

    return push_to_staging(
        code,
        f"AI:{review['level']} score:{review['score']}"
    )

# ================= UI =================
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Deploy", callback_data="deploy")],
        [InlineKeyboardButton("📦 Version", callback_data="version")],
        [InlineKeyboardButton("📜 History", callback_data="history")],
        [InlineKeyboardButton("🧠 AI Review", callback_data="review")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 BOT ONLINE")

# ================= ADMIN =================
async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    deploy_pending.discard(uid)

    if not is_admin(uid):
        return await update.message.reply_text("❌ no access")

    await update.message.reply_text("🛠 PANEL", reply_markup=panel())

# ================= CALLBACK =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    await q.answer()

    if not is_admin(uid):
        return await q.edit_message_text("❌ no access")

    data = q.data

    if data == "deploy":
        deploy_pending.add(uid)
        return await q.edit_message_text("📦 Kod gönder")

    if data == "version":
        return await q.edit_message_text(f"📦 VERSION:\n{CURRENT_VERSION}", reply_markup=panel())

    if data == "history":
        msg = "\n".join(code_history[-5:]) if code_history else "No history"
        return await q.edit_message_text(msg, reply_markup=panel())

    if data == "review":
        if not code_history:
            return await q.edit_message_text("No code")
        r = ai_review(code_history[-1])
        return await q.edit_message_text(str(r), reply_markup=panel())

    if data == "status":
        return await q.edit_message_text(
            f"STATUS OK\nUptime: {uptime()}\nVersion: {CURRENT_VERSION}",
            reply_markup=panel()
        )

# ================= MESSAGE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if not is_admin(uid):
        return

    # deploy mode
    if uid in deploy_pending:
        deploy_pending.remove(uid)

        ok, res = smart_update(text)

        if ok:
            await update.message.reply_text("🚀 Deploy OK")
        else:
            await update.message.reply_text(f"❌ {res}")

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

    print("BOT RUNNING SAFE MODE")

    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
# watcher test 123
