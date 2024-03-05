from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

url = 'postgresql://postgres:Haker15987@localhost/postgres4'

engine = create_engine(url)
session = Session(engine)

Base = declarative_base()