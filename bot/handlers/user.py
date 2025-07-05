# bot/handlers/user.py
# Обработчик /start, menu_search и menu_filter

import logging
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_main_keyboard
from bot.utils.db_utils import is_allowed, is_admin
from bot.handlers.search import cmd_search
from bot.handlers.filters import start_filter

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def on_start(message: types.Message):
    user_id = message.from_user.id
    if not is_allowed(user_id):
        await message.reply("🚫 У вас нет доступа к этому боту.")
        logger.warning(f"[user] Доступ запрещён пользователю {user_id}")
        return
    text = "📊 Выберите действие:"
    if is_admin(user_id):
        text += "\n🛡️ Статус: Администратор"
    else:
        text += "\n👤 Статус: Пользователь"
    kb = get_main_keyboard(user_id)
    await message.answer(text, reply_markup=kb)
    logger.info(f"[user] Пользователь {user_id} запустил бота")

# Переход в поиск
@router.callback_query(lambda c: c.data == "menu_search")
async def on_menu_search(callback: CallbackQuery):
    await callback.answer()
    await cmd_search(callback.message)

# Переход в фильтрацию
@router.callback_query(lambda c: c.data == "menu_filter")
async def on_menu_filter(callback: CallbackQuery):
    await callback.answer()
    await start_filter(callback)
