from ai.review import ai_review

async def handle_message(update, context):
    text = update.message.text
    uid = update.effective_user.id

    if text.lower() == "selam":
        return await update.message.reply_text("Selam 👋")

    if "def " in text or "print(" in text:
        result = ai_review(text)

        await update.message.reply_text(
            f"AI: {result['level']} | score: {result['score']}"
        )
