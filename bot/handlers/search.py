# bot/handlers/search.py
# Обработчики поиска товаров по наименованию и артикулу
# Формат ответа, пагинация и навигация дублируют монолитный bot.py

import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from bot.utils.db_utils import search_items, is_admin
from bot.keyboards.inline import get_back_main_keyboard, get_products_keyboard

router = Router()
logger = logging.getLogger(__name__)

# Вспомогательная функция форматирования товара
def format_product(product, show_bs=False):
    parts = []
    if show_bs:
        parts.append(f"БС№: {product.bs_number}")
    parts.extend([
        f"Наименование: {product.product_name}",
        f"Категория: {product.category or '-'}",
        f"Город: {product.region.city}",
        f"Регион: {product.region.region}",
        f"Цена: {product.price:,.2f} ₽" if product.price is not None else "Цена: –",
        f"Артикул: {product.product_name.split()[0]}"
    ])
    return "\n".join(parts)

# Команда /search – начало поиска
@router.message(Command("search"))
async def cmd_search(message: types.Message):
    await message.answer("🔍 Введите наименование или артикул товара для поиска:")
    logger.info(f"[search] Пользователь {message.from_user.id} начал поиск")

# Обработка введённой строки – выполнение поиска
@router.message(lambda msg: msg.text and not msg.text.startswith("/"))
async def process_search_query(message: types.Message):
    query = message.text.strip()
    logger.info(f"[search] Пользователь {message.from_user.id} ищет: '{query}'")
    results = search_items(query)
    if not results:
        await message.answer("❌ Товары не найдены.", reply_markup=get_back_main_keyboard())
        return

    # Показываем первые 5
    page = results[:5]
    show_bs = is_admin(message.from_user.id)
    text = "\n\n".join([f"🔹 {format_product(p, show_bs)}" for p in page])

    kb = get_products_keyboard(
        filter_type="search",
        filter_value=query,
        offset=5,
        limit=5
    )
    await message.answer(
        f"🔎 Результаты поиска по запросу '<b>{query}</b>':\n\n{text}",
        reply_markup=kb
    )

# Пагинация результатов поиска
@router.callback_query(F.data.startswith("search_next:"))
async def search_next(callback: types.CallbackQuery):
    await callback.answer()
    _, query, offset = callback.data.split(":", 2)
    offset = int(offset)
    logger.info(f"[search] Пользователь {callback.from_user.id} листает результаты '{query}', offset={offset}")
    results = search_items(query)
    page = results[offset:offset+5]
    if not page:
        await callback.answer("📭 Больше товаров не найдено.", show_alert=True)
        return

    show_bs = is_admin(callback.from_user.id)
    text = "\n\n".join([f"🔹 {format_product(p, show_bs)}" for p in page])
    kb = get_products_keyboard(
        filter_type="search",
        filter_value=query,
        offset=offset+5,
        limit=5
    )
    await callback.message.edit_text(
        f"🔎 Продолжение по запросу '<b>{query}</b>':\n\n{text}",
        reply_markup=kb
    )
