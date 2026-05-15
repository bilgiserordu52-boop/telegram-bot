import os
import base64
import requests
import logging
import time
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)

ADMINS = set([ADMIN_ID])

deploy_pending = set()
code_history = []

# ================= SYSTEM STATE =================
start_time = time.time()
last_ping = time.time()
CURRENT_VERSION = str(uuid.uuid4())

# ================= STAGING =================
STAGING_BRANCH = "staging"

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
    if "def " in text or "import " in text or "print(" in text:
        return "code"
    return "msg"

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
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"
    return requests.get(url, headers=headers()).json()

# ================= STAGING PUSH =================
def push_to_staging(code, msg):
    file = get_file()
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
    return r.status_code in [200, 201], r.text

# ================= SMART UPDATE =================
def smart_update(code):
    code_history.append(code)

    if len(code_history) > 10:
        code_history.pop(0)

    review = ai_review(code)

    if review["level"] == "DANGEROUS":
        return False, f"BLOCKED:\n{review}"

    return push_to_staging(code, f"AI:{review['level']} score:{review['score']}")

# ================= INFO =================
def version():
    return CURRENT_VERSION

# ================= UI =================
def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Deploy", callback_data="deploy")],
        [InlineKeyboardButton("🧠 AI Review", callback_data="review")],
        [InlineKeyboardButton("📦 Version", callback_data="version")],
        [InlineKeyboardButton("📜 History", callback_data="history")],
        [InlineKeyboardButton("🔁 Reload Status", callback_data="reload")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])

# ================= CORE =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 PRO MAX v7 ACTIVE")

async def home(update, context):
    uid = update.effective_user.id
    if not is_admin(uid):
        return await update.message.reply_text("❌ no access")

    heartbeat()

    await update.message.reply_text("🛠 DEVOPS PANEL", reply_markup=panel())

# ================= CALLBACK =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    await q.answer()

    if not is_admin(uid):
        return await q.edit_message_text("❌ no access")

    heartbeat()
    data = q.data

    if data == "version":
        return await q.edit_message_text(f"📦 VERSION:\n{version()}", reply_markup=panel())

    if data == "history":
        msg = "🧠 HISTORY:\n\n"
        for i, c in enumerate(code_history[-5:]):
            msg += f"{i+1}. {c[:40]}\n"
        return await q.edit_message_text(msg, reply_markup=panel())

    if data == "status":
        return await q.edit_message_text(
            f"""
🟢 SYSTEM

Uptime: {uptime()}
Health: {"OK" if is_alive() else "DOWN"}
Version: {CURRENT_VERSION}
            """,
            reply_markup=panel()
        )

    if data == "review":
        if not code_history:
            return await q.edit_message_text("❌ no code")

        r = ai_review(code_history[-1])

        return await q.edit_message_text(
            f"""
🧠 AI REVIEW

Score: {r['score']}
Level: {r['level']}

{chr(10).join(r['reasons']) if r['reasons'] else 'Clean'}
            """,
            reply_markup=panel()
        )

    if data == "reload":
        return await q.edit_message_text(
            f"""
🔁 AUTO RELOAD SYSTEM

Version: {CURRENT_VERSION}
Branch: staging
Mode: CI/CD (GitHub → Railway)
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

    if t == "code":
        ok, res = smart_update(text)

        if ok:
            await update.message.reply_text("🧠 SENT TO STAGING (AI OK)")
        else:
            await update.message.reply_text(f"❌ BLOCKED:\n{res}")

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

    print("PRO MAX v7 RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
# test watcher
# watcher test 123
