# bot/keyboards/inline.py

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# Главное меню с кнопками: Поиск и Категории
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Поиск", callback_data="start_search")
    builder.button(text="📂 Категории", callback_data="show_filters")
    builder.adjust(2)
    return builder.as_markup()

# Кнопка "Назад" к главному меню
def get_back_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="back_to_main")
    return builder.as_markup()
