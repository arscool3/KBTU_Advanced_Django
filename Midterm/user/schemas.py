from typing import Optional

from cart import schemas
from helpers import BaseSchema


class BaseUser(BaseSchema):
    name: str
    email: str


class User(BaseUser):
    id: int
    cart: Optional[schemas.Cart]


class CreateUser(BaseUser):
    pass
