from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('DATABASE_URL')
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()