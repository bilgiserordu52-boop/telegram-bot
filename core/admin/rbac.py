import json
import os

FILE = "roles.json"


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_role(user_id):
    data = load()
    return data.get(str(user_id), "user")


def set_role(user_id, role):
    data = load()
    data[str(user_id)] = role
    save(data)


def is_admin(user_id):
    return get_role(user_id) in ["admin", "superadmin"]


def is_superadmin(user_id):
    return get_role(user_id) == "superadmin"
