import time
import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8945412773:AAFRsFVmYqqcgzSwidMVo-VN3uK59ELEiEE"
ADMIN_ID = 8607713044

users = load_users()
admins = load_admins()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


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

def is_admin(uid):
    return uid in admins_sessions and (time.time() - admin_sessions[uid]) < SESSION_TIMEOUT


def count_users():
    return len(users)


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("🤖 Info", callback_data="info")]
    ])


def admin_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("👮 Admin Panel", callback_data="admin")],
        [InlineKeyboardButton("➕ Admin Ekle", callback_data="add_admin")],
        [InlineKeyboardButton("➖ Admin Sil", callback_data="remove_admin")],
        [InlineKeyboardButton("🔙 Geri", callback_data="back")]
    ])


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Geri", callback_data="back")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    users.add(uid)

    if is_admin(uid):
        touch(uid)
        await update.message.reply_text("👮 Admin Menü", reply_markup=admin_menu())
    else:
        await update.message.reply_text("👤 Kullanıcı Menü", reply_markup=main_menu())


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if is_admin(uid):
        touch(uid)
        await update.message.reply_text("👮 Admin Menü", reply_markup=admin_menu())
    else:
        await update.message.reply_text("👤 Kullanıcı Menü", reply_markup=main_menu())


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text.lower()

    users.add(uid)
    save_users(users)
    logger.info(f"{uid}: {text}")

    if text == "selam":
        await update.message.reply_text("Selam 👋")


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
            f"📊 Kullanıcı sayısı: {count_users()}",
            reply_markup=back_menu()
        )

    elif query.data == "info":
        await query.edit_message_text(
            "🤖 Bot aktif",
            reply_markup=back_menu()
        )

    elif query.data == "admin":
        if is_admin(uid):
            await query.edit_message_text("👮 Admin Panel", reply_markup=admin_menu())
        else:
            await query.edit_message_text("❌ Yetki yok", reply_markup=back_menu())

    elif query.data == "add_admin":
        await query.edit_message_text("➕ Admin ekleme", reply_markup=back_menu())

    elif query.data == "remove_admin":
        await query.edit_message_text("➖ Admin silme", reply_markup=back_menu())


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))
    app.add_handler(CallbackQueryHandler(button))

    print("🚀 BOT RUNNING")
    app.run_polling()


if __name__ == "__main__":
    main()
