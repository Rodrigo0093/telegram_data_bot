# bot/handlers/filters.py
# Обработчики фильтрации товаров по регионам, городам и категориям
# Полная логика дублирует монолитный bot.py, включая формат ответов и навигацию

import logging
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline import get_back_main_keyboard, get_products_keyboard

from bot.utils.db_utils import (
    get_all_regions,
    get_cities_for_region,
    get_categories_for_region_city,
    get_products_by_filter,
    is_admin
)

router = Router()
logger = logging.getLogger(__name__)

# Вспомогательная функция форматирования товара по образцу монолита
def format_product(product, show_bs=False):
    """
    Форматирует объект SaleData в текст:
    БС№ (если админ), Наименование, Категория, Город, Регион, Цена, Артикул
    """
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

# Этап 1: выбор региона
@router.callback_query(lambda c: c.data == "menu_filter")
async def start_filter(callback: types.CallbackQuery):
    await callback.answer()
    logger.info(f"[filters] Пользователь {callback.from_user.id} начал фильтрацию")
    regions = get_all_regions()
    builder = InlineKeyboardBuilder()
    for r in regions:
        builder.button(text=r, callback_data=f"filter_region:{r}")
    builder.button(text="🏠 Главное меню", callback_data="nav_home")
    builder.adjust(2)
    await callback.message.edit_text("🌍 Выберите регион:", reply_markup=builder.as_markup())

# Этап 2: выбор города
@router.callback_query(lambda c: c.data.startswith("filter_region:"))
async def filter_region(callback: types.CallbackQuery):
    await callback.answer()
    region = callback.data.split(":",1)[1]
    logger.info(f"[filters] Пользователь выбрал регион: {region}")
    cities = get_cities_for_region(region)
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.button(text=city, callback_data=f"filter_city:{region}:{city}")
    builder.button(text="⬅️ Назад", callback_data="menu_filter")
    builder.button(text="🏠 Главное меню", callback_data="nav_home")
    builder.adjust(2)
    await callback.message.edit_text(
        f"🏙️ Выберите город в регионе <b>{region}</b>:",
        reply_markup=builder.as_markup()
    )

# Этап 3: выбор категории
@router.callback_query(lambda c: c.data.startswith("filter_city:"))
async def filter_city(callback: types.CallbackQuery):
    await callback.answer()
    _, region, city = callback.data.split(":",2)
    logger.info(f"[filters] Пользователь выбрал город: {city} (регион: {region})")
    categories = get_categories_for_region_city(region, city)
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=cat, callback_data=f"filter_category:{region}:{city}:{cat}")
    builder.button(text="⬅️ Назад", callback_data=f"filter_region:{region}")
    builder.button(text="🏠 Главное меню", callback_data="nav_home")
    builder.adjust(2)
    await callback.message.edit_text(
        f"📦 Выберите категорию в городе <b>{city}</b> (регион: <b>{region}</b>):",
        reply_markup=builder.as_markup()
    )

# Этап 4: вывод товаров по фильтру
@router.callback_query(lambda c: c.data.startswith("filter_category:"))
async def filter_category(callback: types.CallbackQuery):
    await callback.answer()
    _, region, city, category = callback.data.split(":",3)
    logger.info(f"[filters] Пользователь выбрал категорию: {category} в {city}, {region}")
    products = get_products_by_filter(region=region, city=city, category=category, limit=5, offset=0)
    if not products:
        await callback.message.edit_text(
            f"❌ Товары не найдены по фильтру: <b>{category}</b> в <b>{city}, {region}</b>",
            reply_markup=get_back_main_keyboard()
        )
        return
    show_bs = is_admin(callback.from_user.id)
    text = "\n\n".join([f"🔹 {format_product(p, show_bs)}" for p in products])
    builder = get_products_keyboard(
        filter_type="filter",
        filter_value=f"{region}|{city}|{category}",
        offset=5,
        limit=5
    )
    await callback.message.edit_text(
        f"⚙️ Результаты по фильтру <b>{category}</b> в <b>{city}, {region}</b>:\n\n{text}",
        reply_markup=builder
    )

# Этап 5: пагинация фильтра
@router.callback_query(lambda c: c.data.startswith("filter_next:"))
async def filter_next(callback: types.CallbackQuery):
    await callback.answer()
    _, region, city, category, offset = callback.data.split(":",4)
    offset = int(offset)
    logger.info(f"[filters] Пользователь листает фильтр {category} в {city}, {region}, offset={offset}")
    products = get_products_by_filter(region=region, city=city, category=category, limit=5, offset=offset)
    if not products:
        await callback.answer("📭 Больше товаров не найдено.", show_alert=True)
        return
    show_bs = is_admin(callback.from_user.id)
    text = "\n\n".join([f"🔹 {format_product(p, show_bs)}" for p in products])
    builder = get_products_keyboard(
        filter_type="filter",
        filter_value=f"{region}|{city}|{category}",
        offset=offset+5,
        limit=5
    )
    await callback.message.edit_text(
        f"⚙️ Продолжение по фильтру <b>{category}</b> в <b>{city}, {region}</b>:\n\n{text}",
        reply_markup=builder
    )
