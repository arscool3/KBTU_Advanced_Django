from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy


class ConfigModel:
    id: Mapped[Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]]
    name: str


class ConfigSchema(BaseModel):
    id: int

    class Config:
        from_attributes = True
