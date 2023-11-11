from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), index=True)
    price = Column(Float)
    inventory_id = Column(Integer, ForeignKey('inventory.product_id'))

class Inventory(Base):
    __tablename__ = "inventory"
    product_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    product = relationship("Product", back_populates="inventory")

class Sale(Base):
    __tablename__ = "sales"
    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity_sold = Column(Integer)
    total_amount = Column(Float)
    sale_date = Column(Date)
    product = relationship("Product", back_populates="sales")

Product.inventory = relationship("Inventory", back_populates="product")
Product.sales = relationship("Sale", back_populates="product")

