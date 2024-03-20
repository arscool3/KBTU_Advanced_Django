from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import mapped_column
import sqlalchemy


class ConfigModel(BaseModel):
    id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]
    name: str


class ConfigSchema(BaseModel):
    class Config:
        from_attributes = True
