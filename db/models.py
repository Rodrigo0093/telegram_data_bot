# models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Region(Base):
    """
    Модель региона (город, регион, округ)
    """
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    region = Column(String, nullable=True)
    district = Column(String, nullable=True)

    stores = relationship("Store", back_populates="region")
    sales = relationship("SaleData", back_populates="region")

class Store(Base):
    """
    Модель магазина: код, город, адрес
    """
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    store_code = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)

    region = relationship("Region", back_populates="stores")
    sales = relationship("SaleData", back_populates="store")

class SaleData(Base):
    """
    Модель продаж: товар, цена, срок действия и связи с магазином и регионом
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    bs_number = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    end_date = Column(Date, nullable=True)

    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)

    store = relationship("Store", back_populates="sales")
    region = relationship("Region", back_populates="sales")
