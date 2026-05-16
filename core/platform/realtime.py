from flask_socketio import SocketIO

socketio = SocketIO(
    cors_allowed_origins="*"
)


# =========================
# LIVE EVENT
# =========================
def live_emit(event, data):

    try:

        socketio.emit(event, data)

    except Exception as e:

        print(f"[SOCKET ERROR] {e}")
