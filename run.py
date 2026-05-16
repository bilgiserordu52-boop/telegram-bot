# run.py

from core.single_core import core

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


TOKEN = "8945412773:AAFRsFVmYqqcgzSwidMVo-VN3uK59ELEiEE"


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot aktif")


# =========================
# MENU (REAL UI FIX)
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ui = core.ui()

    keyboard = ReplyKeyboardMarkup(ui["keyboard"], resize_keyboard=True)

    await update.message.reply_text(ui["text"], reply_markup=keyboard)


# =========================
# STATUS
# =========================
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    st = core.status()

    await update.message.reply_text(str(st))


# =========================
# MESSAGE ROUTER
# =========================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    result = core.run(text)

    if isinstance(result, dict) and result.get("status") == "ok":
        await update.message.reply_text(result.get("response", "OK"))
    else:
        await update.message.reply_text(str(result))


# =========================
# MAIN
# =========================
def main():

    core.boot()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🟢 BOT RUNNING (SINGLE CORE v2 FINAL)")

    app.run_polling()


if __name__ == "__main__":
    main()
