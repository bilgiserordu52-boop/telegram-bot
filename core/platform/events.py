EVENTS = {}


# =========================
# REGISTER
# =========================
def on(event_name, callback):

    if event_name not in EVENTS:
        EVENTS[event_name] = []

    EVENTS[event_name].append(callback)


# =========================
# EMIT
# =========================
def emit(event_name, data=None):

    listeners = EVENTS.get(event_name, [])

    for callback in listeners:

        try:
            callback(data)

        except Exception as e:
            print(f"[EVENT ERROR] {event_name}: {e}")
