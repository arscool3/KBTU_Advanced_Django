from datetime import datetime

from models import BinanceDealModel
from schemas import BinanceDeal
from database import session
import matplotlib.pyplot as plt
import numpy as np

def get_heatmap(start_date: datetime, end_date: datetime):
    response = get_from_db(start_date, end_date)
    timestamps = [deal.timestamp for deal in response]
    prices = [deal.price for deal in response]
    k_to_usd = [deal.k_to_usd for deal in response]

    timestamps_ord = [timestamp.toordinal() for timestamp in timestamps]


    # Plot heatmap
    plt.figure(figsize=(10, 6))
    plt.hexbin(timestamps_ord, prices, gridsize=20, cmap='hot')
    plt.colorbar(label='count in bin')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.title('Heatmap of Prices over Time')
    plt.savefig('heatmap.png')

    plt.show()
    return response


def get_from_db(start_date: datetime, end_date: datetime):
    db_session = session()
    print("!!!!!")
    binance_deals = db_session.query(BinanceDealModel).filter(
        BinanceDealModel.timestamp.between(start_date, end_date)
    ).all()
    db_session.close()
    return binance_deals

if __name__ == 'main':
    get_heatmap(start_date=datetime(2024, 4, 12), end_date=datetime(2024, 5, 2))


#output
# BTC-USD 69439.0 816.929
# BTC-USD 70113.0 1460.688
# BTC-USD 70284.0 1434.367
# BTC-USD 69849.0 712.745
# BTC-USD 69674.0 839.446
# BTC-USD 71635.0 1432.7
# BTC-USD 71235.0 1047.574
# BTC-USD 69505.0 1782.179
# BTC-USD 70619.0 3530.95
# BTC-USD 70495.0 1409.9
# BTC-USD 71234.0 989.361