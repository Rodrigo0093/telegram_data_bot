import pandas as pd
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal, engine
from db.models import Base, Store, Region, SaleData
from datetime import datetime

# Пути к Excel-файлам
DATA_PATH = "data/data.xlsx"
ADDRESS_PATH = "data/store_addresses.xlsx"
REGIONS_PATH = "data/city_regions.xlsx"

# Создаём таблицы, если не созданы
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Импорт регионов ---
print("Импорт регионов...")
regions_df = pd.read_excel(REGIONS_PATH).dropna(subset=["Город"])
for _, row in regions_df.iterrows():
    city = row["Город"].strip()
    region = row.get("Регион", "").strip()
    district = row.get("Округ", "").strip()

    existing = db.query(Region).filter_by(city=city).first()
    if not existing:
        db.add(Region(city=city, region=region, district=district))

db.commit()

# --- Импорт магазинов ---
print("Импорт магазинов...")
addresses_df = pd.read_excel(ADDRESS_PATH).dropna(subset=["Магазин"])
for _, row in addresses_df.iterrows():
    try:
        store_code = int(row["Магазин"])
    except:
        continue

    city = str(row.get("Город", "")).strip()
    address = str(row.get("Адрес", "")).strip()

    existing = db.query(Store).filter_by(store_code=store_code).first()
    if not existing:
        db.add(Store(store_code=store_code, city=city, address=address))

db.commit()

# --- Импорт основной таблицы ---
print("Импорт данных...")
data_df = pd.read_excel(DATA_PATH)

def safe_date(value):
    date = pd.to_datetime(value, errors='coerce', dayfirst=True)
    return None if pd.isna(date) else date

def safe_int(value):
    try:
        return int(value)
    except:
        return None

for _, row in data_df.iterrows():
    bs_number = str(row.get("БС№", "")).strip()
    if not bs_number:
        continue

    store_code = row.get("Код магазина")
    policy_type = str(row.get("Вид полиса", "")).strip()
    category = str(row.get("Категория", "")).strip()
    product_name = str(row.get("Наименование", "")).strip()
    price = row.get("Сумма")
    days_left = safe_int(row.get("Осталось дней"))

    sale_date = safe_date(row.get("Дата продажи"))
    start_date = safe_date(row.get("Дата начала"))
    end_date = safe_date(row.get("Дата окончания"))

    # Определим регион по городу (если есть)
    city = str(row.get("Город", "")).strip()
    region_id = None
    if city:
        region = db.query(Region).filter_by(city=city).first()
        if region:
            region_id = region.id

    existing = db.query(SaleData).filter_by(bs_number=bs_number).first()
    if existing:
        # Обновление
        existing.store_code = store_code
        existing.policy_type = policy_type
        existing.category = category
        existing.product_name = product_name
        existing.sale_date = sale_date
        existing.start_date = start_date
        existing.end_date = end_date
        existing.days_left = days_left
        existing.price = price
        existing.region_id = region_id
    else:
        # Добавление
        db.add(SaleData(
            bs_number=bs_number,
            store_code=store_code,
            policy_type=policy_type,
            category=category,
            product_name=product_name,
            sale_date=sale_date,
            start_date=start_date,
            end_date=end_date,
            days_left=days_left,
            price=price,
            region_id=region_id,
        ))

try:
    db.commit()
    print("✅ Импорт завершён успешно.")
except IntegrityError as e:
    db.rollback()
    print("❌ Ошибка при импорте:", e)
finally:
    db.close()
