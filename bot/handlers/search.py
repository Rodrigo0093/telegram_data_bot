from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.db_utils import get_all_categories, get_all_regions, search_items


router = Router()


@router.message(Command("поиск"))
async def start_search(message: types.Message):
    await message.answer("Введите запрос для поиска (наименование или артикул):")


@router.message(F.text.len() > 2)
async def handle_search_query(message: types.Message):
    query = message.text.strip()
    results = search_items(query=query, limit=5)

    if not results:
        await message.answer("Ничего не найдено.")
        return

    text = "\n\n".join(
        [f"<b>{r.product_name}</b>\nЦена: {r.price}₽\nГород: {r.region.city}" for r in results]
    )

    await message.answer(text)
