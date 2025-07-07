from db.database import engine
from db.models import Base

def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы")

if __name__ == "__main__":
    init_db()