from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters

import config
from commands.deploy import deploy_cmd
from commands.admin import admin_cmd, rollback_cmd
from commands.message import handle_message
from ui.admin_panel import button_handler


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command_wrapper))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BOT RUNNING FIXED VERSION")
    app.run_polling()


async def handle_command_wrapper(update, context):
    text = update.message.text.lower()

    if text.startswith("/deploy"):
        from deploy.engine import deploy_module

        if "core" in text:
            await deploy_module("core", update.message)
        elif "ui" in text:
            await deploy_module("ui", update.message)
        elif "full" in text:
            await deploy_module("full", update.message)
        return

    if text == "/admin":
        return await admin_cmd(update, context)

    if text == "/rollback":
        return await rollback_cmd(update, context)

    if text == "selam":
        return await update.message.reply_text("Selam 👋")

    return await update.message.reply_text("❓ command not found")


if __name__ == "__main__":
    main()
