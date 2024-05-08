from pydantic import BaseModel


class Info(BaseModel):
    email: str
    username: str
    total: int
    order_id: str
    restaurant_id: str
    # data: dict
