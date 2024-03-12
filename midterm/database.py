from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://postgres:601246@localhost:5432/midterm'
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()
