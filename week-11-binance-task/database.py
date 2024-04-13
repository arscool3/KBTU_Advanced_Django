import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from models import Bitcoin

url = 'postgresql://postgres:postgres@localhost:5433/postgres'
engine = sqlalchemy.create_engine(url)
session = Session(engine)
Base = declarative_base()


def insert_to_db(time, price, coin):
    new_entry = Bitcoin(time=time, price=price, coin=coin)
    session.add(new_entry)
    session.commit()
    session.close()


def get_from_db(coin):
    bitcoin = session.query(Bitcoin).filter_by(coin=coin).all()
    session.close()
    return bitcoin
