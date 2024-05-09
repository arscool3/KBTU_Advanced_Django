import schemas
from database import session, Currency

def insert_to_db(currency: schemas.CurrencyCreate):
    session.add(Currency(**currency.model_dump()))
    session.commit()
    session.close()


def get_from_db(coin):
    currency = session.query(Currency).filter_by(coin=coin).all()
    print(f'{coin} has {len(currency)} entry')
    session.close()
    return currency