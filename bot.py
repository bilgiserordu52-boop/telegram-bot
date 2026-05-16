from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from core.right_lob_gateway import gateway


TOKEN = "8945412773:AAFRsFVmYqqcgzSwidMVo-VN3uK59ELEiEE"


# -------------------------
# START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot aktif\n\n/menu ile panel aç"
    )


# -------------------------
# MENU
# -------------------------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ui = gateway.ui()

    keyboard = ReplyKeyboardMarkup(
        ui["keyboard"],
        resize_keyboard=True
    )

    await update.message.reply_text(ui["text"], reply_markup=keyboard)


# -------------------------
# CALLBACK HANDLER (INLINE BUTTONS)
# -------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    result = gateway.handle_sync(data)

    if isinstance(result, dict):
        msg = result.get("response") or result.get("message") or str(result)
    else:
        msg = str(result)

    await query.edit_message_text(msg)


# -------------------------
# MESSAGE HANDLER
# -------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    result = gateway.handle_sync(text)

    if isinstance(result, dict):
        msg = result.get("response") or result.get("message") or str(result)
    else:
        msg = str(result)

    await update.message.reply_text(msg)


# -------------------------
# MAIN
# -------------------------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🟢 PHASE 3 BOT RUNNING...")
    app.run_polling()


if __name__ == "__main__":
    main()
