from pydantic import BaseModel, Field


class Movie(BaseModel):
    name: str = Field(max_length=15)
    description: str = Field(max_length=140)
    rating: int = Field(gt=0, lt=5)
    director: str = Field(max_length=10)