from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


url = 'postgresql://postgres:postgres@localhost:5433/postgres'

engine = create_engine(url)
session = Session(engine)

Base = declarative_base()

