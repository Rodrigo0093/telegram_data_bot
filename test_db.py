from db.database import SessionLocal
from db.models import SaleData

db = SessionLocal()
categories = db.query(SaleData.category).distinct().all()
print("Категории в БД:", categories)
db.close()
