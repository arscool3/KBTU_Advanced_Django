from typing import Annotated

from pydantic import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
import sqlalchemy


class ConfigModel:
    id: Mapped[Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]]
    name: Mapped[str]


class ConfigSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True
