from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
import database as db

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    supplier_id: int
    category_id: int

    class Config:
        orm_mode = True

class Supplier(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post('/product')
def create_product(product: Product, session: db.Session = Depends(get_session)):
    session.add(db.Product(**product.dict()))
    session.commit()
    return f"Product {product.name} created successfully"

@app.get('/products')
def get_products(session: db.Session = Depends(get_session)):
    products = session.execute(select(db.Product)).scalars().all()
    return products

@app.get('/product/{product_id}')
def get_product(product_id: int, session: db.Session = Depends(get_session)):
    product = session.query(db.Product).filter(db.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post('/supplier')
def create_supplier(supplier_name: str, session: db.Session = Depends(get_session)):
    supplier = db.Supplier(name=supplier_name)
    session.add(supplier)
    session.commit()
    return f"Supplier {supplier_name} created successfully"

@app.get('/suppliers')
def get_suppliers(session: db.Session = Depends(get_session)):
    suppliers = session.execute(select(db.Supplier)).scalars().all()
    return suppliers

@app.post('/category')
def create_category(category_name: str, session: db.Session = Depends(get_session)):
    category = db.Category(name=category_name)
    session.add(category)
    session.commit()
    return f"Category {category_name} created successfully"

@app.get('/categories')
def get_categories(session: db.Session = Depends(get_session)):
    categories = session.execute(select(db.Category)).scalars().all()
    return categories

@app.delete('/product/{product_id}')
def delete_product(product_id: int, session: db.Session = Depends(get_session)):
    product = session.query(db.Product).filter(db.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return f"Product with ID {product_id} deleted successfully"

@app.delete('/supplier/{supplier_id}')
def delete_supplier(supplier_id: int, session: db.Session = Depends(get_session)):
    supplier = session.query(db.Supplier).filter(db.Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    session.delete(supplier)
    session.commit()
    return f"Supplier with ID {supplier_id} deleted successfully"

@app.delete('/category/{category_id}')
def delete_category(category_id: int, session: db.Session = Depends(get_session)):
    category = session.query(db.Category).filter(db.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return f"Category with ID {category_id} deleted successfully"