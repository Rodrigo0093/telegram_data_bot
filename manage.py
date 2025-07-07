# manage.py
# Скрипт для управления ботом: update и runbot команды
import sys
from db.database import init_db  # Импортируем функцию инициализации

if __name__ == "__main__":
    # Инициализация БД перед выполнением команд
    init_db()
    
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == "update":
        from main import update_database
        update_database()
    elif command == "runbot":
        from main import run_bot
        import asyncio
        asyncio.run(run_bot())
    else:
        from main import update_database, run_bot
        import asyncio
        update_database()
        asyncio.run(run_bot())


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == "update":
        # Импорт функции update_database из main
        from main import update_database
        update_database()
    elif command == "runbot":
        # Импорт функции run_bot из main
        from main import run_bot
        import asyncio
        asyncio.run(run_bot())
    else:
        # По умолчанию: обновление данных + запуск бота
        from main import update_database, run_bot
        import asyncio
        update_database()
        asyncio.run(run_bot())
