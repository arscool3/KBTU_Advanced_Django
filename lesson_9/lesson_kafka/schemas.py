from pydantic import BaseModel


class Film(BaseModel):
    name: str
    director: str
    genre: str
    recommendations: List[str] = []
