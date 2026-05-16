import sqlite3

DB = "bot.db"


# =========================
# CONNECTION
# =========================
def conn():
    return sqlite3.connect(DB)


# =========================
# INIT
# =========================
def init_db():

    c = conn()
    cur = c.cursor()


    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        messages INTEGER DEFAULT 0,
        bond INTEGER DEFAULT 0,
        warnings INTEGER DEFAULT 0,
        role TEXT DEFAULT 'user'
    )
    """)


    # MEMORY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        text TEXT,
        reply TEXT
    )
    """)


    # LOGS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        text TEXT,
        reply TEXT
    )
    """)


    # SYSTEM
    cur.execute("""
    CREATE TABLE IF NOT EXISTS system (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    c.commit()
    c.close()


# =========================
# USERS
# =========================
def add_user(user_id):

    c = conn()
    cur = c.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users (user_id)
    VALUES (?)
    """, (str(user_id),))

    c.commit()
    c.close()


def get_user(user_id):

    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT * FROM users
    WHERE user_id=?
    """, (str(user_id),))

    row = cur.fetchone()

    c.close()

    return row


def update_user(user_id, field, value):

    c = conn()
    cur = c.cursor()

    cur.execute(f"""
    UPDATE users
    SET {field}=?
    WHERE user_id=?
    """, (value, str(user_id)))

    c.commit()
    c.close()


# =========================
# MEMORY
# =========================
def add_memory(user_id, text, reply):

    c = conn()
    cur = c.cursor()

    cur.execute("""
    INSERT INTO memory (user_id, text, reply)
    VALUES (?, ?, ?)
    """, (str(user_id), text, reply))

    # limit memory
    cur.execute("""
    DELETE FROM memory
    WHERE id NOT IN (
        SELECT id FROM memory
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 25
    )
    AND user_id=?
    """, (str(user_id), str(user_id)))

    c.commit()
    c.close()


def get_memory(user_id, limit=5):

    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT text, reply
    FROM memory
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT ?
    """, (str(user_id), limit))

    rows = cur.fetchall()

    c.close()

    return [
        {
            "text": r[0],
            "reply": r[1]
        }
        for r in rows
    ]


# =========================
# LOGS
# =========================
def add_log(user_id, text, reply):

    c = conn()
    cur = c.cursor()

    cur.execute("""
    INSERT INTO logs (user_id, text, reply)
    VALUES (?, ?, ?)
    """, (str(user_id), text, reply))

    # global log limit
    cur.execute("""
    DELETE FROM logs
    WHERE id NOT IN (
        SELECT id FROM logs
        ORDER BY id DESC
        LIMIT 300
    )
    """)

    c.commit()
    c.close()


def get_logs(limit=20):

    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT user_id, text, reply
    FROM logs
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()

    c.close()

    return rows


# =========================
# WARNINGS
# =========================
def add_warning(user_id):

    user = get_user(user_id)

    if not user:
        add_user(user_id)
        user = get_user(user_id)

    warnings = user[3] + 1

    update_user(user_id, "warnings", warnings)

    return warnings


# =========================
# ROLES
# =========================
def set_role(user_id, role):

    update_user(user_id, "role", role)


def get_role(user_id):

    user = get_user(user_id)

    if not user:
        return "user"

    return user[4]
