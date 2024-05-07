from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Film(Base):
    __tablename__ = 'film'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    director = Column(String)

Base.metadata.create_all(bind=engine)

session = SessionLocal()
