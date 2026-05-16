from telegram import ReplyKeyboardMarkup


# =========================
# ANA MENÜ
# =========================
def home():
    return ReplyKeyboardMarkup(
        [
            ["👤 Profil", "📊 Durum"],
            ["⚙️ Ayarlar", "❓ Yardım"],
            ["🚪 Çıkış"]
        ],
        resize_keyboard=True
    )


# =========================
# PROFİL MENÜ
# =========================
def profile_menu():
    return ReplyKeyboardMarkup(
        [
            ["📄 Bilgiler", "📊 İstatistik"],
            ["🔙 Geri"]
        ],
        resize_keyboard=True
    )


# =========================
# DURUM MENÜ
# =========================
def status_menu():
    return ReplyKeyboardMarkup(
        [
            ["🚀 Sistem", "📡 Sunucu"],
            ["🔙 Geri"]
        ],
        resize_keyboard=True
    )


# =========================
# AYARLAR MENÜ
# =========================
def settings_menu():
    return ReplyKeyboardMarkup(
        [
            ["🔐 Güvenlik", "🎨 Arayüz"],
            ["🔙 Geri"]
        ],
        resize_keyboard=True
    )


# =========================
# YARDIM MENÜ
# =========================
def help_menu():
    return ReplyKeyboardMarkup(
        [
            ["📖 Komutlar", "💬 Destek"],
            ["🔙 Geri"]
        ],
        resize_keyboard=True
    )
