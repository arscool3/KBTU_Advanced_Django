from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

session = Session(engine)
