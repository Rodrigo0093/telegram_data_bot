# bot/handlers/search.py
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.keyboards.inline import get_back_main_keyboard, get_main_keyboard
from bot.utils.db_utils import search_items

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "search")
async def ask_search_query(callback: CallbackQuery):
    try:
        await callback.message.edit_text("🔎 Введите запрос для поиска:", reply_markup=get_back_main_keyboard())
        await callback.answer()
        logger.info("Запрошен ввод поискового запроса.")
    except Exception as e:
        logger.exception("Ошибка при запросе поискового запроса")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.message()
async def process_search_query(message: Message):
    try:
        query = message.text.strip()
        if not query:
            await message.answer("⚠ Пустой запрос. Введите текст для поиска.")
            return

        results = search_items(query=query)

        if not results:
            await message.answer("❌ Ничего не найдено.", reply_markup=get_back_main_keyboard())
            return

        # Формируем ответ
        text_lines = [
            f"<b>{item.name}</b>\nЦена: {item.price} руб.\nГород: {item.city}"
            for item in results
        ]
        response = "\n\n".join(text_lines)

        await message.answer(response, reply_markup=get_back_main_keyboard())
        logger.info(f"Показаны результаты поиска по запросу: {query}")

    except Exception as e:
        logger.exception("Ошибка при обработке поискового запроса")
        await message.answer("❌ Произошла ошибка при поиске. Попробуйте позже.")


@router.callback_query(F.data == "main_menu")
async def handle_main_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text("🏠 Главное меню:", reply_markup=get_main_keyboard())
        await callback.answer()
        logger.info("Возврат в главное меню из поиска.")
    except Exception as e:
        logger.exception("Ошибка при возврате в главное меню")
