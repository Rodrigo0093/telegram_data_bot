import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()

async def main():
    # Проверка токена
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        logger.error("Не найден BOT_TOKEN в .env файле!")
        return

    try:
        # Инициализация бота
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Создаем диспетчер
        dp = Dispatcher(storage=MemoryStorage())
        
        # Подключаем хэндлеры
        from bot.handlers import commands
        dp.include_router(commands.router)
        
        # Тест БД перед запуском
        logger.info("Проверка подключения к БД...")
        from bot.utils import db_utils
        categories = db_utils.get_all_categories()
        regions = db_utils.get_all_regions()
        logger.info(f"Категории: {len(categories)}, Регионы: {len(regions)}")
        
        # Запуск бота
        logger.info("Бот запущен")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
    finally:
        if 'bot' in locals():
            await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())