rt config

from core.router import handle_command
from ui.admin_panel import button_handler


# =========================
# BOT ENTRY POINT
# =========================
def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # ALL TEXT TRAFFIC → ROUTER
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_command)
    )

    # INLINE BUTTONS
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 BOT RUNNING (V3 ORCHESTRATOR MODE)")

    app.run_polling()


if __name__ == "__main__":
    main()
