import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect  # Добавлено для получения списка таблиц

# Настройки
POSTGRES_URL = "postgresql://postgres:2080klinTT@localhost:5432/telegram_bot_db" # Используем имя БД
SQLITE_URL = "sqlite:///./telegram_bot.db"

def migrate_postgres_to_sqlite():
    try:
        # 1. Подключение к PostgreSQL
        pg_engine = create_engine(POSTGRES_URL)
        
        # Получаем список всех таблиц в базе
        inspector = inspect(pg_engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("В базе нет таблиц для переноса!")
            return
            
        print(f"Найдены таблицы: {tables}")
        
        # 2. Подключение к SQLite
        sqlite_engine = create_engine(SQLITE_URL)
        
        # 3. Перенос данных
        for table in tables:
            try:
                # Чтение из PostgreSQL
                df = pd.read_sql_table(table, pg_engine)
                
                # Запись в SQLite
                df.to_sql(table, sqlite_engine, if_exists="replace", index=False)
                print(f"Таблица {table} перенесена ({len(df)} записей)")
                
            except Exception as e:
                print(f"Ошибка при переносе таблицы {table}: {str(e)}")
                continue
    
        # 4. Проверка
        print("\nПроверка данных в SQLite:")
        for table in tables:
            try:
                test_df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", sqlite_engine)
                print(f"{table}: {test_df.columns.tolist()}")
            except:
                print(f"Не удалось проверить таблицу {table}")

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")

if __name__ == "__main__":
    migrate_postgres_to_sqlite()