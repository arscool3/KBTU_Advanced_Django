from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

url = "postgresql://postgres:1234@localhost/postgres"

engine = create_engine(url)

session = Session(engine)

Base = declarative_base()

# alembic init alembic

# docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres

# alembic revision -m "initial_migration" --autogenerate
# alembic upgrade head / 8c9b2abc8029


_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Currency(Base):
    __tablename__ = "Currency"

    id: Mapped[_id]
    name: Mapped[str]
    timestamp: Mapped[datetime]
    coefficient: Mapped[float]

class WorkTime(Base):
    __tablename__ = "WorkTime"

    id: Mapped[_id]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
