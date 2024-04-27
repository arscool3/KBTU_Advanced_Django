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

    def __call__(self, id: int) -> Annotated[sc.Country, sc.Citizen, sc.President]:
        return self.repo.get_by_id(id)


def get_container(Repository: type[rp.AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(rp.AbcRepository, Repository, instance=Repository(session=db.session))
    container.register(Dependency)
    return container

@app.get("/citizens")
def get_citizenss(
        dependency_func: BaseModel = Depends(get_container(Repository=rp.CitizenRepository).resolve(Dependency))):
    return dependency_func


@app.get("/countries")
def get_counries(
        dependency_func: BaseModel = Depends(get_container(Repository=rp.CountryRepository).resolve(Dependency))):
    return dependency_func


@app.get("/presidents")
def get_presidents(
        dependency_func: BaseModel = Depends(get_container(Repository=rp.PresidentRepository).resolve(Dependency))):
    return dependency_func


@app.post('/citizens')
def add_citizens(citizen: sc.Citizen):
    db.session.add(db.Citizen(**citizen.model_dump()))
    db.session.commit()
    db.session.close()
    return "ok!"


@app.get("/country")
def get_countries(name: str = None):
    if str == None:
        db_countries = db.session.execute(select(md.Citizen)).scalars().all()
    else:
        db_countries = db.session.execute(select(md.Citizen).where(name=name)).all()
    citizens = []
    for db_country in db_countries:
        citizens.append(sc.Country.model_validate(db_country))
    return citizens


@app.post('/country')
def add_citizens(country: sc.Country):
    db.session.add(md.Country(**country.model_dump()))
    db.session.commit()
    db.session.close()
    return "ok!"
