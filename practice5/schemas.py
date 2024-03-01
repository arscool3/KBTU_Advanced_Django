from pydantic import BaseModel
from datetime import date
class BaseCitizen(BaseModel):
    name:str
    age:int
    class Config:
        from_attributes=True

#create pydantic model
class Citizen(BaseCitizen):
    id:int

class CreateCitizen(BaseCitizen):
    pass


class BaseCountry(BaseModel):
    name:str
    created_at:date
    class Config:
        from_attributes=True
        
class Country(BaseCountry):
    id:int

class CreateCountry(BaseCountry):
    pass



class BasePresident(BaseModel):
    name:str
    class Config:
        from_attributes=True


class CreatePresident(BasePresident):

    country_id:int

class President(BasePresident):
    id:int
    country:Country
