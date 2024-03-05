from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base

url = 'postgresql://postgresql:postgresql@postgresql/postgresql'

engine = create_engine(url)

Base = declarative_base()