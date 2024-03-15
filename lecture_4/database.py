import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, Session, mapped_column

from typing import Annotated

url = 'postgresql://postgres:JASIK_2004@localhost/db_django'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

# Country President -> one-to-one
# Country Person -> one-to-many

_id = Annotated[int, mapped_column(sa.Integer, primary_key=True)]


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[_id]
    name: Mapped[str]
    population: Mapped[int]


class President(Base):
    __tablename__ = 'presidents'

    id: Mapped[_id]
    name: Mapped[str]


class Citizen(Base):
    __tablename__ = 'citizens'

    id: Mapped[_id]
    name: Mapped[str]
    age: Mapped[int]


# alembic revision -m "initial migration" --autogenerate
# alembic upgrade head
# docker run --name db_django -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
