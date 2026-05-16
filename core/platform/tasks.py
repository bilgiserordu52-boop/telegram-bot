import threading
import time

from core.platform.self_heal import safe_execute


TASKS = []


# =========================
# ADD TASK
# =========================
def add_task(name, interval, callback):

    TASKS.append({
        "name": name,
        "interval": interval,
        "callback": callback,
        "last_run": 0
    })


# =========================
# TASK LOOP
# =========================
def loop():

    while True:

        now = time.time()

        for task in TASKS:

            try:

                if now - task["last_run"] >= task["interval"]:

                    safe_execute(task["callback"])

                    task["last_run"] = now

            except Exception as e:

                print(f"[TASK ERROR] {task['name']} -> {e}")

        time.sleep(1)


# =========================
# START SYSTEM
# =========================
def start_tasks():

    thread = threading.Thread(
        target=loop,
        daemon=True
    )

    thread.start()
