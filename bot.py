import os
import time
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

VERSION = time.strftime("%Y.%m.%d-%H%M")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🤖 Bot aktif\n📦 Versiyon: {VERSION}")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == "selam":
        await update.message.reply_text("Selam 👋")

    elif text == "naber":
        await update.message.reply_text("İyiyim 👍")

    elif text == "version":
        await update.message.reply_text(f"📦 {VERSION}")

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

if __name__ == "__main__":
    main()
