from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

def validate_database():
    if not database_exists(engine.url):
        create_database(engine.url)
#db, user,password, db_name

url='postgresql://postgres:postgres@localhost/posgtres'

engine=create_engine(url)
session=Session(engine)

Base=declarative_base()
