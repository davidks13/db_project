from pydantic import BaseModel
from datetime import date


class CustomerSchema(BaseModel):
    name: str
    address: str
    mobile_number: str
    contact_person: str


class ProductSchema(BaseModel):
    product_name: str
    manufacturer: str
    units: str


class PurchaseSchema(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    estimated_shipment_date: date
    price_per_unit: float


class ProductCreate(BaseModel):
    product_name: str
    manufacturer: str
    units: str

class CustomerCreate(BaseModel):
    name: str
    address: str
    mobile_number: str
    contact_person: str

class PurchaseCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    estimated_shipment_date: str
    price_per_unit: float
    