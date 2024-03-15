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


class Order(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class Customer(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Cart(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


class DelSession():
    def __init__(self):
        self.session = db.SessionLocal()
    def __enter__(self):
        return self.session
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


def get_db_session():
    with DelSession() as session:
        yield session


@app.post('/product')
def create_product(product: Product, session: db.Session = Depends(get_db_session)):
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
    session.delete(product)
    session.commit()
    return f"Product with ID {product_id} deleted successfully"


@app.delete('/supplier/{supplier_id}')
def delete_supplier(supplier_id: int, session: db.Session = Depends(get_db_session)):
    supplier = session.query(db.Supplier).filter(db.Supplier.id == supplier_id).first()
    session.delete(supplier)
    session.commit()
    return f"Supplier with ID {supplier_id} deleted successfully"


@app.delete('/category/{category_id}')
def delete_category(category_id: int, session: db.Session = Depends(get_session)):
    category = session.query(db.Category).filter(db.Category.id == category_id).first()
    session.delete(category)
    session.commit()
    return f"Category with ID {category_id} deleted successfully"


@app.put('/product/{product_id}')
def update_product(product_id: int, product: Product, session: db.Session = Depends(get_session)):
    db_product = session.query(db.Product).filter(db.Product.id == product_id).first()
    db_product.name = product.name
    db_product.supplier_id = product.supplier_id
    db_product.category_id = product.category_id
    session.commit()
    return f"Product with ID {product_id} updated successfully"


@app.put('/supplier/{supplier_id}')
def update_supplier(supplier_id: int, supplier_name: str, session: db.Session = Depends(get_session)):
    db_supplier = session.query(db.Supplier).filter(db.Supplier.id == supplier_id).first()
    db_supplier.name = supplier_name
    session.commit()
    return f"Supplier with ID {supplier_id} updated successfully"


@app.put('/category/{category_id}')
def update_category(category_id: int, category_name: str, session: db.Session = Depends(get_session)):
    db_category = session.query(db.Category).filter(db.Category.id == category_id).first()
    db_category.name = category_name
    session.commit()
    return f"Category with ID {category_id} updated successfully"


@app.post('/order')
def create_order(order: Order, session: db.Session = Depends(get_session)):
    db_order = db.Order(**order.dict())
    session.add(db_order)
    session.commit()
    return f"Order with ID {db_order.id} created successfully"


@app.get('/orders')
def get_orders(session: db.Session = Depends(get_session)):
    orders = session.execute(select(db.Order)).scalars().all()
    return orders


@app.post('/customer')
def create_customer(customer_name: str, session: db.Session = Depends(get_session)):
    customer = db.Customer(name=customer_name)
    session.add(customer)
    session.commit()
    return f"Customer {customer_name} created successfully"


@app.get('/customers')
def get_customers(session: db.Session = Depends(get_session)):
    customers = session.execute(select(db.Customer)).scalars().all()
    return customers


@app.post('/cart')
def add_to_cart(cart: Cart, session: db.Session = Depends(get_session)):
    db_cart = db.Cart(**cart.dict())
    session.add(db_cart)
    session.commit()
    return f"Item added to cart successfully"


@app.get('/cart/{customer_id}')
def get_cart(customer_id: int, session: db.Session = Depends(get_session)):
    cart_items = session.query(db.Cart).filter(db.Cart.customer_id == customer_id).all()
    return cart_items


@app.delete('/cart/{cart_id}')
def remove_from_cart(cart_id: int, session: db.Session = Depends(get_session)):
    cart_item = session.query(db.Cart).filter(db.Cart.id == cart_id).first()
    session.delete(cart_item)
    session.commit()
    return f"Item removed from cart successfully"
