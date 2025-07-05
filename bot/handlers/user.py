# bot/handlers/user.py
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.keyboards.inline import (
    get_main_keyboard,
    get_back_main_keyboard
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    try:
        await message.answer("👋 Добро пожаловать! Выберите действие:", reply_markup=get_main_keyboard())
        logger.info("Показано главное меню пользователю.")
    except Exception as e:
        logger.exception("Ошибка при показе главного меню")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data == "back")
async def handle_back(callback: CallbackQuery):
    try:
        await callback.message.edit_text("⬅ Вы вернулись назад.", reply_markup=get_main_keyboard())
        await callback.answer()
        logger.info("Переход назад выполнен.")
    except Exception as e:
        logger.exception("Ошибка при возврате назад")


@router.callback_query(F.data == "main_menu")
async def handle_main_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text("🏠 Главное меню:", reply_markup=get_main_keyboard())
        await callback.answer()
        logger.info("Возврат в главное меню.")
    except Exception as e:
        logger.exception("Ошибка при возврате в главное меню")
