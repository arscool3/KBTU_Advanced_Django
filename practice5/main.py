import punq
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select, insert
from fastapi import FastAPI
from database import session

import models as db
from schemas import Citizen,CreateCitizen, CreateCountry,Country, CreatePresident, President
from repository import CitizenRepository,AbstractRepository
app=FastAPI()

class Dependency:
    def __init__(self,repo:AbstractRepository):
        self.repo=repo
    def __call__(self,id:int)->President|Country|Citizen:
        return self.repo.get_by_id(id)
    
 # for registering dependencies(from the bottom to the top)
def get_container(repository:type[AbstractRepository]) -> punq.Container:
    container=punq.Container()
    container.register(AbstractRepository,repository,instance=repository(session=session))
    container.register(Dependency)
    return container
   
#dependency_citizen=Dependency(repo=CitizenRepository(session=session))
@app.get('/citizensDependency')
def get_citizensDependency(dependency_func:BaseModel=Depends(get_container(CitizenRepository).resolve(Dependency))):
    return dependency_func

"""
same as the above function with the decorator but shorter
app.add_api_route("/citizensDependency",get_container(CitizenRepository).resolve(Dependency),methods=["GET"])
"""

@app.get('/citizens')
def get_citizens(name:str=None):
    if name is None:
        db_citizens=session.execute(
            select(db.Citizen)
        ).scalars().all()
    else:
        db_citizens=session.execute(
            select(db.Citizen).where(db.Citizen.name==name)
        ).scalars().all()

    citizens=[]
    for db_citizen in db_citizens:
        citizens.append(Citizen.model_validate(db_citizen))
    return citizens

@app.post('/citizens')
def add_citizens(citizen:CreateCitizen)->str:
    session.add(db.Citizen(**citizen.model_dump()))
    session.commit()
    session.close()    
    return 'Citizen was added'

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

@app.post('/president')
def add_president(president:CreatePresident)->str:
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