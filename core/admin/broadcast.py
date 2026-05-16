from core.state import load_users


# =========================
# REAL BROADCAST
# =========================
async def send_broadcast(app, text):
    users = load_users()
    sent = 0

    for uid in users.keys():
        try:
            await app.bot.send_message(chat_id=int(uid), text=text)
            sent += 1
        except:
            pass

    return sent
