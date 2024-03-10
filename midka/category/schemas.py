from typing import List
from utils.schemas_config import BaseSchema


class BaseCategory(BaseSchema):
    title: str


class CreateCategory(BaseCategory):
    pass


class Category(BaseCategory):
    id: int
