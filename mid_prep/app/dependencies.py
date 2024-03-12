from sqlalchemy.orm import Session
import models
import schemas
import database


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_owner(db: Session, owner: schemas.OwnerCreate):
    db_owner = models.Owner(name=owner.name)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def get_car(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def get_owner(db: Session, owner_id: int):
    return db.query(models.Owner).filter(models.Owner.id == owner_id).first()


def create_car(db: Session, car: schemas.CarCreate):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def get_owners(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Owner).offset(skip).limit(limit).all()


def get_cars(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Car).offset(skip).limit(limit).all()


def get_cars_by_owner(db: Session, owner_id: int):
    return db.query(models.Car).filter(models.Car.owner_id == owner_id).all()
