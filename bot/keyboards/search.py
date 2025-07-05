# bot/handlers/search.py
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.inline import get_back_main_keyboard, get_main_keyboard
from bot.utils.db_utils import search_items

router = Router()
logger = logging.getLogger(__name__)

# 🔹 Состояния FSM для поиска
class SearchStates(StatesGroup):
    waiting_for_query = State()


# 🔹 Обработка кнопки "Поиск"
@router.callback_query(F.data == "start_search")
async def start_search(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_query)
    await callback.message.edit_text("Введите запрос для поиска:", reply_markup=get_back_main_keyboard())
    await callback.answer()
    logger.info("Ожидание ввода поискового запроса.")


# 🔹 Обработка ввода текста (поискового запроса)
@router.message(SearchStates.waiting_for_query)
async def process_search_query(message: Message, state: FSMContext):
    query = message.text.strip()
    if not query:
        await message.answer("⚠ Введите непустой запрос.", reply_markup=get_back_main_keyboard())
        return

    try:
        results = search_items(query)
        if not results:
            await message.answer("❌ Ничего не найдено.", reply_markup=get_back_main_keyboard())
            logger.info(f"По запросу '{query}' ничего не найдено.")
        else:
            text = "🔍 Результаты поиска:\n\n"
            text += "\n".join(f"{item.name} — {item.price}₽ ({item.city})" for item in results[:10])
            await message.answer(text, reply_markup=get_back_main_keyboard())
            logger.info(f"Найдено {len(results)} результатов по запросу '{query}'.")

    except Exception as e:
        logger.exception("Ошибка при поиске товаров")
        await message.answer("❌ Ошибка при поиске.", reply_markup=get_main_keyboard())

    await state.clear()
