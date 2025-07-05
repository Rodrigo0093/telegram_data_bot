# bot/handlers/search.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.inline import get_back_main_keyboard
from bot.utils.db_utils import search_items

router = Router()

# Обработка команды /search
@router.message(Command(commands=["search"]))
async def cmd_search(message: Message):
    await message.answer("Введите запрос в формате: Поиск: <слово>")

# Обработка сообщения, начинающегося с "Поиск:"
@router.message(lambda msg: msg.text and msg.text.startswith("Поиск:"))
async def handle_search_query(message: Message):
    query = message.text[7:].strip()  # Удаляем "Поиск:" и пробелы
    results = search_items(query)

    if not results:
        await message.answer("❌ Ничего не найдено по запросу.", reply_markup=get_back_main_keyboard())
        return

    response = "\n".join([
        f"<b>{item.product_name}</b> — {item.price} ₽ — {item.region.region} ({item.region.city})"
        for item in results[:5]
    ])
    await message.answer(response, reply_markup=get_back_main_keyboard())
