from datetime import date
from typing import Annotated
from sqlalchemy.orm import sessionmaker

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship



url = 'sqlite:///e-store.db'
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

Base.metadata.create_all(engine)
