from core.features.registry import get_features

def build_keyboard():
    features = get_features()

    if not features:
        return [["EMPTY"]]

    # inline + reply uyumlu
    return [[k] for k in features.keys()]


def build_ui_text():
    features = get_features()

    if not features:
        return "EMPTY SYSTEM"

    text = "🤖 BOT CONTROL PANEL\n\nFEATURES:\n"

    for k in features.keys():
        text += f"- {k}\n"

    return text
