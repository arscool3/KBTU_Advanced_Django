from database import session, HeatMapData
from sqlalchemy import select
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw
import io
import plotly.graph_objects as go
import numpy as np

from pydantic import BaseModel

from fastapi import FastAPI, Response

# 127.0.0.1:80
app = FastAPI()


class HeatMap(BaseModel):
    timestamp: datetime
    data: dict

    class Config:
        from_attributes = True


def generate_heatmap(data):
    timestamps = []
    values = []
    for item in data:
        timestamps.append(item["timestamp"])
        values.append(list(item["data"].values()))

    # Create a NumPy array from the values
    heatmap_array = np.array(values)

    # Create a heatmap plotly figure
    fig = go.Figure(data=go.Heatmap(z=heatmap_array, x=list(data[0]["data"].keys()), y=timestamps))
    fig.update_layout(title="Currency Exchange Heatmap", xaxis_title="Currency Pair", yaxis_title="Timestamp")

    # Convert the plotly figure to a div string
    div_string = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return div_string


@app.get("/data/get-all/", tags=["main"])
def get_all_data():
    db_data = session.execute(select(HeatMapData)).scalars()
    return [HeatMap.model_validate(a) for a in db_data]


@app.get("/data/heatmap/", tags=["main"])
def get_heatmap_of_all():
    db_data = session.execute(select(HeatMapData)).scalars()

    data = [HeatMap.model_validate(a).model_dump() for a in db_data]

    return Response(content=generate_heatmap(data), media_type="text/html")
