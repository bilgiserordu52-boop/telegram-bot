import time
import uuid


# =========================
# NODE ID
# =========================
NODE_ID = str(uuid.uuid4())[:8]
START_TIME = time.time()


# =========================
# CLUSTER STATE
# =========================
CLUSTER = {
    "node_id": NODE_ID,
    "status": "online",
    "heartbeat": time.time(),
    "errors": 0,
    "recoveries": 0
}


# =========================
# HEARTBEAT
# =========================
def heartbeat():
    CLUSTER["heartbeat"] = time.time()


# =========================
# ERROR TRACK
# =========================
def register_error():
    CLUSTER["errors"] += 1


# =========================
# RECOVERY TRACK
# =========================
def recovery():
    CLUSTER["recoveries"] += 1


# =========================
# STATUS REPORT
# =========================
def cluster_status():
    return {
        "node_id": CLUSTER["node_id"],
        "status": CLUSTER["status"],
        "uptime": int(time.time() - START_TIME),
        "heartbeat": CLUSTER["heartbeat"],
        "errors": CLUSTER["errors"],
        "recoveries": CLUSTER["recoveries"]
    }
