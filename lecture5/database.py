from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = create_engine(url)
session = Session(engine)

Base = declarative_base()


# Country <-> President one to one
# Country <-> Person one to many

# 7dd1aea02f85 - alembic migration

# Docker: 141c952dfd49cd0b4e3bb68b9d1f8d348cc1c4d0f1c404002c26f6b2dfd38054
