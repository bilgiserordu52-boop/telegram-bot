from core.platform.cluster import (
    heartbeat,
    register_error,
    recovery
)


# =========================
# SAFE EXECUTOR
# =========================
def safe_execute(func):

    try:
        heartbeat()
        return func()

    except Exception as e:

        register_error()
        recovery()

        print("[SELF HEAL] recovered from:", e)
