import sqlalchemy
from sqlalchemy.orm import Session

url = f"postgresql://postgres:December1225@localhost/lesson_7"
engine = sqlalchemy.create_engine(url)
session = Session(engine)


