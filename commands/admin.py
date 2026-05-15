import config
from ui.keyboard import panel

def is_admin(user_id):
    return user_id == config.ADMIN_ID

async def admin_cmd(update, context):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("❌ no access")

    await update.message.reply_text("🛠 PANEL AKTİF", reply_markup=panel())
