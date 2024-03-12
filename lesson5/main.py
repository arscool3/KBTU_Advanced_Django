import punq

import database as db
import models
import schemas
from fastapi import FastAPI, Depends
from reposiroty import CitizenRepository, AbcRepository, CountryRepository, PresidentRepository
app = FastAPI()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self._repo = repo

    def __call__(self, id: int) -> schemas.ReturnType:
        if id:
            return self._repo.get_by_id(id)
        return "Hello"


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=db.session))
    container.register(Dependency)
    return container


app.add_api_route("/citizens", get_container(CitizenRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/countries", get_container(CountryRepository).resolve(Dependency), methods=["GET"])
# app.add_api_route("/citizens", get_container(PresidentRepository).resolve(Dependency), methods=["GET"])


@app.post('/citizens')
def add_citizens(citizen: schemas.CreateCitizen):
    db.session.add(models.Citizen(**citizen.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{citizen.name} was added"


@app.post('/countries')
def add_countries(country: schemas.CreateCountry):
    db.session.add(models.Country(**country.model_dump()))
    db.session.commit()
    db.session.close()
    return f"{country.name} was added"

# @app.post('/citizens')
# def add_citizens(data: CreateType, dep_func=Depends(get_container(CitizenRepository).resolve(Dependency))):
#     return dep_func.add(data)

# dep_citizen = Dependency(repo=CitizenRepository(session=db.session))

# @app.get('/citizens')
# def add_citizens(dep_func: ReturnType = Depends(dep_citizen)):
#     return dep_func

# @app.post('/citizens')
# def add_citizens(dep_func: ReturnType = Depends(dep_citizen)):
#     return dep_func


# @app.get('/citizens')
# def get_citizens(name: str = None):
#     if name is None:
#         db_citizens = db.session.execute(select(db.Citizen)).scalars().all()
#     else:
#         db_citizens = db.session.execute(select(db.Citizen).where(db.Citizen.name == name)).scalars().all()
#     citizens = []
#     for citizen in db_citizens:
#         citizens.append(Citizen.model_validate(citizen))
#     return citizens
#
#


