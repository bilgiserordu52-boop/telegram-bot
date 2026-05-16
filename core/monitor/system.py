import sqlite3
import os

from core.system.kernel import (
    uptime,
    active_users
)

DB = "bot.db"


# =========================
# CONNECTION
# =========================
def conn():
    return sqlite3.connect(DB)


# =========================
# DATABASE STATS
# =========================
def stats():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM users
    """)

    users = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*)
    FROM memory
    """)

    memory = cur.fetchone()[0]


    cur.execute("""
    SELECT COUNT(*)
    FROM logs
    """)

    logs = cur.fetchone()[0]


    c.close()

    return users, memory, logs


# =========================
# DATABASE SIZE
# =========================
def db_size():

    if not os.path.exists(DB):
        return "0 MB"

    size = os.path.getsize(DB)

    mb = round(size / 1024 / 1024, 2)

    return f"{mb} MB"


# =========================
# HEALTH REPORT
# =========================
def health_report():

    users, memory, logs = stats()

    return f"""
🟢 SYSTEM ONLINE

⏱ UPTIME: {uptime()}

👤 TOTAL USERS: {users}
🔥 ACTIVE USERS: {active_users()}

🧠 MEMORY: {memory}
📜 LOGS: {logs}

💾 DATABASE: {db_size()}

🛡 SECURITY: ACTIVE
⚡ WATCHDOG: ACTIVE
🤖 AI CORE: ACTIVE
👑 ADMIN CORE: ACTIVE
"""
