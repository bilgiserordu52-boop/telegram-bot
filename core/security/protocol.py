import time
import re

from core.platform.config import get


# =========================
# CONFIG
# =========================
MAX_MESSAGE_LENGTH = get("MAX_MESSAGE_LENGTH")

USER_RATE_LIMIT = get("USER_RATE_LIMIT")

CALLBACK_RATE_LIMIT = get("CALLBACK_RATE_LIMIT")

AUTO_MUTE_SCORE = get("AUTO_MUTE_SCORE")

AUTO_BAN_SCORE = get("AUTO_BAN_SCORE")


# =========================
# MEMORY
# =========================
USER_TRACK = {}

CALLBACK_TRACK = {}

USER_WARNINGS = {}

USER_LAST_MESSAGE = {}


# =========================
# VALIDATION
# =========================
def validate_text(user_id, text):

    if not text:
        return False, "❌ Boş mesaj"

    if len(text) > MAX_MESSAGE_LENGTH:

        add_warning(user_id)

        return False, "⚠️ Mesaj çok uzun"


    # repeated spam
    last = USER_LAST_MESSAGE.get(str(user_id))

    if last == text:

        add_warning(user_id)

        return False, "🚫 Spam algılandı"


    USER_LAST_MESSAGE[str(user_id)] = text


    # emoji flood
    if len(re.findall(r"[🤣😂😎🔥❤️💀]", text)) > 15:

        add_warning(user_id)

        return False, "🚫 Emoji flood"


    # link block
    if "http://" in text or "https://" in text:

        add_warning(user_id)

        return False, "🔒 Link engellendi"


    return True, text


# =========================
# RATE LIMIT
# =========================
def user_rate_limit(user_id):

    now = time.time()

    last = USER_TRACK.get(str(user_id), 0)

    if now - last < USER_RATE_LIMIT:

        add_warning(user_id)

        return False


    USER_TRACK[str(user_id)] = now

    return True


# =========================
# CALLBACK LIMIT
# =========================
def callback_rate_limit(user_id):

    now = time.time()

    last = CALLBACK_TRACK.get(str(user_id), 0)

    if now - last < CALLBACK_RATE_LIMIT:

        add_warning(user_id)

        return False


    CALLBACK_TRACK[str(user_id)] = now

    return True


# =========================
# WARNING SYSTEM
# =========================
def add_warning(user_id):

    current = USER_WARNINGS.get(str(user_id), 0)

    current += 1

    USER_WARNINGS[str(user_id)] = current


def get_warning(user_id):

    return USER_WARNINGS.get(str(user_id), 0)


def should_mute(user_id):

    return get_warning(user_id) >= AUTO_MUTE_SCORE


def should_ban(user_id):

    return get_warning(user_id) >= AUTO_BAN_SCORE
