# bot/handlers/filters.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.db_utils import get_all_categories, get_all_regions
from bot.keyboards.inline import get_main_keyboard, get_back_main_keyboard


router = Router()


@router.message(Command("категории"))
async def list_categories(message: types.Message):
    categories = get_all_categories()
    if not categories:
        await message.answer("Категории не найдены.")
        return

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category, callback_data=f"category:{category}")
    builder.adjust(2)

    await message.answer("Выберите категорию:", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("category:"))
async def handle_category(callback: types.CallbackQuery):
    category = callback.data.split(":", 1)[1]
    await callback.message.edit_text(
        f"Вы выбрали категорию: <b>{category}</b>",
        reply_markup=get_back_main_keyboard()
    )


@router.message(Command("регионы"))
async def list_regions(message: types.Message):
    regions = get_all_regions()
    if not regions:
        await message.answer("Регионы не найдены.")
        return

    builder = InlineKeyboardBuilder()
    for region in regions:
        builder.button(text=region, callback_data=f"region:{region}")
    builder.adjust(2)

    await message.answer("Выберите регион:", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("region:"))
async def handle_region(callback: types.CallbackQuery):
    region = callback.data.split(":", 1)[1]
    await callback.message.edit_text(
        f"Вы выбрали регион: <b>{region}</b>",
        reply_markup=get_back_main_keyboard()
    )
