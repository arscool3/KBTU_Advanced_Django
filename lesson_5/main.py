import punq
from typing import Union, List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine
from repository import AbcRepository, CitizenRepository, PresidentRepository, CountryRepository
from schemas import Citizen, Country, President

app = FastAPI()
RetrieveReturnType = Union[Citizen, Country, President]
ListReturnType = Union[List[Citizen], List[Country], List[President]]
session = Session(engine)


class RetrieveDependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> RetrieveReturnType:
        return self.repo.get_by_id(id)


class ListDependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self) -> ListReturnType:
        return self.repo.get_all()


def get_container(repository: type[AbcRepository]) -> punq:
    container = punq.Container()

    # register RetrieveDependency
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(RetrieveDependency)

    # register ListDependency
    container.register(ListDependency)
    return container


@app.get("/citizen")
async def get_citizen(dep_func: Citizen = Depends(get_container(CitizenRepository).resolve(RetrieveDependency))):
    return dep_func


@app.get("/citizens")
async def get_citizens(dep_func: List[Citizen] = Depends(get_container(CitizenRepository).resolve(ListDependency))):
    return dep_func


@app.get("/president")
async def get_president(dep_func: President = Depends(get_container(PresidentRepository).resolve(RetrieveDependency))):
    return dep_func


@app.get("/presidents")
async def get_presidents(dep_func: List[President] = Depends(get_container(PresidentRepository).resolve(ListDependency))):
    return dep_func


@app.get("/country")
async def get_country(dep_func: Country = Depends(get_container(CountryRepository).resolve(RetrieveDependency))):
    return dep_func


@app.get("/countries")
async def get_countries(dep_func: List[Country] = Depends(get_container(CountryRepository).resolve(ListDependency))):
    return dep_func
