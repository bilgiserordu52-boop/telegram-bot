# =========================
# PLATFORM CONFIG
# =========================

CONFIG = {

    # =========================
    # BOT
    # =========================
    "BOT_NAME": "AI CORE",

    "VERSION": "3.0",

    "DEBUG": True,


    # =========================
    # SECURITY
    # =========================
    "MAX_MESSAGE_LENGTH": 500,

    "USER_RATE_LIMIT": 1.5,

    "CALLBACK_RATE_LIMIT": 1.0,

    "AUTO_MUTE_SCORE": 3,

    "AUTO_BAN_SCORE": 5,


    # =========================
    # DATABASE
    # =========================
    "MAX_MEMORY_PER_USER": 25,

    "MAX_LOGS": 300,


    # =========================
    # MONITORING
    # =========================
    "WATCHDOG_INTERVAL": 3600,

    "MAX_GLOBAL_MEMORY": 1000,

    "MAX_GLOBAL_LOGS": 500,


    # =========================
    # AI
    # =========================
    "AI_ENABLED": True,

    "AI_MEMORY_ENABLED": True,

    "AI_CONTEXT_LIMIT": 5,


    # =========================
    # ADMIN
    # =========================
    "ADMIN_ENABLED": True,

    "MONITOR_ENABLED": True,

    "SECURITY_ENABLED": True
}


# =========================
# GETTER
# =========================
def get(key, default=None):

    return CONFIG.get(key, default)
