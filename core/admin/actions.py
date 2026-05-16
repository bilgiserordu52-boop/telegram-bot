from core.state import load_users, save_users


# =========================
# USERS
# =========================
def get_users():
    return load_users()


def get_user_count():
    return len(load_users())


# =========================
# MESSAGES
# =========================
def get_message_count():
    users = load_users()
    return sum(u.get("messages", 0) for u in users.values())


# =========================
# BAN SYSTEM
# =========================
def ban_user(user_id):
    users = load_users()
    uid = str(user_id)

    if uid in users:
        users[uid]["banned"] = True
        save_users(users)


def unban_user(user_id):
    users = load_users()
    uid = str(user_id)

    if uid in users:
        users[uid]["banned"] = False
        save_users(users)


def is_banned(user_id):
    users = load_users()
    uid = str(user_id)

    return users.get(uid, {}).get("banned", False)
