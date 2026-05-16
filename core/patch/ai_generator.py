# =========================
# AI PATCH GENERATOR v1
# =========================

from core.patch.engine import patch


# =========================
# SIMPLE AI TRANSLATOR
# (natural language → patch command)
# =========================
def generate_patch_request(text):

    text = text.lower()

    # -------------------------
    # FEATURE ADD
    # -------------------------
    if "feature ekle" in text or "ekle feature" in text:

        # fake feature extraction
        if "selam" in text:

            return {
                "file": "core/features/loader.py",
                "anchor": "register_feature",
                "code": """
def selam():
    return "Selam 👋"

register_feature("selam", selam)
"""
            }

    # -------------------------
    # MODIFY CONFIG
    # -------------------------
    if "debug" in text:

        return {
            "file": "config.py",
            "search": "DEBUG = False",
            "replace": "DEBUG = True"
        }

    # -------------------------
    # DEFAULT RESPONSE
    # -------------------------
    return {
        "error": "Bu komut henüz öğrenilmedi"
    }


# =========================
# APPLY GENERATED PATCH
# =========================
def apply_ai_patch(user_text):

    command = generate_patch_request(user_text)

    if "error" in command:
        return command

    return patch(
        file_path=command.get("file"),
        search=command.get("search"),
        replace=command.get("replace"),
        anchor=command.get("anchor"),
        code=command.get("code")
    )
