from pydantic import BaseModel


class Info(BaseModel):
    email: str
    username: str
    # data: dict
