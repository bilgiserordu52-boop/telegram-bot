from telegram.ext import ApplicationBuilder, MessageHandler, filters
import config


async def handle(update, context):
    text = (update.message.text or "").strip()

    print("GELEN:", text)

    # START
    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    # DEPLOY TEST (SADECE MESAJ KONTROL)
    if text.startswith("/deploy"):
        await update.message.reply_text(f"Deploy yakalandı: {text}")
        return

    await update.message.reply_text("Komut yok")


def main():
    app = ApplicationBuilder().token(config.TOKEN).build()

    # ⚠️ EN ÖNEMLİ SATIR
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING MINIMAL FIX")

    app.run_polling()


if __name__ == "__main__":
    main()
