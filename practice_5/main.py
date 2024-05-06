import punq
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from fastapi import FastAPI
from sqlalchemy.orm import dependency

import models as db
from database import session
from repository import CitizenRepository, AbcRepository, CountryRepository, PresidentRepository
from schemas import CreateCitizen, Country, CreateCountry, CreatePresident, President, Citizen

app = FastAPI()



class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> President | Citizen | Country :
        return self.repo.get_by_id(id)



def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container


app.add_api_route("/citizens", get_container(CitizenRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/countries", get_container(CountryRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/presidents", get_container(PresidentRepository).resolve(Dependency), methods=["GET"])



@app.get("/citizens")
def get_citizens(dependency_func: BaseModel = Depends(get_container(CitizenRepository).resolve(Dependency))):
    return dependency_func

@app.get("/countries")
def get_country(dependency_func: BaseModel = Depends(get_container(CountryRepository).resolve(Dependency))):
    return dependency_func


@app.get("/presidents")
def get_presidents(dependency_func: BaseModel = Depends(get_container(PresidentRepository).resolve(Dependency))):
    return dependency_func


@app.post("/citizens")
def add_citizens(citizen: CreateCitizen) -> str:
    session.add(db.Citizen(**citizen.dict()))
    session.commit()
    session.close()
    return "Citizen was added"

@app.post("/countries")
def add_country(country: CreateCountry):
    session.add(db.Country(**country.dict()))
    session.commit()
    session.close()
    return "Country was added"

@app.post("/presidents")
def add_president(name: str, country_id: int):
    new_president = db.President(name=name, country_id=country_id)
    session.add(new_president)
    session.commit()
    session.close()
    return "President was added"
