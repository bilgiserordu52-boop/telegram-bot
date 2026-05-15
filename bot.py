from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters

import config
from core.router import handle_command
from ui.admin_panel import button_handler


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BOT RUNNING V4 SYSTEM")
    app.run_polling()


if __name__ == "__main__":
    main()
