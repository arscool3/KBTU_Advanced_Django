from datetime import datetime

from lesson11.core.schemas import CreateData, Binance


def algo_service(message: Binance):
    tradeData = CreateData(
        time=datetime.now(),
        name=f'{message.pair.send_coin}_to_{message.pair.get_coin}',
        k_to_usd=message.pair.send_coin.amount / message.pair.get_coin.amount
    )
    return tradeData
