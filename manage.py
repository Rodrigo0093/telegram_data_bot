# manage.py

import click
import asyncio
import logging
from main import run_bot, update_database
from db.database import engine
from db.models import Base
from bot.utils.db_utils import import_data

# Логирование в файл
logging.basicConfig(
    filename="manage.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """📦 Утилита управления Telegram Data Bot"""
    pass


@cli.command()
def runbot():
    """🚀 Запуск Telegram-бота"""
    logger.info("▶ Запуск бота...")
    asyncio.run(run_bot())
    logger.info("⛔ Бот остановлен.")


@cli.command()
def updatedb():
    """📥 Обновление данных в БД (без сброса)"""
    logger.info("🔁 Обновление данных...")
    update_database()
    logger.info("✅ Данные обновлены.")


@cli.command()
def createdb():
    """📦 Только создание таблиц"""
    logger.info("📦 Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы.")
    logger.info("✅ Таблицы успешно созданы.")


@cli.command()
def resetdb():
    """🧨 Полный сброс БД: удаление, создание, импорт"""
    confirm = input("❗ Это удалит все данные. Продолжить? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Операция отменена.")
        return

    logger.warning("⚠ Выполняется сброс БД...")
    Base.metadata.drop_all(bind=engine)
    logger.info("🗑️ Таблицы удалены.")

    Base.metadata.create_all(bind=engine)
    logger.info("📦 Таблицы созданы.")

    import_data()
    logger.info("✅ Данные импортированы.")
    print("✅ Сброс базы данных завершён.")


@cli.command()
def testdb():
    """🧪 Проверка подключения к БД"""
    try:
        conn = engine.connect()
        conn.close()
        print("✅ Подключение к БД успешно.")
        logger.info("✅ Проверка БД прошла успешно.")
    except Exception as e:
        print("❌ Ошибка подключения к БД:", e)
        logger.error(f"❌ Ошибка подключения к БД: {e}")


if __name__ == "__main__":
    cli()
