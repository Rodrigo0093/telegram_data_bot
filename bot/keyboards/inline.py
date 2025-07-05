# bot/keyboards/inline.py

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# 🔹 Главное меню
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Поиск", callback_data="search")  # <--- исправлено
    builder.button(text="📂 Категории", callback_data="show_filters")
    builder.adjust(2)
    return builder.as_markup()



# 🔹 Клавиатура "Назад" + "Главное меню"
def get_back_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="back")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()


# 🔹 Только кнопка "Назад"
def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="back")
    return builder.as_markup()


# 🔹 Только кнопка "Главное меню"
def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    return builder.as_markup()


# 🔹 Кнопка "Отмена"
def get_cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data="cancel")
    return builder.as_markup()
