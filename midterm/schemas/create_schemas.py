from pydantic import BaseModel


class CreateMark(BaseModel):
    name: str
