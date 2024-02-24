from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select, insert
from fastapi import FastAPI

import models as db
from database import session
from schemas import Citizen, CreateCitizen, Country, CreateCountry, CreatePresident, President
from repository import CitizenRepository, AbcRepository

app = FastAPI()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> BaseModel:
        return self.repo.get_by_id(id)


dep_citizen = Dependency(repo=CitizenRepository(session=session))


@app.get("/citizens")
def get_citizens(dependency_func: BaseModel = Depends(dep_citizen)):
    return dependency_func


@app.post("/citizens")
def add_citizens(citizen: CreateCitizen) -> str:
    session.add(db.Citizen(**citizen.model_dump()))
    session.commit()
    session.close()
    return "Citizen was added"


@app.post("/country")
def add_country(country: CreateCountry):
    session.add(db.Country(**country.model_dump()))
    session.commit()
    session.close()
    return "Country was added"


@app.get("/country")
def get_country():
    db_countries = session.execute(select(db.Country)).scalars().all()
    countries = []
    for db_country in db_countries:
        countries.append(Country.model_validate(db_country))
    return countries


@app.post("/president")
def add_president(president: CreatePresident):
    session.add(db.President(**president.model_dump()))
    session.commit()
    session.close()
    return "President was added"


@app.get("/president")
def get_presidents():
    db_presidents = session.execute(select(db.President)).scalars().all()
    presidents = []
    for db_president in db_presidents:
        presidents.append(President.model_validate(db_president))
    return presidents

# Database Transactions
# A -> B
# x, y, z packages

# Begin
# A x-> B
# A y-> B
# A z-> B
# Close

# Tinkoff Bank <-> Arslan <-> Nursultan
# Tinkoff Bank Deposit 100 tenge

# Tinkoff Bank 50 Tenge

# network Атомарность
# Open Session
# Arslan -50 tenge
# Nursultan +50 tenge
# Commit Session
# Close session