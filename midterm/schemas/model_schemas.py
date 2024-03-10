from pydantic import BaseModel


class Mark(BaseModel):
    id: int
    name: str
