# =========================
# ENGINE CORE
# =========================

from core.ui.builder import build_ui_text, build_keyboard
from core.features.engine import execute
from core.ai.evolve import evolve
from core.ai.real_evolve import evolve_real

def handle(update, context):

    text = update.message.text


    # =========================
    # AI EVOLVE MODE COMMAND
    # =========================
    if text.startswith("/evolve "):

        command = text.replace("/evolve ", "")

        result = evolve(command)

        update.message.reply_text(str(result))
        return

    
    if text.startswith("/revolve "):

        command = text.replace("/revolve ", "")

        result = evolve_real(command)

        update.message.reply_text(str(result))
        return
    # =========================
    # UI PANEL
    # =========================
    if text == "/ui":

        ui_text = build_ui_text()
        keyboard = build_keyboard()

        update.message.reply_text(
            ui_text + "\n\n" + str(keyboard)
        )
        return


    # =========================
    # RUN FEATURE
    # =========================
    if text.startswith("/run "):

        feature_name = text.replace("/run ", "")

        result = execute(feature_name)

        update.message.reply_text(str(result))
        return


    # =========================
    # DEFAULT AI RESPONSE
    # =========================
    if text:

        result = execute("think", text)

        update.message.reply_text(str(result))
