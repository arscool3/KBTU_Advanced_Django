import matplotlib
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from consumer import consume
from producer import produce
from repository import get_from_db

matplotlib.use('Agg')
app = FastAPI()

def create_growth_graph(currency):
    times = [entry.time for entry in currency]
    prices = [entry.price for entry in currency]

    plt.figure(figsize=(10, 6))
    plt.plot(times, prices, marker='o', linestyle='-')
    plt.title('Currency Growth/Decrease Over Time')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True)
    graph_file = "/tmp/growth_graph.png"
    plt.savefig(graph_file)
    plt.close()
    return FileResponse(graph_file)

@app.get("/currency/run")
def run_server(background_tasks: BackgroundTasks):
    background_tasks.add_task(produce)
    background_tasks.add_task(consume)
    return "Producer and consumer started"

@app.get("/currency/{currency_name}")
async def get_currency_prices(coin_name: str):
    currency = get_from_db(coin_name)
    return create_growth_graph(currency)
