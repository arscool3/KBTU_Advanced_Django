from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from schemas import Data
from database import session
import models as db

app = FastAPI()


def get_db():
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/heatmap")
def get_heatmap(coin1: Data, coin2: Data, start_date: str, session: Session = Depends(get_db)):
    c1 = session.query(db.Data).filter(db.Data.name == coin1.name).first()
    c2 = session.query(db.Data).filter(db.Data.name == coin2.name).first()
    return [c1, c2]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)