from sqlalchemy import create_engine
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship

url = 'postgresql://postgres:Haker15987@localhost/postgres2'

engine = create_engine(url)
session = Session(engine)


