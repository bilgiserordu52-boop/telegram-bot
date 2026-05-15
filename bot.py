import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from commands.start import start_cmd
from commands.admin import admin_cmd
from commands.message import handle_message
from ui.admin_panel import button_handler

import config

def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BOT RUNNING (MODULAR)")
    app.run_polling()

if __name__ == "__main__":
    main()
