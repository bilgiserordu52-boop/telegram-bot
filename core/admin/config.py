from core.config import TOKEN

ADMIN_CONFIG = {
    "bot_token": TOKEN,
    "maintenance": False,
    "debug": False
}


# =========================
# CONFIG GETTER
# =========================
def get_config():
    return ADMIN_CONFIG


# =========================
# CONFIG SETTER
# =========================
def set_config(key, value):
    ADMIN_CONFIG[key] = value


# =========================
# TOKEN CONTROL (BASİT VIEW)
# =========================
def get_token_preview():
    token = ADMIN_CONFIG["bot_token"]
    return token[:10] + "..."
