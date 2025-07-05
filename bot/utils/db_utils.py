# db_utils.py

import pandas as pd
import logging
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from db.database import engine, SessionLocal
from db.models import Region, Store, SaleData
from datetime import datetime

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Загрузка Excel файлов
data_df = pd.read_excel("data/data.xlsx")
regions_df = pd.read_excel("data/city_regions.xlsx")
stores_df = pd.read_excel("data/store_addresses.xlsx")


# Утилита безопасного получения строк
def safe_strip(val):
    """Безопасно вызывает .strip(), если значение строка"""
    return str(val).strip() if pd.notna(val) else ""


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
        logger.info("🧹 Очистка старых данных...")
        db.query(SaleData).delete()
        db.query(Store).delete()
        db.query(Region).delete()
        db.commit()

        logger.info("📥 Импорт регионов...")
        region_cache = {}
        for city, (region, district) in city_to_region.items():
            r = Region(city=city, region=region, district=district)
            db.add(r)
            region_cache[city] = r
        db.commit()
        logger.info(f"✅ Импортировано регионов: {len(region_cache)}")

        logger.info("📦 Импорт магазинов...")
        store_cache = {}
        for code, (city, address) in store_info.items():
            region = region_cache.get(city)
            if not region:
                logger.warning(f"⚠️ Город {city} не найден в справочнике регионов.")
                continue
            s = Store(store_code=code, city=city, address=address, region=region)
            db.add(s)
            store_cache[code] = s
        db.commit()
        logger.info(f"✅ Импортировано магазинов: {len(store_cache)}")

        logger.info("💾 Импорт продаж...")
        added_sales = 0
        for _, row in data_df.iterrows():
            code = safe_strip(row.get("Код магазина"))
            store = store_cache.get(code)
            if not store:
                logger.warning(f"⚠️ Пропущен магазин с кодом: {code}")
                continue

            try:
                price = float(row.get("Цена"))
            except:
                price = None

            try:
                date = pd.to_datetime(row.get("Дата окончания"))
            except:
                date = None

            sale = SaleData(
                bs_number=safe_strip(row.get("Номер БС")),
                product_name=safe_strip(row.get("Наименование")),
                category=safe_strip(row.get("Категория")),
                price=price,
                end_date=date,
                store=store,
                region=store.region
            )
            db.add(sale)
            added_sales += 1
        db.commit()
        logger.info(f"✅ Импортировано продаж: {added_sales}")

    finally:
        db.close()
        logger.info("🔒 Подключение к БД закрыто.")


# 🚀 Дополнительные функции для фильтрации и поиска

def get_all_categories():
    db = SessionLocal()
    try:
        categories = db.query(SaleData.category).distinct().all()
        return sorted({c[0] for c in categories if c[0]})
    finally:
        db.close()


def get_all_regions():
    db = SessionLocal()
    try:
        regions = db.query(Region.region).distinct().all()
        return sorted({r[0] for r in regions if r[0]})
    finally:
        db.close()


def search_items(query: str = "", category: str = None, region: str = None, limit: int = 5, offset: int = 0):
    db = SessionLocal()
    try:
        q = db.query(SaleData).options(joinedload(SaleData.region))

        if query:
            q = q.filter(
                or_(
                    SaleData.product_name.ilike(f"%{query}%"),
                    SaleData.bs_number.ilike(f"%{query}%")
                )
            )

        if category:
            q = q.filter(SaleData.category == category)

        if region:
            q = q.join(SaleData.region).filter(Region.region == region)

        results = (
            q.order_by(SaleData.price.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return results
    finally:
        db.close()


# Для тестового запуска импорта
if __name__ == "__main__":
    import_data()
