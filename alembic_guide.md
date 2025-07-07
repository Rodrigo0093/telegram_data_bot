"""
ALEMBIC MINI-GUIDE (SQLAlchemy migrations)

1. Установка:
pip install alembic psycopg2-binary  # для PostgreSQL

2. Базовая настройка:
"""
# В терминале выполните:
"""
alembic init migrations
"""

"""
3. Конфигурация (2 файла):
"""
# --- alembic.ini ---
"""
[alembic]
sqlalchemy.url = postgresql://user:password@localhost/db_name
"""

# --- migrations/env.py ---
"""
from db.models import Base  # импорт ваших моделей SQLAlchemy
target_metadata = Base.metadata
"""

"""
4. Основные команды:
"""
COMMANDS = {
    "Создать миграцию": "alembic revision --autogenerate -m 'описание изменений'",
    "Применить миграции": "alembic upgrade head",
    "Откатить последнюю": "alembic downgrade -1",
    "Показать историю": "alembic history",
    "Сбросить все таблицы": "alembic downgrade base && alembic upgrade head",
}

"""
5. Жизненный цикл миграции:
1. Измените модели SQLAlchemy
2. alembic revision --autogenerate -m "описание"
3. ПРОВЕРЬТЕ сгенерированный файл в migrations/versions/
4. alembic upgrade head
"""

"""
6. Решение проблем:
• Если autogenerate не видит изменения:
  - Убедитесь, что импорт моделей в env.py корректен
  - Проверьте, что модели наследуются от Base
  - Перезапустите терминал

• Ошибки подключения:
  - Проверьте sqlalchemy.url в alembic.ini
  - Убедитесь, что БД запущена
"""

if __name__ == "__main__":
    print("="*50)
    print("ALEMBIC QUICK GUIDE".center(50))
    print("="*50)
    for action, cmd in COMMANDS.items():
        print(f"\n★ {action}:")
        print(f"   {cmd}")
    print("\n⚠ Внимание: всегда проверяйте сгенерированные миграции перед применением!")