from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config
from deploy.engine import deploy_module


async def handle(update, context):
    text = update.message.text.lower().strip()

    print("MSG:", text)

    # -------------------------
    # DEPLOY SYSTEM
    # -------------------------
    if text.startswith("/deploy"):
        if "core" in text:
            await deploy_module("core", update.message)
            return

        if "ui" in text:
            await deploy_module("ui", update.message)
            return

        if "full" in text:
            await deploy_module("full", update.message)
            return

        await update.message.reply_text("Kullanım: /deploy core|ui|full")
        return

    # -------------------------
    # START
    # -------------------------
    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    # -------------------------
    # DEFAULT
    # -------------------------
    await update.message.reply_text("Komut tanınmadı")


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # ⚠️ HER MESAJI AL
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING FINAL CLEAN SYSTEM")

    app.run_polling()


if __name__ == "__main__":
    main()
