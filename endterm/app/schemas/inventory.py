from pydantic import BaseModel

class InventoryBase(BaseModel):
    product_id: int
    quantity: int

class InventoryOut(InventoryBase):
    
    class Config:
        orm_mode = True
