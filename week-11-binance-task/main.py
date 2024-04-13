import os
from datetime import datetime
import matplotlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import numpy as np
from database import insert_to_db, get_from_db
from schemas import Bitcoin

matplotlib.use('Agg')
app = FastAPI()

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


def create_heatmap(bitcoin):
    prices = [entry.price for entry in bitcoin]

    matrix_size = min(len(prices), 10)
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


@app.post("/bitcoin/")
def create_bitcoin_entry(bitcoin: Bitcoin):
    insert_to_db(bitcoin.time, bitcoin.price, bitcoin.coin)
    return {"message": "Bitcoin data added successfully"}


@app.get("/bitcoin/{coin_name}")
def get_bitcoin_prices(coin_name: str):
    bitcoin = get_from_db(coin_name)
    return create_heatmap(bitcoin)