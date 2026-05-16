from core.features.engine import auto_learn


# =========================
# SIMPLE FEATURE CREATOR
# =========================
def create_feature(name, response_text):

    def feature(*args, **kwargs):
        return response_text

    return auto_learn(name, feature)
