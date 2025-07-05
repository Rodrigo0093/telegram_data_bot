# bot/handlers/filters.py
import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    get_back_main_keyboard,
    get_main_keyboard,
    get_cancel_keyboard,
)
from bot.utils.db_utils import get_all_categories

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "show_filters")
async def show_filters(callback: CallbackQuery):
    try:
        categories = get_all_categories()
        if not categories:
            await callback.message.answer("⚠ Категории не найдены.", reply_markup=get_back_main_keyboard())
            logger.warning("Категории не найдены в базе данных.")
            return

        text = "📂 Доступные категории:\n\n"
        text += "\n".join(f"🔸 {cat}" for cat in categories)
        await callback.message.edit_text(text, reply_markup=get_back_main_keyboard())
        await callback.answer()
        logger.info("Показаны категории.")

    except Exception as e:
        logger.exception("Ошибка при отображении категорий")
        await callback.message.answer("❌ Не удалось получить категории.", reply_markup=get_main_keyboard())
        await callback.answer()
