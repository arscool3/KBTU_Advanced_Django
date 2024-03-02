from pydantic import BaseModel

class Customer(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class Product(BaseModel):
    id:int
    name: str
    price: int

    class Config:
        from_attributes = True

class CartItem(BaseModel):
    id: int
    product_id: int
    cart_id: int
    quantity: int
    
class Cart(BaseModel):
    id: int
    customer_id:int
    

