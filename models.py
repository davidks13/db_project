from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    mobile_number = Column(String)
    contact_person = Column(String)

    purchases = relationship("Purchase", back_populates='customer')

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    manufacturer = Column(String)
    units = Column(String)

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
