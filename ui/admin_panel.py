async def button_handler(update, context):
    q = update.callback_query
    await q.answer()

    if q.data == "status":
        await q.edit_message_text("Bot çalışıyor ✔")

    elif q.data == "ai":
        await q.edit_message_text("AI sistemi aktif ✔")

    elif q.data == "deploy":
        await q.edit_message_text("Deploy tetiklendi ✔")
