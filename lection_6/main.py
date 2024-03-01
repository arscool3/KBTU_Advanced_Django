import database as db
import punq
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


app.add_api_route("/citizen/", get_container(repo=CitizenRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/country/", get_container(repo=CountryRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/president/", get_container(repo=PresidentRepository).resolve(Dependency), methods=["GET"])


@app.post("/citizen/")
def add_citizens(citizen: s.CreateCitizen):
    db.session.add(m.Citizen(**citizen.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"


@app.post("/country/")
def add_country(country: s.CreateCountry):
    db.session.add(m.Country(**country.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"


@app.post("/president/")
def add_president(president: s.CreatePresident):
    db.session.add(m.President(**president.model_dump()))
    db.session.commit()
    db.session.close()
    return "OK"
