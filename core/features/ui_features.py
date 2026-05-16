from core.features.registry import register_feature


# =========================
# UI FEATURES WRAPPER
# =========================
def load_ui_features():

    async def home():
        return "🏠 ANA MENÜ"

    async def profile():
        return "👤 PROFİL"

    async def status():
        return "📊 DURUM"

    async def settings():
        return "⚙️ AYARLAR"

    async def help_menu():
        return "❓ YARDIM"

    async def system():
        return "🚀 Sistem aktif"

    async def server():
        return "📡 Sunucu aktif"

    async def info():
        return "👤 Kullanıcı bilgisi"

    async def stats():
        return "📊 İstatistikler"


    # REGISTER AS FEATURES
    register_feature("home", home)
    register_feature("profile", profile)
    register_feature("status", status)
    register_feature("settings", settings)
    register_feature("help", help_menu)
    register_feature("system", system)
    register_feature("server", server)
    register_feature("info", info)
    register_feature("stats", stats)
