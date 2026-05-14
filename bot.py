import os
TOKEN = os.getenv("TOKEN")
print("TOKEN", TOKEN)
import json
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

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))

# ================= LOG =================
logging.basicConfig(level=logging.INFO)

# ================= MEMORY =================
users = set()
admins = set()

deploy_mode = False

# ================= ADMIN CHECK =================
def is_admin(uid):
    return uid in admins or uid == ADMIN_ID

# ================= COMMANDS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif\n/help")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - başlat\n"
        "/help - yardım\n"
        "/login 1234 - admin giriş\n"
        "/deploy - kod gönder"
    )

# ================= LOGIN (FIXED) =================
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    parts = update.message.text.split()

    if len(parts) < 2:
        await update.message.reply_text("Kullanım: /login 1234")
        return

    password = parts[1]

    if password == ADMIN_PASSWORD:
        admins.add(uid)
        await update.message.reply_text("✅ Admin giriş başarılı")
    else:
        await update.message.reply_text("❌ Hatalı şifre")

# ================= DEPLOY =================
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deploy_mode
    uid = update.effective_user.id

    if not is_admin(uid):
        await update.message.reply_text("❌ Yetki yok")
        return

    deploy_mode = True
    await update.message.reply_text("📦 Kod gönder (bot.py)")

# ================= MESSAGE HANDLER =================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global deploy_mode

    uid = update.effective_user.id
    text = update.message.text

    # ========== DEPLOY MODE ==========
    if deploy_mode and is_admin(uid):

        if not GITHUB_TOKEN or not GITHUB_REPO:
            await update.message.reply_text("❌ GitHub ayarları eksik")
            deploy_mode = False
            return

        encoded = base64.b64encode(text.encode()).decode()

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/bot.py"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        data = {
            "message": "telegram deploy update",
            "content": encoded
        }

        r = requests.put(url, json=data, headers=headers)

        deploy_mode = False
