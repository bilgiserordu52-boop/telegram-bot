import subprocess
import os
import sys
import time


def update_and_restart():

    print("CHECKING UPDATES...")

    result = subprocess.run(
        ["git", "pull"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    print("RESTARTING BOT...")

    time.sleep(1)

    os.execv(
        sys.executable,
        [sys.executable, "bot.py"]
    )
