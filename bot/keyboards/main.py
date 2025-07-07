# bot/keyboards/main.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="🔍 Поиск", callback_data="search")],
        [InlineKeyboardButton(text="📂 По категориям", callback_data="categories")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
