from sqlalchemy import select

import database as db

from fastapi import FastAPI, HTTPException
from database import session, execute_session
from schemas import BaseProduct, BaseCategory, BaseOrder, CreateOrder, CreateProduct

app = FastAPI()


@app.get('/categories')
def get_categories():
    db_categories = session.execute(select(db.Category)).scalars().all()
    categories = []
    for c in db_categories:
        categories.append(BaseCategory.model_validate(c))

    return categories


@app.post('/categories')
def add_category(category: BaseCategory):
    execute_session(db.Category(**category.model_dump()))
    return 'Category added'


@app.get('/products')
def get_products():
    db_products = session.execute(select(db.Product)).scalars().all()
    products = []
    for p in db_products:
        products.append(BaseProduct.model_validate(p))

    return products


@app.post('/products')
def add_product(product: CreateProduct):
    execute_session(db.Product(**product.model_dump()))
    return 'Product added'


@app.get('/orders')
def get_orders():
    db_orders = session.execute(select(db.Order)).scalars().all()
    orders = []
    for o in db_orders:
        orders.append(BaseOrder.model_validate(o))

    return orders


@app.post('/orders')
def add_order(order: CreateOrder):
    execute_session(db.Order(**order.model_dump()))
    return 'Order added'


@app.get('/categories/<int:category_id>/products')
def get_products_by_category(category_id):
    category = session.query(db.Category).filter(db.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return category.products


@app.get('/products/<int:product_id/orders')
def get_orders_by_product(product_id):
    product = session.query(db.Product).filter(db.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product.orders
