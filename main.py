from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Customer, Product, Purchase
from schemas import (
    CustomerSchema, 
    ProductSchema, 
    PurchaseSchema, 
    CustomerCreate, 
    ProductCreate, 
    PurchaseCreate
)
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/check_db_connection")
async def check_db_connection(db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).first()

        if customer:
            return {"message": "Database connection successful!"}
        else:
            return {"message": "No records found in the database."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


@app.post("/customers/", response_model=CustomerSchema)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # db_customer = Customer(**customer.dict())
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=CustomerSchema)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# CRUD operations for products
@app.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# CRUD operations for purchases
@app.post("/purchases/", response_model=PurchaseSchema)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = PurchaseSchema(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchases/{purchase_id}", response_model=PurchaseSchema)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase
