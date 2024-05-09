from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from database import Base, engine
from database import Category, Coworking, User, Booking, Order, Payment
from kafka import KafkaProducer
from pydantic import BaseModel
from typing import List
import json
from database import PaymentType
from dependencies import get_db
from datetime import datetime

class OrderCreate(BaseModel):
    user_id: int
    items: List[str] 
    total_amount: float
    status: str  

class PaymentCreate(BaseModel):
    user_id: int
    amount: float
    payment_type: str
    status: str 

class CoworkingCreate(BaseModel):
    name: str
    address: str
    category_id: int

class BookingCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    coworking_id: int
    user_id: int

class UserCreate(BaseModel):
    name: str
    email: str

class CreateCategory(BaseModel):
    name: str

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Create session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.post("/categories/")
def create_category(category: CreateCategory, db: Session = Depends(get_db)):
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}

# Endpoint to create a new coworking
@app.post("/coworkings/")
def create_coworking(coworking: CoworkingCreate, db: Session = Depends(get_db)):
    new_coworking = Coworking(**coworking.dict())
    db.add(new_coworking)
    db.commit()
    db.refresh(new_coworking)
    return new_coworking

@app.delete("/coworkings/{coworking_id}")
def delete_coworking(coworking_id: int, db: Session = Depends(get_db)):
    coworking = db.query(Coworking).filter(Coworking.id == coworking_id).first()
    if not coworking:
        raise HTTPException(status_code=404, detail="Coworking not found")
    db.delete(coworking)
    db.commit()
    return {"message": "Coworking deleted successfully"}


# Example endpoint to place a food order
@app.post("/orders/")
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()

    # Publish order event to Kafka
    order_event = {
        "order_id": new_order.id,
        "user_id": new_order.user_id,
        "items": new_order.items,
        "total_amount": new_order.total_amount,
        "status": new_order.status
    }
    producer.send('order_events', value=json.dumps(order_event).encode('utf-8'))

    db.refresh(new_order)
    return new_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

# Example endpoint to process payment
@app.post("/payments/")
def process_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    from models import Payment
    new_payment = Payment(user_id=payment.user_id, amount=payment.amount, status=payment.status, payment_type=PaymentType[payment.payment_type])
    db.add(new_payment)
    db.commit()

    # Publish payment event to Kafka
    payment_event = {
        "payment_id": new_payment.id,
        "user_id": new_payment.user_id,
        "amount": new_payment.amount,
        "status": new_payment.status,
        "payment_type": new_payment.payment_type.value  # Include payment_type in the event
    }
    producer.send('payment_events', value=json.dumps(payment_event).encode('utf-8'))

    db.refresh(new_payment)
    return new_payment

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}


@app.post("/bookings/", response_model=None)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    new_booking = Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}


@app.get("/users/", response_model=None)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.get("/categories/", response_model=None)
def get_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Category).offset(skip).limit(limit).all()

@app.get("/coworkings/", response_model=None)
def get_coworkings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Coworking).offset(skip).limit(limit).all()

@app.get("/bookings/", response_model=None)
def get_bookings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Booking).offset(skip).limit(limit).all()

@app.get("/orders/", response_model=None)
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Order).offset(skip).limit(limit).all()

@app.get("/payments/", response_model=None)
def get_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Payment).offset(skip).limit(limit).all()