# core/core_v2/brain.py

FEATURES = {}


def register(name, func):
    FEATURES[name] = func


def get(name):
    return FEATURES.get(name)


def all_features():
    return FEATURES


def execute(name, *args, **kwargs):
    name = (name or "").lower().strip()

    # built-ins
    if name == "ping":
        return {"status": "ok", "response": "pong"}

    if name == "selam":
        return {"status": "ok", "response": "Selam 👋"}

    feature = FEATURES.get(name)

    if not feature:
        return {
            "status": "error",
            "message": f"Feature '{name}' not found",
            "available": list(FEATURES.keys())
        }

    try:
        return {"status": "ok", "result": feature(*args, **kwargs)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
