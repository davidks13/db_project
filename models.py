from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Boolean, Integer, Column, Text, ForeignKey, Date, Float


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    manufacturer = Column(String(255), nullable=False)
    units = Column(String(255), nullable=False)
    
    
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    contact_person = Column(String(255), nullable=False)
    
    
class Purchase(Base):
    __tablename__ = 'purchases'
    purchase_id = Column(Integer, primary_key=True)  
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    Customer = relationship("Customer", back_populates='purchases')
    product_id = Column(Integer, ForeignKey("products.product_id"))
    Products = relationship("Customer", back_populates='products')
    quantity = Column(Integer, nullable=False)
    estimated_shipment_date = Column(Date, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    