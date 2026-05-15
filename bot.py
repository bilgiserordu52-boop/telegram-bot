from telegram.ext import ApplicationBuilder, MessageHandler, filters

import config
from deploy.engine import deploy_module


async def handle(update, context):
    text = update.message.text.lower()

    if text.startswith("/deploy"):
        if "core" in text:
            await deploy_module("core", update.message)
        elif "ui" in text:
            await deploy_module("ui", update.message)
        elif "full" in text:
            await deploy_module("full", update.message)
        else:
            await update.message.reply_text("Use: /deploy core|ui|full")
        return

    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    await update.message.reply_text("Komut yok")


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # ⚠️ KRİTİK: COMMAND FILTER YOK
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING CLEAN V6")
    app.run_polling()


if __name__ == "__main__":
    main()
