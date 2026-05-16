SCREENS = {}
USER_SCREEN = {}
USER_STACK = {}


# =========================
# REGISTER SCREEN
# =========================
def screen(name):
    def wrapper(func):
        SCREENS[name] = func
        return func
    return wrapper


# =========================
# SET SCREEN
# =========================
def set_screen(user_id, screen_name):
    uid = str(user_id)
    USER_SCREEN[uid] = screen_name

    USER_STACK.setdefault(uid, [])
    USER_STACK[uid].append(screen_name)


# =========================
# GET SCREEN
# =========================
def get_screen(user_id):
    return USER_SCREEN.get(str(user_id), "home")


# =========================
# BACK
# =========================
def back(user_id):
    uid = str(user_id)
    stack = USER_STACK.get(uid, [])

    if len(stack) > 1:
        stack.pop()
        USER_SCREEN[uid] = stack[-1]
        return stack[-1]

    return "home"
