from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import models, schemas

from app.background.workers import send_email

app = FastAPI()

@app.post("/send-email/")
async def trigger_send_email(email: str, message: str):
    send_email.send(email, message)
    return {"message": "Email will be sent in the background"}

##############################################

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=models.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=models.User)
def update_user(user_id: int, user: models.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user.dict().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=models.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

##############################################

@app.post("/products/", response_model=models.Product)
def create_product(product: models.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=models.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=models.Product)
def update_product(product_id: int, product: models.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for attr, value in product.dict().items():
        setattr(db_product, attr, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=models.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product

##############################################

@app.post("/orders/", response_model=models.Order)
def create_order(order: models.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=models.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=models.Order)
def update_order(order_id: int, order: models.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    for attr, value in order.dict().items():
        setattr(db_order, attr, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}", response_model=models.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return db_order

##############################################

@app.post("/categories/", response_model=models.Category)
def create_category(category: models.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/{category_id}", response_model=models.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categories/{category_id}", response_model=models.Category)
def update_category(category_id: int, category: models.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for attr, value in category.dict().items():
        setattr(db_category, attr, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}", response_model=models.Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category

##############################################

@app.post("/addresses/", response_model=models.Address)
def create_address(address: models.AddressCreate, db: Session = Depends(get_db)):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/addresses/{address_id}", response_model=models.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.put("/addresses/{address_id}", response_model=models.Address)
def update_address(address_id: int, address: models.AddressUpdate, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    for attr, value in address.dict().items():
        setattr(db_address, attr, value)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.delete("/addresses/{address_id}", response_model=models.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address

##############################################

@app.post("/payments/", response_model=models.Payment)
def create_payment(payment: models.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments/{payment_id}", response_model=models.Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.put("/payments/{payment_id}", response_model=models.Payment)
def update_payment(payment_id: int, payment: models.PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    for attr, value in payment.dict().items():
        setattr(db_payment, attr, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.delete("/payments/{payment_id}", response_model=models.Payment)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()