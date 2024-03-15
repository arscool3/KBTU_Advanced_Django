import database as db
import punq

import models
import schemas as s
from fastapi import *
from repository import *

app = FastAPI()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> Citizen | President | Country:
        return self.repo.get_by_id(id)


def get_container(repo: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repo, instance=repo(db=db.session))
    container.register(Dependency)
    return container


def get_dependency(schema):
    def get_db_country(id: int):
        db_country = db.session.get(m.Country, id)
        country = schema.model_validate(db_country)
        return country

    return get_db_country


app.add_api_route("/citizen/", get_container(repo=CitizenRepository).resolve(Dependency), methods=["GET"])


@app.post("/citizen/")
def add_citizens(citizen: s.CreateCitizen):
    db.session.add(m.Citizen(**citizen.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"


app.add_api_route("/country/", get_container(repo=CountryRepository).resolve(Dependency), methods=["GET"])


@app.post("/country/")
def add_country(country: s.CreateCountry):
    db.session.add(m.Country(**country.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"


@app.get("/country/president/")
def get_president_by_country(country: CountryWithPresident = Depends(get_dependency(CountryWithPresident))):
    return country.president


@app.get("/country/citizens/")
def get_citizens_by_country(country: CountryWithCitizens = Depends(get_dependency(CountryWithCitizens))):
    return country.citizens


@app.get("/country/citizens/num/")
def get_citizens_by_country(country: CountryWithCitizens = Depends(get_dependency(CountryWithCitizens))):
    return len(country.citizens)


app.add_api_route("/president/", get_container(repo=PresidentRepository).resolve(Dependency), methods=["GET"])


@app.post("/president/")
def add_president(president: s.CreatePresident):
    db.session.add(m.President(**president.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"


@app.post("/union/")
def add_union(union: s.BaseUnion):
    db.session.add(m.Union(**union.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"


@app.get("/union/")
def get_union_by_id(id: int):
    db_union = db.session.get(m.Union, id)
    union = Union.model_validate(db_union)
    return union


@app.get("/union/countries/")
def get_union_countries(id: int):
    db_union = db.session.get(m.Union, id)
    union = UnionWithCountries.model_validate(db_union)
    return union.countries


@app.post("/union/countries/add/")
def add_country_to_union(id: int, country_id: int):
    db_union = db.session.get(m.Union, id)
    db_country = db.session.get(m.Country, country_id)
    db_union.countries.append(db_country)
    db.session.commit()
    db.session.close()
    return "Added"
