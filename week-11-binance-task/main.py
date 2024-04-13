import matplotlib
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import numpy as np
from consumer import consume
from producer import produce
from reposiroty import get_from_db

matplotlib.use('Agg')
app = FastAPI()


def create_heatmap(bitcoin):
    prices = [entry.price for entry in bitcoin]
    matrix_size = min(len(prices), 40)
    data = np.zeros((matrix_size, matrix_size))

    for i in range(matrix_size):
        for j in range(matrix_size):
            data[i, j] = abs(prices[i] - prices[j])

    plt.figure(figsize=(8, 6))
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()
    heatmap_file = "/tmp/heatmap.png"
    plt.savefig(heatmap_file)
    plt.close()
    return FileResponse(heatmap_file)


@app.get("/bitcoin/run")
def run_server(background_tasks: BackgroundTasks):
    background_tasks.add_task(produce)
    background_tasks.add_task(consume)
    return "Producer and consumer started"


@app.get("/bitcoin/{coin_name}")
async def get_bitcoin_prices(coin_name: str):
    bitcoin = get_from_db(coin_name)
    return create_heatmap(bitcoin)


# random number's heatmap
@app.get("/heatmap")
def random_heat_map():
    data = np.random.rand(10, 10)

    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()

    heatmap_file = "/tmp/heatmap.png"
    plt.savefig(heatmap_file)
    plt.close()
    return FileResponse(heatmap_file)
