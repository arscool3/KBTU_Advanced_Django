import punq
from fastapi import FastAPI
from sqlalchemy import select

import models as db
from database import session
from schemas import *
from repository import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container


app.add_api_route("/items", get_container(ItemRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/users", get_container(UserRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/categories", get_container(CategoryRepository).resolve(Dependency), methods=["GET"])


@app.get("/all_items")
def get_items():
    db_items = session.execute(select(db.Item)).scalars().all()
    items = []
    for db_item in db_items:
        items.append(Item.model_validate(db_item))
    return items


@app.get("/all_users")
def get_users():
    db_users = session.execute(select(db.User)).scalars().all()
    users = []
    for db_user in db_users:
        users.append(User.model_validate(db_user))
    return users


@app.get("/all_categories")
def get_categories():
    db_categories = session.execute(select(db.Category)).scalars().all()
    categories = []
    for db_category in db_categories:
        categories.append(Category.model_validate(db_category))
    return categories


@app.post("/items")
def add_item(item: CreateItem):
    session.add(db.Item(**item.model_dump()))
    session.commit()
    session.close()
    return "Item was added"


@app.post("/users")
def add_user(user: CreateUser):
    session.add(db.User(**user.model_dump()))
    session.commit()
    session.close()
    return "User was added"


@app.post("/categories")
def add_category(category: CreateCategory):
    session.add(db.Category(**category.model_dump()))
    session.commit()
    session.close()
    return "Category was added"
