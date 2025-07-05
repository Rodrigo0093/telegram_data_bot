# bot/handlers/search.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.db_utils import search_items

router = Router()

# Обработка команды /поиск — приглашение к вводу запроса
@router.message(Command("поиск"))
async def start_search(message: types.Message):
    await message.answer("Введите запрос для поиска (наименование или артикул):")

# Обработка текста пользователя длиной более 2 символов
@router.message(F.text.len() > 2)
async def handle_search_query(message: types.Message):
    query = message.text.strip()

    # Поиск по базе (без фильтров)
    results = search_items(query=query, limit=5)

    if not results:
        await message.answer("Ничего не найдено.")
        return

    # Формирование ответа с результатами
    text = "\n\n".join(
        [f"<b>{r.product_name}</b>\nЦена: {r.price}₽\nГород: {r.region.city}" for r in results]
    )

    await message.answer(text)
