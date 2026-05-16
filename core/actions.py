from core.ui.keyboard import home, profile_menu, status_menu, settings_menu, help_menu
from core.auth import logout_admin


# =========================
# UI ENGINE (REAL APP MODE)
# =========================
async def render(update, text, keyboard=None):
    """
    TEK MESAJ UI ENGINE:
    - edit varsa edit eder
    - yoksa reply atar
    """
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
        else:
            await update.message.edit_text(text, reply_markup=keyboard)
    except:
        await update.message.reply_text(text, reply_markup=keyboard)


# =========================
# MAIN PAGES
# =========================
async def home_page(update):
    await render(update, "🏠 ANA MENÜ", home())


async def profile_page(update):
    await render(update, "👤 PROFİL", profile_menu())


async def status_page(update):
    await render(update, "📊 DURUM", status_menu())


async def settings_page(update):
    await render(update, "⚙️ AYARLAR", settings_menu())


async def help_page(update):
    await render(update, "❓ YARDIM", help_menu())


# =========================
# SUB PAGES
# =========================
async def profile_info(update):
    await render(update, "👤 Kullanıcı bilgileri")


async def profile_stats(update):
    await render(update, "📊 İstatistikler")


async def system_status(update):
    await render(update, "🚀 Sistem aktif")


async def server_status(update):
    await render(update, "📡 Sunucu aktif")


async def security_settings(update):
    await render(update, "🔐 Güvenlik ayarları")


async def ui_settings(update):
    await render(update, "🎨 UI ayarları")


async def help_commands(update):
    await render(update, "/start /login /logout")


async def help_support(update):
    await render(update, "Destek sistemi aktif")


async def do_logout(update):
    logout_admin(update.effective_user.id)
    await render(update, "🚪 Çıkış yapıldı", home())
