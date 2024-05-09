from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "postgresql://postgres:admin@localhost/store"

engine = create_engine(url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
