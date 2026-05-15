from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config
from deploy.engine import deploy_module


async def handle(update, context):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip().lower()

    print("INCOMING:", text)  # DEBUG

    # ---------------- DEPLOY ----------------
    if text.startswith("/deploy"):
        parts = text.split()

        module = "full"
        if len(parts) > 1:
            module = parts[1]

        if module not in ["core", "ui", "full"]:
            await update.message.reply_text("Usage: /deploy core|ui|full")
            return

        await deploy_module(module, update.message)
        return

    # ---------------- START ----------------
    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    await update.message.reply_text("Komut yok")


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # ⚠️ TÜM MESAJLARI AL
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING FIXED ROUTER V2")

    app.run_polling()


if __name__ == "__main__":
    main()
