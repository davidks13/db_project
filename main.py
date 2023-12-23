from sqlalchemy.orm import configure_mappers
from fastapi import FastAPI
from crud import router as crud_router

app = FastAPI()

# Include CRUD operations from crud.py
app.include_router(crud_router)

configure_mappers()
