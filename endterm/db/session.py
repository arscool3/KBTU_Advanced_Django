from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values

config = dotenv_values(".env")

DATABASE_URL = 'postgresql://{user}:{password}@localhost:5428/{database}'.format(
    user=config.get("POSTGRES_USER"),
    password=config.get("POSTGRES_PASSWORD"),
    database=config.get("POSTGRES_DB")
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from .base import Base
