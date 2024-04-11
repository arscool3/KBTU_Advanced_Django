from schemas import CreateCryptoTrade, Message


def process_binance_msg(message: Message) -> CreateCryptoTrade:
    trade = CreateCryptoTrade(
        sold_currency=message.sold_currency.currency,
        purchase_currency=message.purchase_currency.currency,
        k_to_usd=_calculate_coefficient_to_usd(message),
    )

    return trade


def _calculate_coefficient_to_usd(message: Message) -> float:
    return message.purchase_currency.amount / message.sold_currency.amount
