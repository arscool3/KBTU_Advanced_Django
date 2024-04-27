import punq
from pydantic import BaseModel
from sqlalchemy import select, insert
from typing import Annotated

from database import session

from fastapi import FastAPI, Depends
import database as db
import models as md
import schemas as sc
import repository as rp

app = FastAPI()


class Dependency:
    def __init__(self, repo: rp.AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> Annotated[sc.Dog, sc.Cat, sc.Human]:
        return self.repo.get_by_id(id)


def get_container(Repository: type[rp.AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(rp.AbcRepository, Repository, instance=Repository(session=db.session))
    container.register(Dependency)
    return container

@app.get("/cats")
def get_cats(
        dependency_func: BaseModel = Depends(get_container(Repository=rp.CatRepository).resolve(Dependency))):
    return dependency_func


@app.get("/dogs")
def get_dogs(
        dependency_func: BaseModel = Depends(get_container(Repository=rp.DogRepository).resolve(Dependency))):
    return dependency_func


@app.get("/human")
def get_human(
        dependency_func: BaseModel = Depends(get_container(Repository=rp.HumanRepository).resolve(Dependency))):
    return dependency_func



@app.get("/house")
def get_house(address: str = None):
    if address == None:
        db_houses = db.session.execute(select(md.House)).scalars().all()
    else:
        db_houses = db.session.execute(select(md.House).where(address=address)).all()
    houses = []
    for db_house in db_houses:
        houses.append(sc.House.model_validate(db_house))
    return houses

@app.post('/human')
def add_human(human: sc.Human):
    db.session.add(md.Human(**human.model_dump()))
    db.session.commit()
    db.session.close()

@app.post('/cats')
def add_cats(cat: sc.Cat):
    db.session.add(md.Cat(**cat.model_dump()))
    db.session.commit()
    db.session.close()
    return "Cat added!"

@app.post('/Dog')
def add_dogs(dog: sc.Dog):
    db.session.add(md.Dog(**dog.model_dump()))
    db.session.commit()
    db.session.close()
    return "Dog added!"

@app.post('/house')
def add_house(house: sc.House):
    db.session.add(md.House(**house.model_dump()))
    db.session.commit()
    db.session.close()