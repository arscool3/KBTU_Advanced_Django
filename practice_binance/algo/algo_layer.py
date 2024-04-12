
def calculate_avg_price(prices):
    try:
        sum_price = 0
        for price in prices:
            sum_price += (price['Open']+price['High']+price['Low']+price['Close'])/4

        return sum_price/len(prices)
    except Exception as e:
        return f"Failed: {str(e)}"
