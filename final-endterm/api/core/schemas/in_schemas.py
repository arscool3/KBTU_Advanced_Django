from pydantic import BaseModel

__all__ = ['UserInSchema']


class UserInSchema(BaseModel):
    login: str
    password: str
