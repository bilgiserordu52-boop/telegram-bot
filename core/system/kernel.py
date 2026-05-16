import time
import threading
import sqlite3
import shutil
import os

DB = "bot.db"

START_TIME = time.time()

ACTIVE_USERS = set()


# =========================
# CONNECTION
# =========================
def conn():
    return sqlite3.connect(DB)


# =========================
# ACTIVE USER TRACK
# =========================
def touch_user(user_id):
    ACTIVE_USERS.add(str(user_id))


def active_users():
    return len(ACTIVE_USERS)


# =========================
# UPTIME
# =========================
def uptime():

    seconds = int(time.time() - START_TIME)

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h}h {m}m {s}s"


# =========================
# AUTO BACKUP
# =========================
def backup_db():

    if not os.path.exists(DB):
        return

    os.makedirs("backups", exist_ok=True)

    ts = int(time.time())

    shutil.copy(
        DB,
        f"backups/backup_{ts}.db"
    )


# =========================
# CLEAN OLD MEMORY
# =========================
def cleanup_memory():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    DELETE FROM memory
    WHERE id NOT IN (
        SELECT id FROM memory
        ORDER BY id DESC
        LIMIT 1000
    )
    """)

    c.commit()
    c.close()


# =========================
# CLEAN OLD LOGS
# =========================
def cleanup_logs():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    DELETE FROM logs
    WHERE id NOT IN (
        SELECT id FROM logs
        ORDER BY id DESC
        LIMIT 500
    )
    """)

    c.commit()
    c.close()


# =========================
# RESET WARNINGS
# =========================
def reset_warnings():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    UPDATE users
    SET warnings=0
    """)

    c.commit()
    c.close()


# =========================
# WATCHDOG LOOP
# =========================
def watchdog():

    while True:

        try:

            backup_db()

            cleanup_memory()

            cleanup_logs()

            reset_warnings()

        except Exception as e:
            print("WATCHDOG ERROR:", e)

        time.sleep(3600)


# =========================
# START KERNEL
# =========================
def start_kernel():

    t = threading.Thread(
        target=watchdog,
        daemon=True
    )

    t.start()
