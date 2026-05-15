from telegram.ext import ApplicationBuilder, MessageHandler, filters

from core.router import route

TOKEN = "8945412773:AAFRsFVmYqqcgzSwidMVo-VN3uK59ELEiEE"


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, route))

    print("🚀 BOT V3 PRODUCT MODE RUNNING")

    app.run_polling()


if __name__ == "__main__":
    main()
