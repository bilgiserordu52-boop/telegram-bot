import json
import os

FILE = "roles.json"
LOCK_FILE = "bootstrap.lock"


def load_roles():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save_roles(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def is_bootstrapped():
    return os.path.exists(LOCK_FILE)


def bootstrap_superadmin(user_id):

    # already initialized
    if is_bootstrapped():
        return False

    roles = load_roles()

    # FIRST USER = SUPERADMIN
    roles[str(user_id)] = "superadmin"

    save_roles(roles)

    # lock system
    with open(LOCK_FILE, "w") as f:
        f.write("locked")

    return True
