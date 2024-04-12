import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import settings

url = (f'postgresql://{settings.database_username}:{settings.database_password}@'
       f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}')

engine = sqlalchemy.create_engine(url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
