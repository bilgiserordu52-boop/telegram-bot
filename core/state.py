import json
import os

USERS_FILE = "users.json"


def load_users():

    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(data):

    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_user(user_id):

    users = load_users()

    if str(user_id) not in users:
        users[str(user_id)] = {
            "messages": 0
        }

    save_users(users)
