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

users = load_users()
admins = load_admins()

# ================== ADMIN ==================
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
        "🤖 BOT YARDIM\n\n"
        "/start - Menü\n"
        "/help - Yardım\n\n"
        "📌 Özellikler:\n"
        "- selam yaz\n"
        "- nasılsın yaz\n"
        "- admin panel (varsa)\n"
        "- stats"
    )

# ================== CALLBACK ==================
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

    elif query.data == "broadcast":
        context.user_data["broadcast"] = True
        await query.edit_message_text("📢 Mesaj yaz:", reply_markup=back_menu())

    elif query.data == "add_admin":
        context.user_data["add_admin"] = True
        await query.edit_message_text("➕ Admin ID yaz:", reply_markup=back_menu())

    elif query.data == "remove_admin":
        context.user_data["remove_admin"] = True
        await query.edit_message_text("➖ Admin ID yaz:", reply_markup=back_menu())

# ================== MESSAGES (TEK HANDLER) ==================
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.lower()

    users.add(uid)
    save_users(users)

    # ===== ADMIN ACTIONS =====
    if context.user_data.get("add_admin") and is_admin(uid):
        try:
            new_admin = int(text)
            admins.add(new_admin)
            save_admins(admins)
            await update.message.reply_text("✅ Admin eklendi")
        except:
            await update.message.reply_text("❌ Hatalı ID")
        context.user_data["add_admin"] = False
        return

    if context.user_data.get("remove_admin") and is_admin(uid):
        try:
            rem_admin = int(text)
            admins.discard(rem_admin)
            save_admins(admins)
            await update.message.reply_text("🗑 Admin silindi")
        except:
            await update.message.reply_text("❌ Hatalı ID")
        context.user_data["remove_admin"] = False
        return

    # ===== BROADCAST =====
    if context.user_data.get("broadcast") and is_admin(uid):
        for user in users:
            try:
                await context.bot.send_message(user, f"📢 Duyuru:\n\n{text}")
            except:
                pass
        context.user_data["broadcast"] = False
        return

    # ===== NORMAL RESPONSES =====
    if text == "selam":
        await update.message.reply_text("Selam 👋")

    elif text in ["nasılsın", "naber"]:
        await update.message.reply_text("İyiyim 👍 sen nasılsın?")

    elif text in ["ne yapabilirsin", "ne işe yararsın"]:
        await update.message.reply_text(
            "🤖 Ben bir botum:\n"
            "- Menü\n"
            "- Admin panel\n"
            "- Stats\n"
            "- Broadcast"
        )

    elif text in ["bot", "kimsin"]:
        await update.message.reply_text("Ben senin Telegram botunum 😎")

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("🚀 BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()
