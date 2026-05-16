# core/core_v2/ui.py

from core.core_v2.brain import all_features


def build_keyboard():
    return list(all_features().keys())


def build_ui_text():
    return "🤖 BOT V2 ACTIVE\n\n" + "\n".join(all_features().keys())
