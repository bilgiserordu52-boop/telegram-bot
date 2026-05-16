import time

USER_TRACK = {}

MAX_LEN = 500
LIMIT_SECONDS = 2


def clean_input(text):

    if not text:
        return False, "Boş mesaj"

    if len(text) > MAX_LEN:
        return False, "⚠️ Mesaj çok uzun"

    return True, text


def rate_limit(user_id):

    now = time.time()

    last = USER_TRACK.get(str(user_id), 0)

    if now - last < LIMIT_SECONDS:
        return False

    USER_TRACK[str(user_id)] = now
    return True
