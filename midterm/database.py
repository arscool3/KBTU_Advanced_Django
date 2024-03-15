from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = 'postgresql://postgres:yerkhan2003@localhost:5432/midterm_adv_django'
engine = create_engine(url)
session = Session(engine)
Base = declarative_base()
