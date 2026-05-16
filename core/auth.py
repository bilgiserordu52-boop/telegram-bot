import json
import os

FILE = "admins.json"


def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def login_admin(user_id, password):
    data = load()

    if password == "1234":
        data[str(user_id)] = True
        save(data)
        return True

    return False


def logout_admin(user_id):
    data = load()

    if str(user_id) in data:
        del data[str(user_id)]
        save(data)

    return True


def is_admin(user_id):
    return str(user_id) in load()
