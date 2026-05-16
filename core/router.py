from core.screen import SCREENS
from core.state import set_state, push_stack, pop_stack


# =========================
# SPA RENDER ENGINE
# =========================
async def render(update, text, keyboard):

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text,
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )


# =========================
# ROUTER
# =========================
async def route(update, context):

    user_id = update.effective_user.id

    # =========================
    # CALLBACK UI (SPA CORE)
    # =========================
    if update.callback_query:

        data = update.callback_query.data

        if data == "back":
            state = pop_stack(user_id)
            set_state(user_id, state)
            handler = SCREENS.get(state)
            if handler:
                await handler(update, render)
            return

        if data in SCREENS:
            set_state(user_id, data)
            push_stack(user_id, data)

            handler = SCREENS[data]
            await handler(update, render)
            return

        return

    # =========================
    # TEXT INPUT
    # =========================
    text = update.message.text.strip().lower()

    if text == "/start":
        set_state(user_id, "home")
        push_stack(user_id, "home")
        await SCREENS["home"](update, render)
        return

    await update.message.reply_text("❗ Anlaşılmadı")
