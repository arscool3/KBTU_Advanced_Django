import random

from schemas import CreateCryptoTrade, Message


def process_binance_msg(message: Message) -> list[CreateCryptoTrade]:
    trades = [
        CreateCryptoTrade(
            currency=message.sold_currency.currency,
            k_to_usd=_calculate_coefficient_to_usd(message),
        ),
        CreateCryptoTrade(
            currency=message.purchase_currency.currency,
            k_to_usd=_calculate_coefficient_to_usd(message),
        ),
    ]

    return trades


def _calculate_coefficient_to_usd(message: Message) -> float:
    return random.randint(40_000, 50_000)