from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(url)

session = Session(engine)

Base = declarative_base()

# alembic init

# docker
# docker run --name postgres  -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres


# alembic revision -m "initial_migration" --autogenerate
# alembic upgrade head / hash

from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

class Film(Base):
    __tablename__ = "films"

    id: Mapped[_id]
    name: Mapped[str]
    director: Mapped[str]




