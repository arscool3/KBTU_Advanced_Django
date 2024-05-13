from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import database, schemas

from app.background.workers import send_email

from dotenv import dotenv_values

vals = dotenv_values('data.env')

app = FastAPI()

@app.post("/send-email/")
async def trigger_send_email(username: str, recipient: str, text: str):
    send_email.send(username, vals['password'], recipient, text)
    return {"message": "Email will be sent in the background"}

##############################################

@app.post("/users/", response_model=None)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = database.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=None)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(database.User).filter(database.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=None)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(database.User).filter(database.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user.dict().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=None)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(database.User).filter(database.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

##############################################

@app.post("/products/", response_model=None)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = database.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=None)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(database.Product).filter(database.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=None)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(database.Product).filter(database.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for attr, value in product.dict().items():
        setattr(db_product, attr, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=None)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database.Product).filter(database.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product

##############################################

@app.post("/orders/", response_model=None)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = database.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=None)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=None)
def update_order(order_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for attr, value in order.dict().items():
        setattr(db_order, attr, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}", response_model=None)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order

##############################################

@app.post("/categories/", response_model=None)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = database.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/{category_id}", response_model=None)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(database.Category).filter(database.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categories/{category_id}", response_model=None)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(database.Category).filter(database.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for attr, value in category.dict().items():
        setattr(db_category, attr, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}", response_model=None)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(database.Category).filter(database.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category

##############################################

@app.post("/addresses/", response_model=None)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    db_address = database.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/{address_id}", response_model=None)
def read_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(database.Address).filter(database.Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.put("/addresses/{address_id}", response_model=None)
def update_address(address_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)):
    db_address = db.query(database.Address).filter(database.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for attr, value in address.dict().items():
        setattr(db_address, attr, value)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.delete("/addresses/{address_id}", response_model=None)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(database.Address).filter(database.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address

##############################################

@app.post("/payments/", response_model=None)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = database.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments/{payment_id}", response_model=None)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(database.Payment).filter(database.Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.put("/payments/{payment_id}", response_model=None)
def update_payment(payment_id: int, payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = db.query(database.Payment).filter(database.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    for attr, value in payment.dict().items():
        setattr(db_payment, attr, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.delete("/payments/{payment_id}", response_model=None)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(database.Payment).filter(database.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()