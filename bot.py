from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config
from deploy.engine import deploy_module


async def handle(update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    print("IN:", text)

    # START
    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    # DEPLOY SYSTEM
    if text.startswith("/deploy"):
        parts = text.split()

        module = "full"
        if len(parts) > 1:
            module = parts[1]

        if module not in ["core", "ui", "full"]:
            await update.message.reply_text("Kullanım: /deploy core | ui | full")
            return

        await deploy_module(module, update.message)
        return

    await update.message.reply_text("Komut yok")


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # HER MESAJI AL (EN KRİTİK NOKTA)
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING FINAL STABLE VERSION")

    app.run_polling()


if __name__ == "__main__":
    main()
