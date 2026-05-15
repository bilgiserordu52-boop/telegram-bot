import os
import sys
import time


def restart_bot():

    print("RESTARTING BOT...")

    time.sleep(1)

    os.execv(
        sys.executable,
        [sys.executable, "bot.py"]
    )
