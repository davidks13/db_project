from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi import APIRouter
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
from sqlalchemy import func, asc, desc, create_engine, Index, String
from typing import List
from sqlalchemy.orm import selectinload
from database import DATABASE_URL
from databases import Database
from create_db import engine

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
# ORM
session = SessionLocal()
customer = Customer(name='Sam Altman', address='OpenAI st. 1', mobile_number='+1 8888 8888', contact_person='Sam Altman')
session.add(customer)
session.commit()

# READ
customers = session.query(Customer).all()
for customer in customers:
    print(customer.name, customer.contact_person)

# UPD
customer_update_or_new_ceo = session.query(Customer).filter_by(name='Sam Altman').first()
customer_update_or_new_ceo.name = 'Someone'
session.commit()

# DELETE
customer = session.query(Customer).filter_by(name='Someone').first()
session.delete(customer)
session.commit()


@router.get("/check_db_connection")
async def check_db_connection(db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).first()

        if customer:
            return {"message": "Database connection successful!"}
        else:
            return {"message": "No records found in the database."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


@router.post("/customers/", response_model=CustomerSchema)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/customers/{customer_id}", response_model=CustomerSchema)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


# CRUD operations for products
@router.post("/products/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# CRUD operations for purchases
@router.post("/purchases/", response_model=PurchaseSchema)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = Purchase(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


@router.get("/purchases/{purchase_id}", response_model=PurchaseSchema)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase


@router.put("/customers/{customer_id}", response_model=CustomerSchema)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.delete("/customers/{customer_id}", response_model=CustomerSchema)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()
    return db_customer


# CRUD operations for products
@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", response_model=ProductSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product


# CRUD operations for purchases
@router.put("/purchases/{purchase_id}", response_model=PurchaseSchema)
def update_purchase(purchase_id: int, purchase: PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")

    for key, value in purchase.model_dump().items():
        setattr(db_purchase, key, value)

    db.commit()
    db.refresh(db_purchase)
    return db_purchase


@router.delete("/purchases/{purchase_id}", response_model=PurchaseSchema)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = db.query(Purchase).filter(Purchase.purchase_id == purchase_id).first()
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")

    db.delete(db_purchase)
    db.commit()
    return db_purchase


@router.get("/customers/", response_model=List[CustomerSchema])
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers


# Retrieving all products
@router.get("/products/", response_model=List[ProductSchema])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


# Retrieving all purchases
@router.get("/purchases/", response_model=List[PurchaseSchema])
def get_all_purchases(db: Session = Depends(get_db)):
    purchases = db.query(Purchase).all()
    return purchases


# SELECT WHERE
@router.get("/customers/filter/")
def filter_customers(
    name: str = Query(None, title="Name filter", description="Filter customers by name"),
    address: str = Query(None, title="Address filter", description="Filter customers by address"),
    db: Session = Depends(get_db)
):
    query = db.query(Customer)
    if name:
        query = query.filter(Customer.name == name)
    if address:
        query = query.filter(Customer.address == address)
    return query.all()


# JOIN
@router.get("/purchases_and_customers_info")
def purchases_with_customer_info(db: Session = Depends(get_db)):
    purchases_with_customer_info = (
        db.query(Purchase)
        .join(Customer, Purchase.customer_id == Customer.customer_id)
        .options(selectinload(Purchase.customer))
        .all()
    )

    return purchases_with_customer_info
        
    
# UPDATE with a non-trivial condition
@router.put("/update-customer/{customer_id}")
def update_customer(customer_id: int, new_name: str, db: Session = Depends(get_db)):
    db.query(Customer).filter(Customer.customer_id == customer_id).update({"name": new_name})
    db.commit()
    return {"detail": "Customer updated successfully"}


# GROUP BY
@router.get("/purchase-stats/")
def purchase_stats(db: Session = Depends(get_db)):
    stats = (
        db.query(
            Purchase.customer_id,
            func.count().label("total_purchases"),
            func.avg(Purchase.quantity).label("average_quantity")
        )
        .group_by(Purchase.customer_id)
        .all()
    )
    
    # Converting the results to a list of dictionaries
    stats_dict = [{"customer_id": customer_id, "total_purchases": total, "average_quantity": avg} for customer_id, total, avg in stats]
    return stats_dict


@router.get("/sorted_products/", response_model=List[ProductSchema])
def get_sorted_products(
    sort_by: str = Query(..., description="Column to sort by, e.g., product_name, manufacturer"),
    order: str = Query(..., description="Sort order, 'asc' or 'desc'."),
    db: Session = Depends(get_db)
):
    if order.lower() not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order parameter. Use "asc" or "desc".')

    sort_column = getattr(Product, sort_by, None)
    if sort_column is None:
        raise HTTPException(status_code=400, detail='Invalid sort_by parameter.')

    sorted_products = (
        db.query(Product)
        .order_by(asc(sort_column) if order.lower() == 'asc' else desc(sort_column))
        .all()
    )
    return sorted_products

@router.get('/setup-and-search')
def setup_and_search(query: str = Query(..., description="The search query")):
    try:
        # Copying values from existing_column to json_data
        session.execute(Product.__table__.update().values
                        (json_data=func.jsonb_build_object('product_name', Product.product_name)))

        # Creating a GIN index
        Index('idx_json_data_gin', Product.json_data, postgresql_using='gin').create(bind=engine)

        # Creating a pg_trgm index
        Index('idx_json_data_trgm', Product.json_data, postgresql_using='gin', postgresql_ops={'json_data': 'jsonb_path_ops,gin_trgm_ops'}).create(bind=engine)

        # Utilizing the GIN index for faster search
        result = (
            session.query(Product)
            .filter(
                Product.json_data.isnot(None),  # Excluding rows with empty json_data
                func.lower(func.jsonb_build_object(
                    'product_name', Product.product_name,
                    'json_data', func.cast(Product.json_data, String)  # Converting json_data to string if necessary
                )).op('~*')(f'.*{query}.*')  # Using the ~* operator for case-insensitive regular expression match
            )
        )

        result = result.all()  # Executing the query

        # Converting result to a list of dictionaries
        data = [{"product_id": row.product_id, "product_name": row.product_name, 
                 "json_data": row.json_data} for row in result]

        return data

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
