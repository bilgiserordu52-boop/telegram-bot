from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config
from deploy.engine import deploy_module


async def handle(update, context):
    text = update.message.text or ""
    text = text.lower().strip()

    print("MSG:", text)

    # START
    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    # DEPLOY (EN SADE VE GARANTİ PARSE)
    if "/deploy" in text:
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

    # ⚠️ KRİTİK: HER ŞEYİ AL
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING FIXED ROUTER FINAL")

    app.run_polling()


if __name__ == "__main__":
    main()
