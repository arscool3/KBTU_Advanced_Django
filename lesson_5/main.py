import punq
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select, insert
from fastapi import FastAPI

import models as db
from database import session
from schemas import Citizen, CreateCitizen, Country, CreateCountry, CreatePresident, President, ReturnType
from repository import CitizenRepository, AbcRepository, CountryRepository, PresidentRepository

app = FastAPI()


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


app.add_api_route("/citizens", get_container(CitizenRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/countries", get_container(CountryRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/presidents", get_container(PresidentRepository).resolve(Dependency), methods=["GET"])


@app.post("/citizens")
def add_citizens(citizen: CreateCitizen) -> str:
    session.add(db.Citizen(**citizen.model_dump()))
    session.commit()
    session.close()
    return "Citizen was added"


@app.post("/countries")
def add_country(country: CreateCountry):
    session.add(db.Country(**country.model_dump()))
    session.commit()
    session.close()
    return "Country was added"


@app.post("/presidents")
def add_president(president: CreatePresident):
    session.add(db.President(**president.model_dump()))
    session.commit()
    session.close()
    return "President was added"

