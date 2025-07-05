# main.py

import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from bot.utils.db_utils import import_data  # Функция импорта данных

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env
load_dotenv()


async def run_bot():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("❌ Не найден BOT_TOKEN в .env файле!")
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация всех роутеров из handlers
    from bot.handlers import routers
    for router in routers:
        dp.include_router(router)

    try:
        logger.info("▶ Бот запущен")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("⛔ Бот остановлен")


def update_database():
    logger.info("📥 Обновление данных в БД...")
    import_data()
    logger.info("✅ Данные успешно обновлены.")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == "update":
        update_database()
    elif command == "runbot":
        asyncio.run(run_bot())
    else:
        # По умолчанию: обновление данных + запуск бота
        update_database()
        asyncio.run(run_bot())
