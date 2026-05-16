from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def admin_panel():

    text = """
👑 ADMIN CONTROL CENTER

🛡 Security aktif
🤖 AI sistemi aktif
📡 Monitoring aktif
"""

    kb = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📊 SYSTEM",
                callback_data="admin_system"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 LOGS",
                callback_data="admin_logs"
            )
        ],

        [
            InlineKeyboardButton(
                "🚪 EXIT",
                callback_data="admin_exit"
            )
        ]

    ])

    return text, kb
