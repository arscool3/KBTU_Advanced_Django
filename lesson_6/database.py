from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = 'postgresql://postgres:postgres@localhost:5432/lesson6'
engine = create_engine(url)
session = Session(engine)
