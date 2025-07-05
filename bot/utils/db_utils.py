from db.database import SessionLocal
from db.models import SaleData, Region
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

def get_all_categories():
    db = SessionLocal()
    try:
        categories = db.query(SaleData.category).distinct().all()
        return sorted([c[0] for c in categories if c[0]])
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
