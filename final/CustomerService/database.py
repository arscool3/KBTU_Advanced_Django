from config import DB_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

url = DB_URL
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()
