import punq
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from repository import AbcRepository, CitizenRepository, CountryRepository, PresidentRepository
from schemas import Citizen, BaseCitizen, Country, President
import models as db

app = FastAPI()
db_session = Session(engine)


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int):
        return self.repo.get_by_id(id)


def get_container(repository: type[AbcRepository]):
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(db_session))
    container.register(Dependency)
    return container



@app.post("/citizens")
async def create_citizen(citizen: BaseCitizen):
    db_session.add(db.Citizen(**citizen.model_dump()))
    db_session.commit()
    return "Successfully added"


@app.get("/citizen")
async def get_citizen(dep_func: Citizen = Depends(get_container(CitizenRepository).resolve(Dependency))):
    return dep_func


@app.get("/country")
async def get_country(dep_func: Country = Depends(get_container(CountryRepository).resolve(Dependency))):
    return dep_func


@app.get("/president")
async def get_country(dep_func: President = Depends(get_container(PresidentRepository).resolve(Dependency))):
    return dep_func


@app.get("/citizens")
async def get_citizens():
    citizens = db_session.execute(select(db.Citizen)).scalars().all()

    return [Citizen.model_validate(citizen) for citizen in citizens]
