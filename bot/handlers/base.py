# bot/handlers/base.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards.main import get_main_menu_keyboard

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Привет! 👋\nЯ помогу найти товары по названию или артикулу.",
        reply_markup=get_main_menu_keyboard()
    )

@router.callback_query(F.data == "search")
async def process_search(callback: CallbackQuery):
    await callback.message.answer("🔍 Введите название или артикул товара:")
    await callback.answer()  # чтобы убрать индикатор загрузки Telegram

@router.callback_query(F.data == "categories")
async def process_categories(callback: CallbackQuery):
    await callback.message.answer("📂 Выберите категорию:")
    await callback.answer()
