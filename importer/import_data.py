# importer/import_data.py
# Скрипт для импорта данных из Excel в базу данных

import pandas as pd
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from db.models import Region, Store, SaleData
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Утилита для безопасной обрезки строк из ячеек
def safe_strip(val):
    if isinstance(val, str):
        return val.strip()
    if pd.notna(val):
        return str(val).strip()
    return ""

# Загрузка Excel-файлов
data_df = pd.read_excel("data/data.xlsx")
regions_df = pd.read_excel("data/city_regions.xlsx")
stores_df = pd.read_excel("data/store_addresses.xlsx")

# Словари справочников
city_to_region = {
    safe_strip(row["Город"]): (safe_strip(row["Регион"]), safe_strip(row["Округ"]))
    for _, row in regions_df.iterrows()
    if pd.notna(row["Город"])
}

store_info = {
    safe_strip(row["Магазин"]): (safe_strip(row["Город"]), safe_strip(row["Адрес"]))
    for _, row in stores_df.iterrows()
    if pd.notna(row["Магазин"])
}

def import_data():
    db: Session = SessionLocal()
    try:
        # Очистка старых данных
        db.query(SaleData).delete()
        db.query(Store).delete()
        db.query(Region).delete()
        db.commit()

        # Импорт регионов
        region_cache = {}
        for city, (region, district) in city_to_region.items():
            r = Region(city=city, region=region, district=district)
            db.add(r)
            region_cache[city] = r
        db.commit()

        # Импорт магазинов
        store_cache = {}
        for code, (city, address) in store_info.items():
            region = region_cache.get(city)
            if not region:
                continue
            s = Store(store_code=code, city=city, address=address, region=region)
            db.add(s)
            store_cache[code] = s
        db.commit()

        # Импорт продаж
        for _, row in data_df.iterrows():
            code = safe_strip(row.get("Код магазина"))
            store = store_cache.get(code)
            if not store:
                continue

            price = row.get("Цена") or 0
            # Преобразуем дату окончания
            end_date = row.get("Дата окончания")
            end_date = pd.to_datetime(end_date) if pd.notna(end_date) else None

            sd = SaleData(
                bs_number=safe_strip(row.get("БС№")),
                product_name=safe_strip(row.get("Наименование")),
                category=safe_strip(row.get("Категория")),
                price=float(price),
                end_date=end_date,
                store=store,
                region=store.region
            )
            db.add(sd)
        db.commit()

        logger.info("✅ Импорт данных завершён успешно.")
    except Exception as e:
        logger.exception("Ошибка при импорте данных:")
        db.rollback()
        raise
    finally:
        db.close()
