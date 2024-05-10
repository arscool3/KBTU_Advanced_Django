# pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://postgres:4477@localhost/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

# Country <-> President one to one
# Country Person <-> One to Many

#alembic init alembic

#docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres

# alembic revision -m "initial_migration" --autogenerate
# alembic upgrade head / 8c9b2abc8029