from sqlalchemy import select, insert
from fastapi import FastAPI
from pydantic import BaseModel

import database as db

app = FastAPI()


class BaseCitizen(BaseModel):
    name: str
    age: int

    class Config:
        from_attributes = True


class Citizen(BaseCitizen):
    id: int


class CreateCitizen(BaseCitizen):
    pass


class President(BaseModel):
    id: str


class CreatePresident(President):
    name: str
    country_id: int


class Country(BaseModel):
    id: int


class CreateCountry(Country):
    name: str


@app.get("/citizens")
def get_citizens(name: str = None):
    if name is None:
        db_citizens = db.session.execute(
            select(db.Citizen)
        ).scalars().all()
    else:
        db_citizens = db.session.execute(
            select(db.Citizen).where(db.Citizen.name == name)
        ).scalars().all()
    citizens = []
    for db_citizen in db_citizens:
        citizens.append(Citizen.model_validate(db_citizen))
    return citizens


@app.post("/citizens")
def add_citizens(citizen: CreateCitizen) -> str:
    db.session.add(db.Citizen(**citizen.model_dump()))
    db.session.commit()
    db.session.close()
    return "Citizen was added"


@app.post("/president")
def add_president(president: CreatePresident) -> str:
    db.session.add(db.President(**president.model_dump()))
    db.session.commit()
    db.session.close()
    return "President was added"


@app.get("/president")
def get_president(name: str = None):
    if name is None:
        db_presidents = db.session.execute(
            select(db.President)
        ).scalars().all()
    else:
        db_presidents = db.session.execute(
            select(db.President).where(db.President.name == name)
        ).scalars().all()
    presidents = []
    for db_president in db_presidents:
        presidents.append(Citizen.model_validate(db_president))
    return presidents


@app.get("/country")
def get_country(name: str = None):
    if name is None:
        db_country = db.session.execute(
            select(db.Country)
        ).scalars().all()
    else:
        db_country = db.session.execute(
            select(db.Country).where(db.Country.name == name)
        ).scalars().all()
    countries = []
    for country in db_country:
        countries.append(Citizen.model_validate(db_country))
    return countries


@app.post("/country")
def add_country(country: CreateCountry) -> str:
    db.session.add(db.Country(**country.model_dump()))
    db.session.commit()
    db.session.close()
    return "Country was added"
