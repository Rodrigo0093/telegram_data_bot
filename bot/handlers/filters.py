from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.utils.db_utils import get_all_categories, get_all_regions, search_items
from bot.states.search_state import SearchState

router = Router()

# Тестовая команда для проверки
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🟢 Бот работает! Используйте /категории или /регионы")

@router.message(Command("категории"))
async def choose_category(message: types.Message):
    categories = get_all_categories()
    print("Категории из функции:", categories)

    if not categories:
        await message.answer("⚠️ Категории не найдены.")
        return

    buttons = [
        [InlineKeyboardButton(text=cat, callback_data=f"filter_category:{cat}")]
        for cat in categories
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("📂 Выберите категорию:", reply_markup=markup)

@router.message(Command("регионы"))
async def choose_region(message: types.Message):
    regions = get_all_regions()
    if not regions:
        await message.answer("⚠️ Регионы не найдены.")
        return

    buttons = [
        [InlineKeyboardButton(text=reg, callback_data=f"filter_region:{reg}")]
        for reg in regions
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("📍 Выберите регион:", reply_markup=markup)

@router.callback_query(F.data.startswith("filter_category:"))
async def filter_by_category(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split(":", 1)[1]
    await state.update_data(category=category, page=0)
    await state.set_state(SearchState.showing_results)
    await show_results(callback.message, state)
    await callback.answer()

@router.callback_query(F.data.startswith("filter_region:"))
async def filter_by_region(callback: types.CallbackQuery, state: FSMContext):
    region = callback.data.split(":", 1)[1]
    await state.update_data(region=region, page=0)
    await state.set_state(SearchState.showing_results)
    await show_results(callback.message, state)
    await callback.answer()

@router.message(Command("поиск"))
async def start_search(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(SearchState.waiting_for_query)
    await message.answer("🔎 Введите запрос для поиска (наименование или артикул):")

@router.message(SearchState.waiting_for_query, F.text.len() > 2)
async def handle_search_query(message: types.Message, state: FSMContext):
    query = message.text.strip()
    await state.update_data(query=query, page=0)
    await state.set_state(SearchState.showing_results)
    await show_results(message, state)

@router.callback_query(F.data == "next")
async def next_page(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["page"] += 1
    await state.update_data(page=data["page"])
    await show_results(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "prev")
async def prev_page(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["page"] = max(data["page"] - 1, 0)
    await state.update_data(page=data["page"])
    await show_results(callback.message, state)
    await callback.answer()

async def show_results(message: types.Message, state: FSMContext):
    data = await state.get_data()
    query = data.get("query", "")
    category = data.get("category")
    region = data.get("region")
    page = data.get("page", 0)

    limit = 5
    offset = page * limit
    results = search_items(query=query, category=category, region=region, limit=limit, offset=offset)

    if not results:
        await message.answer("Ничего не найдено.")
        return

    lines = []
    for r in results:
        lines.append(
            f"<b>{r.product_name}</b>\n"
            f"📦 Артикул: <code>{r.bs_number}</code>\n"
            f"💰 Цена: <b>{r.price}₽</b>\n"
            f"📍 Город: {r.region.city}\n"
        )
    text = "\n".join(lines)

    nav = InlineKeyboardBuilder()
    if page > 0:
        nav.button(text="⬅️ Назад", callback_data="prev")
    if len(results) == limit:
        nav.button(text="➡️ Далее", callback_data="next")

    await message.answer(text, reply_markup=nav.adjust(2).as_markup(), parse_mode="HTML")
