from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str = None

class ProductCreate(ProductBase):
    price: float

class ProductOut(ProductBase):
    id: int
    price: float

    class Config:
        orm_mode = True
