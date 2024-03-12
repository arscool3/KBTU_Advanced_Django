from pydantic import BaseModel


class User(BaseModel):

    class Config:
        from_attributes = True

    id: str
    username: str
    first_name: str
    last_name: str
    # password: str


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
