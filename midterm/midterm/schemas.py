from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
