import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from db.models import Base  # Импорт моделей

# Загрузка .env
load_dotenv()

# Получение строки подключения из переменной окружения
DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
