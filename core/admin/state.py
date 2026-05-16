DMIN_STATE = {}
STACK = {}


def set_admin_state(user_id, state):
    ADMIN_STATE[str(user_id)] = state


def get_admin_state(user_id):
    return ADMIN_STATE.get(str(user_id), "dashboard")


def push_admin_stack(user_id, state):
    STACK.setdefault(str(user_id), []).append(state)


def pop_admin_stack(user_id):
    stack = STACK.get(str(user_id), [])

    if len(stack) > 1:
        stack.pop()

    return stack[-1] if stack else "dashboard"
