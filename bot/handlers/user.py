# bot/handlers/user.py

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder



router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Поиск", callback_data="start_search")
    builder.button(text="Категории", callback_data="show_categories")
    builder.button(text="Регионы", callback_data="show_regions")
    builder.adjust(2)

    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>!\n"
        f"Я помогу тебе найти товар по названию, категории или региону.",
        reply_markup=builder.as_markup()
    )


@router.callback_query(lambda c: c.data == "start_search")
async def callback_search(call: types.CallbackQuery):
    await call.message.answer("Введите запрос для поиска:")


@router.callback_query(lambda c: c.data == "show_categories")
async def callback_categories(call: types.CallbackQuery):
    await call.message.answer("/категории")


@router.callback_query(lambda c: c.data == "show_regions")
async def callback_regions(call: types.CallbackQuery):
    await call.message.answer("/регионы")
