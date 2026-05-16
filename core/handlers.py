from core.ui.keyboard import home, profile_menu, status_menu, settings_menu, help_menu
from core.runtime import uptime
from core.auth import login_admin, logout_admin
from core.ui.builder import build_ui_text, build_keyboard
from core.features.engine import execute

# =========================
# MAIN ACTIONS
# =========================
async def open_home(update):
    await update.message.reply_text("🏠 ANA MENÜ", reply_markup=home())


async def open_profile(update):
    await update.message.reply_text("👤 PROFİL", reply_markup=profile_menu())


async def open_status(update):
    await update.message.reply_text("📊 DURUM", reply_markup=status_menu())


async def open_settings(update):
    await update.message.reply_text("⚙️ AYARLAR", reply_markup=settings_menu())


async def open_help(update):
    await update.message.reply_text("❓ YARDIM", reply_markup=help_menu())


# =========================
# SUB ACTIONS
# =========================
async def show_system(update):
    await update.message.reply_text("🚀 Sistem aktif")


async def show_server(update):
    await update.message.reply_text("📡 Sunucu aktif")


async def show_info(update):
    await update.message.reply_text("👤 Kullanıcı bilgileri")


async def show_stats(update):
    await update.message.reply_text("📊 İstatistikler")
