import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= ENV =================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607713044"))

# ================= LOG =================
logging.basicConfig(level=logging.INFO)

# ================= BOT =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot yeniden başladı!")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == "selam":
        await update.message.reply_text("Selam 👋")

    elif text == "naber":
        await update.message.reply_text("İyiyim 👍")

    elif text == "bot":
        await update.message.reply_text("Çalışıyorum 🤖")

# ================= MAIN =================
def main():
    if not TOKEN:
        print("TOKEN yok")
        return

    print("BOT STARTING")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")
    app.run_polling()

# ================= RUN =================
if __name__ == "__main__":
    main()
