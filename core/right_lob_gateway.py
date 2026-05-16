from core.features.engine import execute
from core.ui.builder import build_keyboard, build_ui_text


class RightLobGateway:

    def handle_sync(self, text, context=None):
        text = str(text).strip()

        # slash normalize
        if text.startswith("/"):
            text = text[1:]

        return execute(text)

    async def handle(self, text, context=None):
        return self.handle_sync(text, context)

    def ui(self):
        return {
            "text": build_ui_text(),
            "keyboard": build_keyboard()
        }


gateway = RightLobGateway()
