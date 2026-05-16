ADMIN_PASSWORD = "1234"

ADMINS = set()


def is_admin(user_id):
    return user_id in ADMINS


def login_admin(user_id, password):
    if password == ADMIN_PASSWORD:
        ADMINS.add(user_id)
        return True
    return False


def logout_admin(user_id):
    ADMINS.discard(user_id)
