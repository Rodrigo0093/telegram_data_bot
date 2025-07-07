# bot/keyboards/inline.py
# Генерация inline-клавиатур: главное меню, навигация и пагинация

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.db_utils import is_admin
import logging

logger = logging.getLogger(__name__)

# Главное меню: Поиск и Фильтрация
def get_main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает главное меню с кнопками поиска и фильтрации и статусом пользователя.
    """
    builder = InlineKeyboardBuilder()
    # Добавляем кнопки
    builder.button(text="🔍 Поиск по наименованию", callback_data="menu_search")
    builder.button(text="⚙️ Фильтрация", callback_data="menu_filter")
    builder.adjust(2)

    # Текстовое сообщение формируется в handler'е, здесь только разметка
    logger.debug(f"[inline] Создана клавиатура главного меню для пользователя {user_id}")
    return builder.as_markup()

# Навигация назад и в начало
def get_back_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="nav_back")
    builder.button(text="🏠 Главное меню", callback_data="nav_home")
    builder.adjust(2)
    logger.debug("[inline] Создана клавиатура навигации назад и домой")
    return builder.as_markup()

# Кнопки для пагинации и навигации
def get_products_keyboard(filter_type: str, filter_value: str, offset: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    # Следующие
    builder.button(
        text="➡️ Следующие",
        callback_data=f"{filter_type}_next:{filter_value}:{offset}"
    )
    # Навигация
    builder.button(text="⬅️ Назад", callback_data="nav_back")
    builder.button(text="🏠 Главное меню", callback_data="nav_home")
    builder.adjust(1, 2)
    logger.debug(f"[inline] Создана клавиатура для фильтра {filter_type}={filter_value}, offset={offset}")
    return builder.as_markup()
