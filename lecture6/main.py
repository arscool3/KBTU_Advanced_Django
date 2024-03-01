import punq
from fastapi import FastAPI, Depends
from pydantic import BaseModel

import database as db
from database import session
from repository import AbcRepository, CategoryRepository, UserRepository, OrderRepository, ProductRepository
from schemas import Product, Category, User, Order, CreateUser, CreateCategory

app = FastAPI()

class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> Product | Category| User | Order :
        return self.repo.get_by_id(id)

def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container


@app.post("/users")
def add_user(user: CreateUser) -> str:
    session.add(db.User(**user.dict()))
    session.commit()
    session.close()
    return "User was added"


@app.post("/orders")
def add_order(name: str, user_id: int):
    new_order = db.Order(name=name, user_id=user_id)
    session.add(new_order)
    session.commit()
    session.close()
    return "Order was added"


@app.post("/categories")
def add_category(category: CreateCategory):
    session.add(db.Category(**category.dict()))
    session.commit()
    session.close()
    return "Category was added"


@app.post("/products")
def add_product(name: str, category_id: int):
    new_product = db.Product(name=name, category_id=category_id)
    session.add(new_product)
    session.commit()
    session.close()
    return "Product was added"


@app.get("/users")
def get_users(dependency_func: BaseModel = Depends(get_container(UserRepository).resolve(Dependency))):
    return dependency_func


@app.get("/categories")
def get_categories(dependency_func: BaseModel = Depends(get_container(CategoryRepository).resolve(Dependency))):
    return dependency_func


@app.get("/products")
def get_products(dependency_func: BaseModel = Depends(get_container(ProductRepository).resolve(Dependency))):
    return dependency_func


@app.get("/orders")
def get_orders(dependency_func: BaseModel = Depends(get_container(OrderRepository).resolve(Dependency))):
    return dependency_func


# Create Web Application using FastAPI
# You need to implement
# at least 8 endpoints (get, post)
# at least 4 model
# at least 3 relationships (many to mane; one to one and etc.)
# at least 1 dependency injection as class (callable) and 2 as methods

# Docker: 49dee0cac4d4f2007556932c49d94f364057408d08305f87ba126cf1e3204a52
