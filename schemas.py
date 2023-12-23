from pydantic import BaseModel


class CustomerSchema(BaseModel):
    id: int
    name: str
    address: str
    mobile_number: str
    contact_person: str


class ProductSchema(BaseModel):
    manufacturer: str
    units: str


class PurchaseSchema(BaseModel):
    id: int
    customer_id: int
    product_id: int
    expected_delivery_date: str
    quantity: int
    price_per_unit: float


class ProductCreate(BaseModel):
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
    