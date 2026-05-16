import sqlite3

DB = "bot.db"


# =========================
# CONNECTION
# =========================
def conn():
    return sqlite3.connect(DB)


# =========================
# CLEAN LOGS
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

    print("[TASK] logs cleaned")


# =========================
# CLEAN MEMORY
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

    print("[TASK] memory cleaned")


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

    print("[TASK] warnings reset")
