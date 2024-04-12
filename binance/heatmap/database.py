import sqlalchemy
from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.orm import Session, declarative_base, mapped_column, Mapped
from typing import Annotated

url = 'postgresql://postgres:postgres@localhost:5439/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Data(Base):
    __tablename__ = 'data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[str] = Column(DateTime, default=func.utcnow)
    name: Mapped[str] = mapped_column(nullable=False)
    k_to_usd: Mapped[float] = mapped_column(nullable=False)