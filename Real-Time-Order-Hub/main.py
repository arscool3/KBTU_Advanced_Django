from fastapi import FastAPI
from database.db import *
from repository import *
from typing import Type
import punq
from typing import List
from models import *


app = FastAPI()

session = sessionmaker(bind=engine)

class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self) -> List[ReturnType]:
        return self.repo.get_all()


class Dependency1(Dependency):
    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)


def get_container(repository: Type[AbcRepository]) -> punq.Container:
    db = SessionLocal()
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=db))
    container.register(Dependency)
    container.register(Dependency1)
    return container


app.add_api_route("/products", get_container(ProductRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/product_by_id", get_container(ProductRepository).resolve(Dependency1), methods=["GET"])
