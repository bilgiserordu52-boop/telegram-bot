import json
import os


FILE = "bond.json"


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
# GET BOND
# =========================
def get_bond(user_id):
    data = load()
    return data.get(str(user_id), 0)


# =========================
# ADD BOND
# =========================
def add_bond(user_id, amount=1):

    data = load()
    uid = str(user_id)

    if uid not in data:
        data[uid] = 0

    data[uid] += amount
    save(data)

    return data[uid]


# =========================
# DECAY (optional future use)
# =========================
def decay_bond(user_id):

    data = load()
    uid = str(user_id)

    if uid in data:
        data[uid] = max(0, data[uid] - 1)
        save(data)

    return data.get(uid, 0)
