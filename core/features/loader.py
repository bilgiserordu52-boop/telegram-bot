from core.features.registry import register_feature


# =========================
# FEATURE DEFINITIONS
# =========================

def ping():
    return {"status": "ok", "response": "pong"}


def selam():
    return {"status": "ok", "response": "Selam 👋"}


def system():
    return {"status": "ok", "response": "system ready"}


def echo():
    return {"status": "ok", "response": "echo"}


# =========================
# LOAD SYSTEM (SAFE REGISTER)
# =========================
def load_features():
    register_feature("ping", ping)
    register_feature("selam", selam)
    register_feature("system", system)
    register_feature("echo", echo)

    return 4
from core.features.registry import register_feature


def load_features():
    from core.features.registry import _FEATURES
    _FEATURES.clear()

    register_feature("ping", ping)
    register_feature("selam", selam)
    register_feature("system", system)
    register_feature("echo", echo)

    return len(_FEATURES)
