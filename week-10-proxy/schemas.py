from pydantic import BaseModel


class Restaurant(BaseModel):
    name: str
    cuisine: str