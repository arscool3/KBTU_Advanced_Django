from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base

url = 'postgresql://postgres:postgres1@postgres/postgres'

engine = create_engine(url)

Base = declarative_base()