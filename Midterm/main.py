from typing import List

from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session

from cart.repository import CartRepo
from cart.schemas import CreateCart
from cart_item.repository import CartItemRepo
from cart_item.schemas import CartItem, CreateCartItem
from category.repository import CategoryRepo
from category.schemas import CreateCategory
from database import get_db
from firm.repository import FirmRepo
from firm.schemas import CreateFirm
from product.repository import ProductRepo
from product.schemas import CreateProduct
from user.models import User
from user.repository import UserRepo
from user.schemas import BaseUser, CreateUser

app = FastAPI()


def get_user_repo(session: Session = Depends(get_db)):
    return UserRepo(session)


def get_product_repo(session: Session = Depends(get_db)):
    return ProductRepo(session)


def get_category_repo(session: Session = Depends(get_db)):
    return CategoryRepo(session)


def get_firm_repo(session: Session = Depends(get_db)):
    return FirmRepo(session)


def get_cart_item_repo(session: Session = Depends(get_db)):
    return CartItemRepo(session)


def get_cart_repo(session: Session = Depends(get_db)):
    return CartRepo(session)


@app.post("/users/")
def create_user(user: CreateUser, user_repo: UserRepo = Depends(get_user_repo)):
    new_user = user_repo.create(user)
    return new_user


@app.get("/users/")
def get_users(user_repo: UserRepo = Depends(get_user_repo)):
    all_users = user_repo.get_all()
    return all_users


@app.get("/users/{user_id}")
async def get_user(user_id: int, user_repo: UserRepo = Depends(get_user_repo)):
    us = user_repo.get_by_id(user_id)
    return us


@app.delete("/users")
async def delete_user(user_id: int, user_repo: UserRepo = Depends(get_user_repo)):
    return user_repo.delete(user_id)


@app.post("/products/")
async def create_product(product: CreateProduct, product_repo: ProductRepo = Depends(get_product_repo)):
    new_product = product_repo.create(product)
    return new_product


@app.get("/products/{product_id}")
async def get_product(product_id: int, product_repo: ProductRepo = Depends(get_product_repo)):
    product = product_repo.get_by_id(product_id)
    return product


@app.get("/products/")
async def get_products(product_repo: ProductRepo = Depends(get_product_repo)):
    products = product_repo.get_all()
    return products


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, product_repo: ProductRepo = Depends(get_product_repo)):
    product_repo.delete(product_id)


@app.get("/categories/")
async def list_category(category_repo: CategoryRepo = Depends(get_category_repo)):
    return category_repo.get_all()


@app.post("/categories/")
async def create_category(category: CreateCategory, category_repo: CategoryRepo = Depends(get_category_repo)):
    new_category = category_repo.create(category)
    return new_category


@app.get("/categories/{id}/")
async def get_category(id: int, category_repo: CategoryRepo = Depends(get_category_repo)):
    category = category_repo.get_by_id(id)
    return category


@app.delete("/categories/{id}")
async def delete_category(id: int, category_repo: CategoryRepo = Depends(get_category_repo)):
    return category_repo.delete(id)


@app.post("/firms/")
async def create_firm(firm: CreateFirm, firm_repo: FirmRepo = Depends(get_firm_repo)):
    return firm_repo.create(firm)

@app.get("/firms/{firm_id}")
async def get_firm(firm_id: int, firm_repo: FirmRepo = Depends(get_firm_repo)):
    return firm_repo.get_by_id(firm_id)


@app.get("/firms/")
async def get_firms(firm_repo: FirmRepo = Depends(get_firm_repo)):
    firms = firm_repo.get_all()
    return firms

@app.delete("/firm/{firm_id}")
async def delete_firm(firm_id: int, firm_repo: FirmRepo = Depends(get_firm_repo)):
    return firm_repo.delete(firm_id)


@app.post("/cart_items/")
async def create_cart_item(cart_item: CreateCartItem, cart_repo: CartItemRepo = Depends(get_cart_item_repo)):
    new_cart_item = cart_repo.create(cart_item)
    return new_cart_item


@app.get("/cart_items/")
async def get_cart_items(cart_repo: CartItemRepo = Depends(get_cart_item_repo)):
    cart_items = cart_repo.get_all()
    return cart_items


@app.get("/cart_items/{cart_item_id}/")
async def get_cart_item(id: int, cart_repo: CartItemRepo = Depends(get_cart_item_repo)):
    cart_item = cart_repo.get_by_id(id)
    return cart_item


@app.delete("/cart_items/{cart_item_id}")
async def delete_cart_item(id: int, cart_repo: CartItemRepo = Depends(get_cart_item_repo)):
    return cart_repo.delete(id)


@app.post("/carts/")
async def create_cart(cart: CreateCart, cart_repo: CartRepo = Depends(get_cart_repo)):
    return cart_repo.create(cart)


@app.get("/carts/")
async def get_carts(cart_repo: CartRepo = Depends(get_cart_repo)):
    return cart_repo.get_all()


@app.get("/carts/{cart_id}/")
async def get_cart(id: int, cart_repo: CartRepo = Depends(get_cart_repo)):
    return cart_repo.get_by_id(id)


@app.delete("/carts/{cart_id}/")
async def delete_cart(id: int, cart_repo: CartRepo = Depends(get_cart_repo)):
    return cart_repo.delete(id)
