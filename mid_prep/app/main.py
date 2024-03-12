from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import dependencies
import schemas
import models
from database import engine, Base

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.post("/owners/", response_model=schemas.Owner)
def create_owner(owner: schemas.OwnerCreate, db: Session = Depends(dependencies.get_db)):
    return dependencies.create_owner(db=db, owner=owner)


@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(dependencies.get_db)):
    return dependencies.get_car(db=db, car_id=car_id)


@app.get("/owners/{owner_id}", response_model=schemas.Owner)
def read_owner(owner_id: int, db: Session = Depends(dependencies.get_db)):
    return dependencies.get_owner(db=db, owner_id=owner_id)


@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(dependencies.get_db)):
    return dependencies.create_car(db=db, car=car)


@app.get("/owners/", response_model=list[schemas.Owner])
def read_owners(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    return dependencies.get_owners(db, skip=skip, limit=limit)


@app.get("/cars/", response_model=list[schemas.Car])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    return dependencies.get_cars(db, skip=skip, limit=limit)


@app.get("/owners/{owner_id}/cars", response_model=list[schemas.Car])
def read_cars_by_owner(owner_id: int, db: Session = Depends(dependencies.get_db)):
    return dependencies.get_cars_by_owner(db, owner_id=owner_id)
