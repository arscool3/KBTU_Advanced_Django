from datetime import datetime
from typing import Annotated
import sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped
from database import Base
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Bitcoin

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]

Session = sessionmaker(bind=engine)



class BitcoinData(Base):
    __tablename__ = 'bitcoindata'

    id: Mapped[_id]
    time: Mapped[datetime] = mapped_column(sqlalchemy.DateTime, default=datetime.now())
    price: Mapped[float]
    coin: Mapped[str]


def insert_to_db(bitcoin_data):
    session = Session()
    bitcoin = Bitcoin(**bitcoin_data.dict())
    session.add(bitcoin)
    session.commit()
    session.close()

def get_from_db(coin):
    session = Session()
    bitcoin_data = session.query(Bitcoin).filter_by(coin=coin).all()
    session.close()
    return bitcoin_data
