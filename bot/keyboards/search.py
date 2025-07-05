from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def categories_kb(categories: list[str]) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=cat, callback_data=f"category:{cat}")]
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def regions_kb(regions: list[str]) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=reg, callback_data=f"region:{reg}")]
        for reg in regions
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back_or_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="nav:back"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="nav:main")
        ]
    ])
