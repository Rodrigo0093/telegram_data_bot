from db.database import engine
from db.models import Base


# Создание всех таблиц из моделей
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы.")
