from core.admin.state import set_admin_state, push_admin_stack
from core.admin.actions import get_user_count, get_message_count


# =========================
# DASHBOARD
# =========================
async def dashboard(update, render):
    user_id = update.effective_user.id
    set_admin_state(user_id, "dashboard")

    text = (
        "🛠 ADMIN DASHBOARD\n\n"
        f"👥 Users: {get_user_count()}\n"
        f"💬 Messages: {get_message_count()}"
    )

    keyboard = [
        {"text": "📊 Stats", "data": "stats"},
        {"text": "👤 Users", "data": "users"},
        {"text": "📢 Broadcast", "data": "broadcast"},
        {"text": "🚪 Logout", "data": "logout"},
    ]

    await render(update, text, keyboard)


# =========================
# STATS
# =========================
async def stats(update, render):
    user_id = update.effective_user.id
    set_admin_state(user_id, "stats")
    push_admin_stack(user_id, "stats")

    text = "📊 REAL STATS PANEL"

    keyboard = [
        {"text": "🔙 Back", "data": "back"},
        {"text": "🏠 Home", "data": "dashboard"},
    ]

    await render(update, text, keyboard)


# =========================
# USERS
# =========================
async def users(update, render):
    user_id = update.effective_user.id
    set_admin_state(user_id, "users")
    push_admin_stack(user_id, "users")

    text = "👤 USERS PANEL (REAL DATA)"

    keyboard = [
        {"text": "🔙 Back", "data": "back"},
        {"text": "🏠 Home", "data": "dashboard"},
    ]

    await render(update, text, keyboard)


# =========================
# BROADCAST
# =========================
async def broadcast(update, render):
    user_id = update.effective_user.id
    set_admin_state(user_id, "broadcast")
    push_admin_stack(user_id, "broadcast")

    text = "📢 BROADCAST PANEL"

    keyboard = [
        {"text": "📡 Send Message", "data": "broadcast_send"},
        {"text": "🔙 Back", "data": "back"},
        {"text": "🏠 Home", "data": "dashboard"},
    ]

    await render(update, text, keyboard)


# =========================
# EXIT
# =========================
async def exit_admin(update, render):
    await render(update, "🚪 Admin panel kapatıldı")
