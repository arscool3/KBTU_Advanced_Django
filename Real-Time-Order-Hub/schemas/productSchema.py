from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    quantity: int

    class Config:
        from_attributes = True


class Product(ProductBase):
    id: int


class CreateProduct(BaseModel):
    pass