async def handle_ui(update, context, text):

    user_id = update.effective_user.id

    if text == "👤 Profil":
        await update.message.reply_text(
            f"👤 Profil\nID: {user_id}\nSystem: V3 PRODUCT MODE"
        )
        return

    if text == "ℹ️ Yardım":
        await update.message.reply_text(
            "ℹ️ Komutlar:\n/start\n/deploy\nButonları kullan"
        )
        return

    if text == "🔥 Durum":
        await update.message.reply_text(
            "🔥 Sistem: STABLE V3 ✔"
        )
        return
