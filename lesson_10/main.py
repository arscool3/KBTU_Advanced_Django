import time
from fastapi import HTTPException, Depends
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, WebSocket
from sqlalchemy.orm import Session
from database import session
from producer import produce
from consumer import consume
from services import *

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


@app.websocket('/data')
async def stock_market(web_socket: WebSocket):
    await web_socket.accept()
    try:
        while True:
            price = random.randint(660, 670)
            if price == 666:
                raise Exception('devil here')
            stock_unit = random.choice(stock_units)
            await web_socket.send_json({'stock': stock_unit, 'price': price})
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Error {e}")
    finally:
        await web_socket.close()

@app.get("/bitcoin/run")
def run_server(background_tasks: BackgroundTasks):
    background_tasks.add_task(produce)
    # background_tasks.add_task(consume)
    return "Producer and consumer started"


@app.get("/heatmap/")
def get_heatmap(coin1: str, coin2: str, start_date: str, db: Session = Depends(get_db)):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')

    latest_date_coin1 = get_latest_date_for_symbol(db, coin1) or datetime.now()
    latest_date_coin2 = get_latest_date_for_symbol(db, coin2) or datetime.now()

    end_datetime = min(latest_date_coin1, latest_date_coin2)

    prices_coin1 = get_prices_from_db(db, coin1, start_datetime, end_datetime)
    prices_coin2 = get_prices_from_db(db, coin2, start_datetime, end_datetime)

    if not prices_coin1 or not prices_coin2:
        raise HTTPException(status_code=404, detail="No price data found for the specified symbols or date range.")

    prices_coin1 = [price[0] for price in prices_coin1]
    prices_coin2 = [price[0] for price in prices_coin2]

    correlation = calculate_correlation(prices_coin1, prices_coin2)

    return {"correlation": correlation}