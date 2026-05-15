from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def panel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Deploy", callback_data="deploy")],
        [InlineKeyboardButton("🧠 AI", callback_data="ai")],
        [InlineKeyboardButton("📊 Status", callback_data="status")]
    ])
