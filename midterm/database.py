import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://postgres:JASIK_2004@localhost:5432/adv_django_midterm'
engine = sqlalchemy.create_engine(url)

session = Session(engine)

Base = declarative_base()
