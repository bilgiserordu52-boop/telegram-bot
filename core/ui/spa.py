from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def build_ui(title, buttons):
    keyboard = []

    for row in buttons:
        keyboard.append([
            InlineKeyboardButton(b["text"], callback_data=b["data"])
            for b in row
        ])

    return title, InlineKeyboardMarkup(keyboard)
