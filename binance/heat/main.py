from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from models import DataToHeatmap
from database import get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/data/{start_date}/{end_date}")
def get_data(start_date: str, end_date: str, db: Session = Depends(get_db)):
    start_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")

    if start_date >= end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")

    data = db.query(DataToHeatmap).filter(
        DataToHeatmap.start_time >= start_date,
        DataToHeatmap.end_time <= end_date
    ).all()

    result = [
        {
            "name": datum.name,
            "end_time": datum.end_time.strftime("%Y-%m-%d"),
            "k_to_usd": datum.k_to_usd
        } for datum in data
    ]

    return result
