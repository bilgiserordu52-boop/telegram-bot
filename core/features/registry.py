# =========================
# SOL LOB CORE REGISTRY (IMMUTABLE CORE)
# =========================

_FEATURES = {}
_CORE_LOCKED = False


def lock_core():
    global _CORE_LOCKED
    _CORE_LOCKED = True


def is_locked():
    return _CORE_LOCKED


def register_feature(name, func):
    """
    SOL LOB RULE:
    - core locked ise hiçbir şey eklenemez
    """
    global _FEATURES, _CORE_LOCKED

    if _CORE_LOCKED:
        raise Exception("SOL LOB LOCKED: feature registration blocked")

    _FEATURES[name] = func


def get_features():
    """
    Immutable snapshot (asla dışarı mutable ref vermez)
    """
    return dict(_FEATURES)


def get_feature(name):
    return _FEATURES.get(name)


def list_features():
    return list(_FEATURES.keys())


def clear_features():
    """
    SADECE UNLOCK durumunda çalışır
    """
    global _FEATURES, _CORE_LOCKED

    if _CORE_LOCKED:
        raise Exception("SOL LOB LOCKED: cannot clear features")

    _FEATURES = {}


def safe_get_features():
    return dict(_FEATURES)
