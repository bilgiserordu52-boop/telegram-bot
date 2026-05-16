from flask import Flask, send_from_directory
import sqlite3
import time

import config

from core.platform.realtime import socketio
from core.ai.memory_graph import MEMORY_GRAPH
from core.ai.evolution_core import evolution_status
from core.ai.brain import USER_STATE
from core.monitor.system import health_report


DB = "bot.db"

dashboard = Flask(__name__)
socketio.init_app(dashboard)


# =========================
# DB
# =========================
def conn():
    return sqlite3.connect(DB)


# =========================
# STYLE (VISUAL UPGRADE)
# =========================
STYLE = """
<style>

@keyframes bgshift {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

body{
    background: linear-gradient(-45deg, #05070d, #0b1020, #070a12, #0a0f18);
    background-size: 400% 400%;
    animation: bgshift 15s ease infinite;
    color:#e6e6e6;
    font-family:Arial;
    padding:25px;
}

/* MAIN CARD */
.card{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding:20px;
    border-radius:18px;
    margin-bottom:18px;
    box-shadow: 0 0 25px rgba(0,0,0,0.6);
    transition: 0.3s;
}

.card:hover{
    transform: scale(1.01);
    border:1px solid rgba(124,196,255,0.35);
}

/* TITLE */
.title{
    font-size:22px;
    font-weight:bold;
    color:#7cc4ff;
    margin-bottom:10px;
}

/* LIVE PULSE */
.pulse{
    width:10px;
    height:10px;
    background:#00ff88;
    border-radius:50%;
    display:inline-block;
    margin-right:6px;
    box-shadow:0 0 15px #00ff88;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {transform:scale(1); opacity:1;}
    50% {transform:scale(1.6); opacity:0.6;}
    100% {transform:scale(1); opacity:1;}
}

/* BARS */
.bar {
    height:6px;
    background:#111;
    border-radius:10px;
    overflow:hidden;
    margin-top:5px;
}

.bar-fill {
    height:100%;
    background:#7cc4ff;
    width:60%;
}

/* LOG */
.log{
    background: rgba(0,0,0,0.35);
    padding:10px;
    border-radius:12px;
    margin-top:8px;
}

/* LINKS */
a{
    color:#7cc4ff;
    text-decoration:none;
}

</style>
"""


# =========================
# STATIC
# =========================
@dashboard.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("ui/static", path)


# =========================
# HOME
# =========================
@dashboard.route("/")
def home():

    report = health_report()
    evo = evolution_status()

    return f"""
    {STYLE}

    <div style="text-align:center;margin-bottom:20px;">
        <img src="/static/logo.png" width="95"
        style="border-radius:50%;box-shadow:0 0 30px #7cc4ff;">
    </div>

    <div class='card'>
        <div class='title'>{config.BOT_NAME}</div>
        <div style="opacity:0.7;font-size:13px;">
            {config.BOT_TAGLINE} • {config.BOT_VERSION}
        </div>
    </div>

    <div class='card'>
        <div class='title'>SYSTEM CORE STATUS</div>
        <pre>{report}</pre>
    </div>

    <div class='card'>
        <div class='title'>AI STATE</div>

        🧠 Level: {evo['level']}<br>
        ⚡ XP: {evo['xp']}<br>
        🔥 Adapt: {evo['adaptation']}<br>

        <div class="bar"><div class="bar-fill"></div></div>
    </div>

    <div class='card'>
        <div class='title'><span class="pulse"></span>LIVE AI STREAM</div>
        <div id="live"></div>
    </div>

    <div class='card'>
        <div class='title'>NAVIGATION</div>
        <span class="pulse"></span><a href='/users'>Users</a><br>
        <span class="pulse"></span><a href='/logs'>Logs</a><br>
        <span class="pulse"></span><a href='/brain'>Brain</a><br>
        <span class="pulse"></span><a href='/memory'>Memory</a><br>
        <span class="pulse"></span><a href='/evolution'>Evolution</a>
    </div>

    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <script src="/static/socket.js"></script>
    """


# =========================
# USERS
# =========================
@dashboard.route("/users")
def users():

    c = conn()
    cur = c.cursor()
    cur.execute("SELECT user_id, messages, bond, warnings, role FROM users")
    rows = cur.fetchall()
    c.close()

    html = f"{STYLE}<div class='card'><div class='title'>USERS</div>"

    for r in rows:
        html += f"""
        <div class='log'>
        👤 {r[0]}<br>
        💬 {r[1]}<br>
        ❤️ {r[2]}<br>
        ⚠ {r[3]}<br>
        👑 {r[4]}
        </div>
        """

    return html + "</div>"


# =========================
# LOGS
# =========================
@dashboard.route("/logs")
def logs():

    c = conn()
    cur = c.cursor()
    cur.execute("SELECT user_id, text, reply FROM logs ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    c.close()

    html = f"{STYLE}<div class='card'><div class='title'>LOGS</div>"

    for r in rows:
        html += f"""
        <div class='log'>
        👤 {r[0]}<br>
        💬 {r[1]}<br>
        🤖 {r[2]}
        </div>
        """

    return html + "</div>"


# =========================
# BRAIN
# =========================
@dashboard.route("/brain")
def brain():

    html = f"{STYLE}<div class='card'><div class='title'>BRAIN</div>"

    for uid, state in USER_STATE.items():

        html += f"""
        <div class='log'>
        👤 {uid}<br>
        🧠 {state['mood']}<br>
        ❤️ {state['bond']}<br>
        ⚡ {state['energy']}<br>
        🎯 {state['last_intent']}
        </div>
        """

    return html + "</div>"


# =========================
# MEMORY
# =========================
@dashboard.route("/memory")
def memory():

    html = f"{STYLE}<div class='card'><div class='title'>MEMORY</div>"

    for uid, data in MEMORY_GRAPH.items():

        html += f"""
        <div class='log'>
        👤 {uid}<br>
        ❤️ {data['emotion_score']}<br>
        🔥 {data['interaction_count']}<br>
        🧠 {list(data['topics'].keys())[:8]}
        </div>
        """

    return html + "</div>"


# =========================
# EVOLUTION
# =========================
@dashboard.route("/evolution")
def evolution():

    evo = evolution_status()

    return f"""
    {STYLE}

    <div class='card'>
        <div class='title'>EVOLUTION CORE</div>

        🧠 Level: {evo['level']}<br>
        ⚡ XP: {evo['xp']}<br>
        🔥 Adaptation: {evo['adaptation']}<br>
        🎭 Mood: {evo['mood_shift']}
    </div>
    """


# =========================
# START
# =========================
def start_dashboard():

    socketio.run(
        dashboard,
        host="0.0.0.0",
        port=5000
    )
