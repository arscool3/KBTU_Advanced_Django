from pydantic import BaseModel


class Film(BaseModel):
    name: str
    director: str