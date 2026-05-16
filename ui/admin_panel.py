# ui/admin_panel.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.runtime import uptime


# =========================
# ADMIN MAIN PANEL
# =========================
def admin_main():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Status", callback_data="admin_status"),
            InlineKeyboardButton("🚀 Deploy", callback_data="admin_deploy")
        ],
        [
            InlineKeyboardButton("🤖 AI Review", callback_data="admin_ai"),
            InlineKeyboardButton("📜 Logs", callback_data="admin_logs")
        ],
        [
            InlineKeyboardButton("👥 Users", callback_data="admin_users"),
            InlineKeyboardButton("⚙️ System", callback_data="admin_system")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back_home")
        ]
    ])


# =========================
# ADMIN DATA BUILDERS
# =========================
def admin_status_text():
    return f"""
📊 SYSTEM STATUS

⏱ Uptime: {uptime()}
🔥 Bot: ACTIVE
⚡ Mode: CLEAN ARCH
"""


def admin_deploy_text(result=""):
    return f"""
🚀 DEPLOY PANEL

Last result:
{result}
"""


def admin_logs_text():
    return "📜 LOG SYSTEM READY"


def admin_users_text():
    return "👥 USER SYSTEM READY"


def admin_system_text():
    return """
⚙️ SYSTEM INFO

✔ Router: ACTIVE
✔ UI: CLEAN
✔ Deploy: SEPARATED
"""
