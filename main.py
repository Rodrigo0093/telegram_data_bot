# main.py
# Точка входа: импорт данных и запуск Telegram-бота с регистрацией роутеров и логированием

import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# Импортируем import_data из модуля importer
from importer.import_data import import_data  # Функция импорта данных в БД
from bot.handlers import routers  # Список роутеров: filters, search, user

# Настройка логирования: INFO-уровень и формат сообщений
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env
load_dotenv()


async def run_bot():
    """
    Основная функция запуска бота: инициализация и регистрация роутеров.
    """
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("❌ Не найден BOT_TOKEN в .env файле!")
        return

    # Инициализация бота с HTML-парсингом
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    # Используем память для состояний (при необходимости можно заменить на Redis)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация всех роутеров из папки handlers
    for router in routers:
        dp.include_router(router)
        logger.debug(f"Роутер зарегистрирован: {router}")

    try:
        logger.info("▶ Бот запущен и начинает polling...")
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию бота при остановке
        await bot.session.close()
        logger.info("⛔ Бот остановлен")


def update_database():
    """
    Обновление данных в базе данных: импорт из исходных файлов.
    """
    logger.info("📥 Начало обновления данных в БД...")
    import_data()
    logger.info("✅ Данные успешно обновлены.")


if __name__ == "__main__":
    # Чтение аргумента командной строки (update/runbot)
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == "update":
        update_database()
    elif command == "runbot":
        asyncio.run(run_bot())
    else:
        # По умолчанию: обновление данных + запуск бота
        update_database()
        asyncio.run(run_bot())
