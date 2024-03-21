import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URL = 'postgresql://postgres:password@localhost:5433/postgres'

engine = sqlalchemy.create_engine(DATABASE_URL)

session = Session(engine)

Base = declarative_base()


def get_db():
    try:
        yield session
        session.commit()
    finally:
        session.close()

# docker run --name postgres -e POSTGRES_PASSWORD=password -p 5433:5432 postgres

# alembic revision -m "initial_migration" --autogenerate
# alembic upgrade head / 8c9b2abc8029
