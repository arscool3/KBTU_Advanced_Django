from fastapi import FastAPI, HTTPException, Depends
from database.database import SessionLocal
from sqlalchemy.orm import Session

from models import CoffeeShop, CoffeeShopOwner, Coffee

app = FastAPI(title="Midterm Prep")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/coffeeshops/")
def create_coffee_shop(coffee_shop: CoffeeShop, db: Session = Depends(get_db)):
    db.add(coffee_shop)
    db.commit()
    return coffee_shop

@app.get("/coffeeshops/{coffee_shop_id}")
def read_coffee_shop(coffee_shop_id: int, db: Session = Depends(get_db)):
    coffee_shop = db.query(CoffeeShop).filter(CoffeeShop.id == coffee_shop_id).first()
    if coffee_shop is None:
        raise HTTPException(status_code=404, detail="Coffee shop not found")
    return coffee_shop

# Эндпоинты для работы с CoffeeShopOwner
@app.post("/owners/")
def create_owner(owner: CoffeeShopOwner, db: Session = Depends(get_db)):
    db.add(owner)
    db.commit()
    return owner

@app.get("/owners/{owner_id}")
def read_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(CoffeeShopOwner).filter(CoffeeShopOwner.id == owner_id).first()
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner

# Эндпоинты для работы с Coffee
@app.post("/coffees/")
def create_coffee(coffee: Coffee, db: Session = Depends(get_db)):
    db.add(coffee)
    db.commit()
    return coffee

@app.get("/coffees/{coffee_id}")
def read_coffee(coffee_id: int, db: Session = Depends(get_db)):
    coffee = db.query(Coffee).filter(Coffee.id == coffee_id).first()
    if coffee is None:
        raise HTTPException(status_code=404, detail="Coffee not found")
    return coffee