import http

from sqlalchemy import select
from sqlalchemy.orm import Session

import models as db

from fastapi import FastAPI, HTTPException, Depends
from database import session
from schemas import BaseProduct, BaseCategory, BaseOrder, CreateOrder, CreateProduct, User, CreateUser

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.post("/users", response_model=dict)
def add_user(user: CreateUser, session: Session = Depends(get_db)):
    try:
        if user.password == "":
            return {"message": "Password is empty"}
        new_user = db.User(**user.model_dump())
        session.add(new_user)

        return {"message": "User added successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", response_model=list[User], tags=["User"])
def get_users(session: Session = Depends(get_db)):
    try:
        users = session.execute(select(db.User)).scalars().all()
        user_response = [User.validate(user) for user in users]
        return user_response
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=User, tags=["User"])
def get_user_by_id(user_id: str, session: Session = Depends(get_db)):
    try:
        user = session.query(db.User).filter(db.User.id == user_id).first()
        if user.id:
            return User.model_validate(user)
        else:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail={"message": "User not found"})
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/categories', response_model=list[BaseCategory])
def get_categories(session: Session = Depends(get_db)):
    try:
        db_categories = session.execute(select(db.Category)).scalars().all()
        return [BaseCategory.model_validate(c) for c in db_categories]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/categories', response_model=dict)
def add_category(category: BaseCategory):
    if not category.name:
        return {"message": "name is empty!"}

    session.add(db.Category(**category.model_dump()))

    return {"message": "category is created!"}


@app.get('/products')
def get_products(session: Session = Depends(get_db)):
    try:
        db_products = session.execute(select(db.Product)).scalars().all()
        return [BaseProduct.model_validate(c) for c in db_products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/products')
def add_product(product: CreateProduct):
    if not product.name:
        return {"message": "name is empty!"}

    session.add(db.Product(**product.model_dump()))

    return {"message": "product is created!"}


@app.get('/orders')
def get_orders(session: Session = Depends(get_db)):
    try:
        db_orders = session.execute(select(db.Order)).scalars().all()
        return [BaseOrder.model_validate(c) for c in db_orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/orders')
def add_order(order: CreateOrder):
    if not order.name:
        return {"message": "name is empty!"}

    session.add(db.Order(**order.model_dump()))

    return {"message": "order is created!"}


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
