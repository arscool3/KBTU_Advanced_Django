import os

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from dotenv import load_dotenv

load_dotenv()

url = "postgresql://%s:%s@%s:%s/%s" % (os.getenv("POSTGRES_USER"),
                                       os.getenv("POSTGRES_PASSWORD"),
                                       os.getenv("POSTGRES_HOST"),
                                       os.getenv("POSTGRES_PORT"),
                                       os.getenv("POSTGRES_DB"))

engine = sqlalchemy.create_engine(url)
session = Session(engine)
Base = declarative_base()
