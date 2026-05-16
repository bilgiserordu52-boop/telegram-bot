from core.admin.panel import admin_panel
from core.admin.rbac import is_admin

from core.monitor.system import health_report
from core.db import get_logs


async def handle_admin(update, render):

    user_id = update.effective_user.id


    # =========================
    # ADMIN CHECK
    # =========================
    if not is_admin(user_id):

        await render(update, "⛔ Yetkin yok")
        return


    data = update.callback_query.data


    # =========================
    # MAIN PANEL
    # =========================
    if data == "admin":

        text, kb = admin_panel()

        await render(update, text, kb)
        return


    # =========================
    # SYSTEM MONITOR
    # =========================
    if data == "admin_system":

        report = health_report()

        await render(update, report)

        return


    # =========================
    # LOGS
    # =========================
    if data == "admin_logs":

        logs = get_logs(10)

        if not logs:
            await render(update, "📭 Log yok")
            return

        text = "📜 LAST LOGS\n\n"

        for log in logs:

            user = log[0]
            msg = log[1]
            reply = log[2]

            text += (
                f"👤 {user}\n"
                f"💬 {msg}\n"
                f"🤖 {reply}\n\n"
            )

        await render(update, text)

        return


    # =========================
    # EXIT
    # =========================
    if data == "admin_exit":

        await render(update, "👋 Panel kapandı")

        return
