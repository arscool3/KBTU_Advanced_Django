from pydantic import BaseModel


class Base(BaseModel):
    id: int
    name: str


a = Base(**{'id': 1, 'name': '<NAME>'})
print(a)