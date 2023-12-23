from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    mobile_number = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)

    purchases = relationship("Purchase", back_populates='customer')

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    units = Column(String(255), nullable=False)

    purchases = relationship("Purchase", back_populates='product')

class Purchase(Base):
    __tablename__ = 'purchases'
    purchase_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    estimated_shipment_date = Column(Date, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates='purchases')
    product = relationship("Product", back_populates='purchases')
