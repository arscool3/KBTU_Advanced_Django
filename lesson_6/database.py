from sqlalchemy import create_engine
from sqlalchemy.orm import Session

url = 'postgresql://postgres:Haker15987@localhost/postgres3'

engine = create_engine(url)
session = Session(engine)