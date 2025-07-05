from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    store_code = Column(Integer, unique=True, nullable=False)
    city = Column(String)
    address = Column(Text)

    sales = relationship("SaleData", back_populates="store")


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    city = Column(String, unique=True)
    region = Column(String)
    district = Column(String)

    sales = relationship("SaleData", back_populates="region")


class SaleData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True)
    bs_number = Column(String, unique=True, nullable=False)  # БС№
    store_code = Column(Integer, ForeignKey("stores.store_code"))
    policy_type = Column(Text)
    category = Column(String)
    product_name = Column(Text)
    sale_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    days_left = Column(Integer)
    price = Column(Numeric)
    region_id = Column(Integer, ForeignKey("regions.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    store = relationship("Store", back_populates="sales")
    region = relationship("Region", back_populates="sales")
