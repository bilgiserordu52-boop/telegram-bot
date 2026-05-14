import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================== CONFIG ==================
TOKEN = os.getenv("TOKEN")

# ================== LOGGING ==================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ================== FILE SYSTEM ==================
def load_users():
    try:
        with open("users.json", "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(list(users), f)

def load_admins():
    try:
        with open("admins.json", "r") as f:
            return set(json.load(f))
    except:
        return {8607713044}

def save_admins(admins):
    with open("admins.json", "w") as f:
        json.dump(list(admins), f)

# ================== DATA ==================
users = load_users()
admins = load_admins()

# ================== ADMIN CHECK ==================
def is_admin(uid):
    return uid in admins

# ================== MENUS ==================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("🤖 Info", callback_data="info")]
    ])

def admin_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")],
        [InlineKeyboardButton("👮 Admin Panel", callback_data="admin")],
        [InlineKeyboardButton("➕ Admin Ekle", callback_data="add_admin")],
        [InlineKeyboardButton("➖ Admin Sil", callback_data="remove_admin")],
        [InlineKeyboardButton("🔙 Geri", callback_data="back")]
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Geri", callback_data="back")]
    ])

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    users.add(uid)
    save_users(users)

    if is_admin(uid):
        await update.message.reply_text("👮 Admin Menü", reply_markup=admin_menu())
    else:
        await update.message.reply_text("👤 Kullanıcı Menü", reply_markup=main_menu())

# ================== HELP ==================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Komutlar:\n"
        "/start - Menü\n"
        "/help - Yardım\n\n"
        "📌 Özellikler:\n"
        "- Selam yaz\n"
        "- Stats gör\n"
        "- Admin panel (varsa)"
    )

# ================== MESSAGES ==================
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.lower()

    users.add(uid)
    save_users(users)

    # BROADCAST MODE
    if context.user_data.get("broadcast") and is_admin(uid):
        for user in users:
            try:
                await context.bot.send_message(user, f"📢 Duyuru:\n\n{text}")
            except:
                pass
        context.user_data["broadcast"] = False
        return

    if text == "selam":
        await update.message.reply_text("Selam 👋")

    elif text in ["nasılsın", "naber"]:
        await update.message.reply_text("İyiyim 👍 sen nasılsın?")

    elif text in ["ne yapabilirsin", "ne işe yararsın"]:
        await update.message.reply_text(
            "🤖 Ben bir botum:\n"
            "- Menü sistemi\n"
            "- Admin panel\n"
            "- Stats\n"
            "- Broadcast"
        )

    elif text in ["bot", "kimsin"]:
        await update.message.reply_text("Ben senin Telegram botunum 😎")

# ================== BUTTONS ==================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id

    if query.data == "back":
        if is_admin(uid):
            await query.edit_message_text("👮 Admin Menü", reply_markup=admin_menu())
        else:
            await query.edit_message_text("👤 Kullanıcı Menü", reply_markup=main_menu())

    elif query.data == "stats":
        await query.edit_message_text(
            f"📊 Kullanıcı sayısı: {len(users)}",
            reply_markup=back_menu()
        )

    elif query.data == "info":
        await query.edit_message_text(
            "🤖 Bot aktif çalışıyor",
            reply_markup=back_menu()
        )

    elif query.data == "admin":
        if is_admin(uid):
            await query.edit_message_text("👮 Admin Panel", reply_markup=admin_menu())
        else:
            await query.edit_message_text("❌ Yetki yok", reply_markup=back_menu())

    elif query.data == "broadcast":
        context.user_data["broadcast"] = True
        await query.edit_message_text("📢 Mesaj yaz:", reply_markup=back_menu())

    elif query.data == "add_admin":
        context.user_data["add_admin"] = True
        await query.edit_message_text("➕ Admin ID yaz:", reply_markup=back_menu())

    elif query.data == "remove_admin":
        context.user_data["remove_admin"] = True
        await query.edit_message_text("➖ Admin ID yaz:", reply_markup=back_menu())

# ================== ADMIN TEXT ACTIONS ==================
async def admin_actions
