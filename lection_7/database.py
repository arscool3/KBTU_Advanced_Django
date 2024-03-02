from sqlalchemy import create_engine
from sqlalchemy.orm import Session

database_url = "postgresql://postgres:postgres@localhost/lecture_7"

engine = create_engine(url=database_url)

session = Session(engine)
