from telegram.ext import ApplicationBuilder, MessageHandler, filters
import asyncio

TOKEN = "BOT_TOKEN_BURAYA"


# ---------------- DEPLOY ENGINE ----------------
async def deploy_module(name, message):

    files = ["bot.py", "config.py"]

    total = len(files)

    for i, f in enumerate(files):

        await asyncio.sleep(0.5)

        try:
            await message.edit_text(
                f"🚀 DEPLOY {name}\n\n{int((i+1)/total*100)}%\n{f}"
            )
        except:
            pass

    try:
        await message.edit_text(f"✅ DEPLOY DONE ({name})")
    except:
        pass


# ---------------- HANDLER ----------------
async def handle(update, context):

    text = (update.message.text or "").strip().lower()

    print("IN:", text)

    # START
    if text == "/start":
        await update.message.reply_text("Bot aktif 🚀")
        return

    # DEPLOY
    if text.startswith("/deploy"):

        parts = text.split()
        module = parts[1] if len(parts) > 1 else "full"

        await deploy_module(module, update.message)
        return

    await update.message.reply_text("Komut yok")


# ---------------- MAIN ----------------
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("BOT RUNNING FINAL VERSION")

    app.run_polling()


if __name__ == "__main__":
    main()
