import traceback

from core.features.loader import load_features
from core.features.registry import get_features
from core.features.engine import execute
from core.ui.builder import build_keyboard, build_ui_text


SYSTEM_STATE = {
    "features_loaded": False,
    "registry_ok": False,
    "ui_ok": False,
    "engine_ok": False,
}


def run_stabilizer():
    try:
        print("🧠 SOL LOB CHECK START")

        load_features()
        SYSTEM_STATE["features_loaded"] = True

        features = get_features()
        SYSTEM_STATE["registry_ok"] = True

        test = execute("ping")
        SYSTEM_STATE["engine_ok"] = isinstance(test, dict)

        build_keyboard()
        build_ui_text()
        SYSTEM_STATE["ui_ok"] = True

        print("\n📊 CORE STATUS:")
        for k, v in SYSTEM_STATE.items():
            print(f"- {k}: {v}")

        print("\n🔒 SOL LOB STABLE (NO AUTO FIX)")

    except Exception:
        print("💥 STABILIZER CRASH")
        print(traceback.format_exc())
