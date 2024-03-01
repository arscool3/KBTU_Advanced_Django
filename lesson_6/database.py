from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = 'postgresql://postgres:9792amina@localhost:5432/lesson_6'
engine = create_engine(url)
session = Session(engine)

