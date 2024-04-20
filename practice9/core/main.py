from fastapi import FastAPI
import database as db
from sqlalchemy import select, insert
from schemas import HeatMap
from models import HeatMapData 
app = FastAPI()


def create_correlation(data):
    pass


@app.get("/get_all_data")
def get_data():
    db_data = db.session.execute(select(HeatMapData)
                              ).scalars().all()
    data_list = []

    for data in db_data:
        data_list.append(HeatMap.model_validate(data))
    return data_list


@app.get("/get_correlation")
def get_correlation():
    db_data = db.session.execute(select(HeatMapData)
                              ).scalars().all()
    return create_correlation(db_data)