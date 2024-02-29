from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

url = 'postgresql://postgres:9792amina@localhost:5432/lesson_5'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()
