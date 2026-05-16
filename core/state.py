import json
import os

USERS_FILE = "users.json"

USER_STATE = {}
USER_STACK = {}


def set_state(user_id, state):
    USER_STATE[str(user_id)] = state


def get_state(user_id):
    return USER_STATE.get(str(user_id), "home")


def push_stack(user_id, state):
    uid = str(user_id)
    USER_STACK.setdefault(uid, [])
    USER_STACK[uid].append(state)


def pop_stack(user_id):
    uid = str(user_id)
    stack = USER_STACK.get(uid, [])

    if len(stack) > 1:
        stack.pop()
        return stack[-1]

    return "home"
