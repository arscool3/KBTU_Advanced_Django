import matplotlib
from fastapi import FastAPI
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import numpy as np

from database import get_from_db

matplotlib.use('Agg')
app = FastAPI()


@app.get("/heatmap")
def show_heat_map():
    data = np.random.rand(10, 10)

    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()

    heatmap_file = "/tmp/heatmap.png"
    plt.savefig(heatmap_file)
    plt.close()
    return FileResponse(heatmap_file)

# data = {
#     "time": ["2021-01-01", "2021-01-02", "2021-01-03"],
#     "correlation_coefficient": [0.8, 0.9, 0.85]
# }


@app.get("/heatmap/{coin1}/{coin2}/{start_date}")
def get_heatmap(coin1: str, coin2: str, start_date: str):
    data_coin1 = get_from_db(coin1)
    data_coin2 = get_from_db(coin2)
    correlation = 0.8
    return {"heatmap_data": correlation}
