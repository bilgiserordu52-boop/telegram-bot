from core.platform.events import on

AUDIT_LOGS = []


# =========================
# AUDIT LOGGER
# =========================
def audit_logger(data):

    if not data:
        return

    AUDIT_LOGS.append(data)

    # limit logs
    if len(AUDIT_LOGS) > 200:
        del AUDIT_LOGS[0]


# =========================
# GET AUDITS
# =========================
def get_audits(limit=20):

    return AUDIT_LOGS[-limit:]


# =========================
# REGISTER EVENTS
# =========================
on("user_message", audit_logger)

on("admin_action", audit_logger)

on("security_alert", audit_logger)

on("ai_response", audit_logger)
