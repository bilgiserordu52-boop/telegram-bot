	mport json
import os

FILE = "admin_data.json"


# =========================
# LOAD / SAVE
# =========================
def load():
    if not os.path.exists(FILE):
        return {"banned": [], "muted": [], "logs": []}

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# BAN SYSTEM
# =========================
def ban_user(user_id):

    data = load()

    if str(user_id) not in data["banned"]:
        data["banned"].append(str(user_id))

    save(data)


def unban_user(user_id):

    data = load()

    if str(user_id) in data["banned"]:
        data["banned"].remove(str(user_id))

    save(data)


def is_banned(user_id):

    data = load()
    return str(user_id) in data["banned"]


# =========================
# MUTE SYSTEM
# =========================
def mute_user(user_id):

    data = load()

    if str(user_id) not in data["muted"]:
        data["muted"].append(str(user_id))

    save(data)


def unmute_user(user_id):

    data = load()

    if str(user_id) in data["muted"]:
        data["muted"].remove(str(user_id))

    save(data)


def is_muted(user_id):

    data = load()
    return str(user_id) in data["muted"]


# =========================
# LOG SYSTEM (ADIM 4 FIXED)
# =========================
def add_log(user_id, text, reply):

    data = load()

    if "logs" not in data:
        data["logs"] = []

    data["logs"].append({
        "user": str(user_id),
        "text": text,
        "reply": reply
    })

    # =========================
    # LOG PROTECTION (FIX)
    # =========================
    MAX_LOG_SIZE = 100
    data["logs"] = data["logs"][-MAX_LOG_SIZE:]

    save(data)


def get_logs(limit=10):

    data = load()

    if "logs" not in data:
        return []

    return data["logs"][-limit:]
