from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters

import config
from deploy.engine import deploy_module
from ui.admin_panel import button_handler


async def handle(update, context):
    text = update.message.text.lower()

    if text.startswith("/deploy"):
        if "core" in text:
            await deploy_module("core", update.message)
        elif "ui" in text:
            await deploy_module("ui", update.message)
        elif "full" in text:
            await deploy_module("full", update.message)
        return

    if text == "/start":
        return await update.message.reply_text("Bot aktif")

    return await update.message.reply_text("komut yok")


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BOT RUNNING CLEAN FIX")

    app.run_polling()


if __name__ == "__main__":
    main()
