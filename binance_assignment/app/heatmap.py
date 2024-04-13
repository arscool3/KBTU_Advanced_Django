from datetime import datetime

from models import BinanceDealModel
from schemas import BinanceDeal
from database import session


def get_heatmap(start_date: datetime, end_date: datetime):
    response = get_from_db(start_date, end_date)
    for row in response:
        print(row.symbol, row.price, row.k_to_usd)
    return response


def get_from_db(start_date: datetime, end_date: datetime):
    db_session = session()
    print("!!!!!")
    binance_deals = db_session.query(BinanceDealModel).filter(
        BinanceDealModel.timestamp.between(start_date, end_date)
    ).all()
    db_session.close()
    return binance_deals

if __name__ == '__main__':
    get_heatmap(start_date=datetime(2024, 4, 12), end_date=datetime(2024, 5, 2))