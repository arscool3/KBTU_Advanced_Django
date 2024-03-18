import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


url = 'postgresql://postgres:password@localhost:5435/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)
Base = declarative_base()

# docker run --name movie_postgres -e POSTGRES_PASSWORD=password -p 5435:5432 postgres

# alembic revision -m 'initial_migration' --autogenerate

# alembic upgrade head
