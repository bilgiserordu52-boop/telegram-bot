from core.system import restart_bot
from core.autoupdate import update_and_restart
from deploy.engine import deploy_module


async def route(update, context):

    text = update.message.text

    print("RAW:", repr(text))

    # TEXT TEMİZLE
    clean = (
        text.replace("👤", "")
        .replace("🔥", "")
        .replace("ℹ️", "")
        .strip()
    )

    print("CLEAN:", clean)

    # START
    if text == "/start":
        await update.message.reply_text(
            "🤖 Autonomous Bot Active"
        )
        return

    # SELAM
    if text.lower() == "selam":
        await update.message.reply_text(
            "selam 😄"
        )
        return

    # STATUS
    if text == "/status":

        await update.message.reply_text(
            "🟢 SYSTEM ONLINE\nSelf-Healing: OFF"
        )
        return

    # RESTART
    if text == "/restart":

        await update.message.reply_text(
            "♻️ Restarting bot..."
        )

        restart_bot()
        return

    # UPDATE
    if text == "/update":

        await update.message.reply_text(
            "🔄 Updating system..."
        )

        update_and_restart()
        return

    # DEPLOY
    if text.startswith("/deploy"):

        name = (
            text.split()[1]
            if len(text.split()) > 1
            else "full"
        )

        await deploy_module(name, update.message)
        return

    # PROFIL
    if "Profil" in clean:

        await update.message.reply_text(
            "👤 Profil çalıştı"
        )
        return

    # DURUM
    if "Durum" in clean:

        await update.message.reply_text(
            "🔥 Sistem aktif"
        )
        return

    # YARDIM
    if "Yardım" in clean:

        await update.message.reply_text(
            "ℹ️ Yardım menüsü"
        )
        return

    # UNKNOWN
    await update.message.reply_text(
        "❗ Anlaşılmadı"
    )
