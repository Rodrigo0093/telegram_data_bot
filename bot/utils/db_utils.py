# bot/utils/db_utils.py
# Утилиты для работы с базой данных и проверки доступа пользователей

import os
import logging
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

from db.database import SessionLocal
from db.models import SaleData, Region, Store

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Загрузка списков пользователей из .env
ADMIN_USERS = set(map(int, os.getenv("ADMIN_USERS", "").split(","))) if os.getenv("ADMIN_USERS") else set()
ALLOWED_USERS = set(map(int, os.getenv("ALLOWED_USERS", "").split(","))) if os.getenv("ALLOWED_USERS") else set()

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_USERS

def is_allowed(user_id: int) -> bool:
    allowed = user_id in ALLOWED_USERS or is_admin(user_id)
    logger.debug(f"[auth] is_allowed({user_id}) -> {allowed}")
    return allowed

def search_items(query: str):
    session = SessionLocal()
    try:
        results = session.query(SaleData)\
            .options(joinedload(SaleData.region))\
            .filter(or_(SaleData.bs_number == query,
                        SaleData.product_name.ilike(f"%{query}%")))\
            .all()
        logger.info(f"[search] Найдено {len(results)} товаров по запросу '{query}'")
        return results
    finally:
        session.close()

def get_all_regions() -> list[str]:
    session = SessionLocal()
    try:
        rows = session.query(Region.region).distinct().order_by(Region.region).all()
        return [r[0] for r in rows if r[0]]
    finally:
        session.close()

def get_cities_for_region(region: str) -> list[str]:
    session = SessionLocal()
    try:
        rows = session.query(Store.city)\
            .join(Region, Store.region_id == Region.id)\
            .filter(Region.region == region)\
            .distinct().order_by(Store.city).all()
        return [r[0] for r in rows if r[0]]
    finally:
        session.close()

def get_categories_for_region_city(region: str, city: str) -> list[str]:
    session = SessionLocal()
    try:
        rows = session.query(SaleData.category)\
            .join(Store, SaleData.store_id == Store.id)\
            .filter(Store.city == city, Store.region.has(region=region))\
            .distinct().order_by(SaleData.category).all()
        return [r[0] for r in rows if r[0]]
    finally:
        session.close()

def get_products_by_filter(
    category: str=None,
    region: str=None,
    city: str=None,
    limit: int=5,
    offset: int=0
) -> list[SaleData]:
    session = SessionLocal()
    try:
        query = session.query(SaleData).options(joinedload(SaleData.region))
        if region:
            query = query.filter(SaleData.region.has(region=region))
        if city:
            query = query.filter(SaleData.region.has(city=city))
        if category:
            query = query.filter(SaleData.category == category)
        results = query.order_by(SaleData.price.desc()).offset(offset).limit(limit).all()
        logger.info(
            f"[db] Фильтр region={region}, city={city}, category={category}, "
            f"offset={offset} → {len(results)} товаров"
        )
        return results
    finally:
        session.close()
