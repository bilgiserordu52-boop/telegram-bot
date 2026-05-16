from core.features.loader import load_features
from core.features.registry import get_features
from core.features.engine import execute
from core.ui.builder import build_keyboard, build_ui_text
from core.stabilizer import run_stabilizer


class SingleCore:
    def __init__(self):
        self.ready = False

    def boot(self):
        print("🧠 CORE v3 BOOTING...")

        run_stabilizer()

        self.ready = True

        features = get_features()

        print(f"🟢 CORE READY | FEATURES: {len(features)}")

    def run(self, command):
        return execute(command)

    def ui(self):
        features = get_features()

        if len(features) == 0:
            return {
                "text": "⚠️ SYSTEM NOT READY",
                "keyboard": [["RESTART"]]
            }

        return {
            "text": build_ui_text(),
            "keyboard": build_keyboard()
        }

    def status(self):
        features = get_features()

        return {
            "ready": self.ready,
            "features": len(features),
            "engine": execute("ping")
        }


core = SingleCore()
