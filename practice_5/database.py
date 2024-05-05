# pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://postgres:postgres@localhost/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

# Country <-> President one to one
# Country Person <-> One to Many

