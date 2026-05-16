import json
import os

FILE = "self.json"


# =========================
# LOAD / SAVE
# =========================
def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# INIT USER SELF PROFILE
# =========================
def init_user(user_id):

    data = load()
    uid = str(user_id)

    if uid not in data:
        data[uid] = {
            "messages": 0,
            "style": "default",
            "memory_hits": 0
        }

    save(data)
    return data[uid]


# =========================
# UPDATE SELF STATE
# =========================
def update_self(user_id, key, value):

    data = load()
    uid = str(user_id)

    if uid not in data:
        init_user(user_id)
        data = load()

    data[uid][key] = value
    save(data)


# =========================
# GET SELF
# =========================
def get_self(user_id):

    data = load()
    return data.get(str(user_id), None)
