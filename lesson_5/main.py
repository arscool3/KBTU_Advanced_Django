import punq
from fastapi import FastAPI
import models as db
from database import session
from schemas import CreateCitizen, CreateCountry, CreatePresident, ReturnType
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

app.add_api_route("/country", get_container(CountryRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/president", get_container(PresidentRepository).resolve(Dependency), methods=["GET"])



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


@app.post("/president")
def add_president(president: CreatePresident):
    session.add(db.President(**president.model_dump()))
    session.commit()
    session.close()
    return "President was added"


# @app.get("/president")
# def get_presidents():
#     db_presidents = session.execute(select(db.President)).scalars().all()
#     presidents = []
#     for db_president in db_presidents:
#         presidents.append(President.model_validate(db_president))
#     return presidents

# @app.get("/country")
# def get_country():
#     db_countries = session.execute(select(db.Country)).scalars().all()
#     countries = []
#     for db_country in db_countries:
#         countries.append(Country.model_validate(db_country))
#     return countries
