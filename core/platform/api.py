from flask import Flask, jsonify

import threading
import sqlite3

from core.monitor.system import health_report

DB = "bot.db"

app = Flask(__name__)


# =========================
# CONNECTION
# =========================
def conn():
    return sqlite3.connect(DB)


# =========================
# HOME
# =========================
@app.route("/")
def home():

    return jsonify({
        "status": "online",
        "system": "AI PLATFORM CORE"
    })


# =========================
# HEALTH
# =========================
@app.route("/health")
def health():

    return jsonify({
        "report": health_report()
    })


# =========================
# USERS
# =========================
@app.route("/users")
def users():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT user_id, messages, bond, warnings, role
    FROM users
    """)

    rows = cur.fetchall()

    c.close()

    result = []

    for row in rows:

        result.append({
            "user_id": row[0],
            "messages": row[1],
            "bond": row[2],
            "warnings": row[3],
            "role": row[4]
        })

    return jsonify(result)


# =========================
# LOGS
# =========================
@app.route("/logs")
def logs():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    SELECT user_id, text, reply
    FROM logs
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cur.fetchall()

    c.close()

    result = []

    for row in rows:

        result.append({
            "user_id": row[0],
            "text": row[1],
            "reply": row[2]
        })

    return jsonify(result)


# =========================
# START API
# =========================
def start_api():

    t = threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=8080
        ),
        daemon=True
    )

    t.start()
