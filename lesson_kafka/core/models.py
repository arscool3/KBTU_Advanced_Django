import pydantic


class Film(pydantic.BaseModel):
    name: str
    director: str

    class Config:
        from_attributes = True
