from pydantic import BaseModel

class Film(BaseModel):
    name: str
    director: str

    class Config:
        from_attributes = True
