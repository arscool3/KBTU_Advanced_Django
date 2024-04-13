# fake repository

import schemas
import models
from database import session


def insert_to_db(bitcoin: schemas.BitcoinCreate):
    session.add(models.Bitcoin(**bitcoin.model_dump()))
    session.commit()
    session.close()


def get_from_db(coin):
    bitcoin = session.query(models.Bitcoin).filter_by(coin=coin).all()
    print(f'{coin} has {len(bitcoin)} entry')
    session.close()
    return bitcoin