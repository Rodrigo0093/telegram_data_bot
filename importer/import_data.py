import pandas as pd
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from db.models import Region, Store, SaleData
from datetime import datetime

# Загрузка Excel файлов
data_df = pd.read_excel("data/data.xlsx")
regions_df = pd.read_excel("data/city_regions.xlsx")
stores_df = pd.read_excel("data/store_addresses.xlsx")

# Словари справочников
city_to_region = {
    row["Город"].strip(): (row["Регион"].strip(), row["Округ"].strip())
    for _, row in regions_df.iterrows()
    if pd.notna(row["Город"])
}

store_info = {
    row["Магазин"].strip(): (row["Город"].strip(), row["Адрес"].strip())
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
            code = str(row.get("Код магазина")).strip()
            store = store_cache.get(code)
            if not store:
                continue

            price = row.get("Цена")
            try:
                price = float(price)
            except:
                price = None

            try:
                date = pd.to_datetime(row.get("Дата окончания"))
            except:
                date = None

            sale = SaleData(
                bs_number=str(row.get("Номер БС")).strip(),
                product_name=str(row.get("Наименование")),
                category=str(row.get("Категория")),
                price=price,
                end_date=date,
                store=store,
                region=store.region
            )
            db.add(sale)
        db.commit()

        print("✅ Импорт завершён успешно.")

    finally:
        db.close()

if __name__ == "__main__":
    import_data()
