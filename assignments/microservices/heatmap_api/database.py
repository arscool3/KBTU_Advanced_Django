from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

import os

url = os.environ.get('POSTGRES_URL')
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()
