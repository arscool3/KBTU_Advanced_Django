from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, User, Product, Order, Category, Review
from typing import List, Optional
import time
from kafka import KafkaProducer, KafkaConsumer
import json
from pydantic import BaseModel
import dramatiq

app = FastAPI()

KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'
KAFKA_TOPIC_LOGS = 'logs'
KAFKA_TOPIC_USER_ACTIONS = 'user_actions'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class OrderCreate(BaseModel):
    user_id: int
    products: List[int]
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class CategoryCreate(BaseModel):
    name: str

class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None

def calculate_total_price(order_data: OrderCreate, products: List[Product]):
    total_price = sum(product.price for product in products)
    return total_price

def validate_user_input(order_data: OrderCreate):
    # Logic to validate user input
    pass

# Class to handle email sending
class EmailSender:
    def __init__(self):
        # Initialize email sender
        pass
    
    def send_email(self, email: str, subject: str, message: str):
        # Logic to send email
        print(f"Sending email to {email} with subject '{subject}' and message '{message}'")

@dramatiq.actor
def send_confirmation_email(order_id: int, email: str, email_sender: EmailSender):
    time.sleep(5) 
    email_sender.send_email(email=email, subject="Order Confirmation", message=f"Your order with ID {order_id} has been confirmed.")

@dramatiq.actor
def process_payment(order_id: int):
    time.sleep(10)  
    print(f"Payment processed for order {order_id}")

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

consumer = KafkaConsumer(KAFKA_TOPIC_LOGS,
                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group')

def log_user_action(action: str, user_id: int):
    log_data = {'action': action, 'user_id': user_id}
    producer.send(KAFKA_TOPIC_USER_ACTIONS, value=log_data)

def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.post("/orders/")
def create_order(
    background_tasks: BackgroundTasks,
    order_data: OrderCreate,
    products: List[Product] = Depends(get_products),
    db: Session = Depends(get_db),
    email_sender: EmailSender = Depends()
):

    validate_user_input(order_data)

    total_price = calculate_total_price(order_data, products)

    db_order = Order(**order_data.dict(), total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    background_tasks.add_task(send_confirmation_email, db_order.id, order_data.email, email_sender)
    background_tasks.add_task(process_payment, db_order.id)

    log_user_action('order_created', order_data.user_id)
    
    return db_order

@app.get("/users/", response_model=None)
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.post("/users/", response_model=None)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    log_user_action('user_created', db_user.id)
    
    return db_user

@app.get("/users/{user_id}", response_model=None)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=None)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.get("/products/", response_model=None)
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@app.post("/products/", response_model=Product)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=None)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=None)
def update_product(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_data.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.on_event("startup")
def start_kafka_consumer():
    def consume():
        for message in consumer:
            log_data = json.loads(message.value.decode('utf-8'))
            print("Received log:", log_data)
    import threading
    threading.Thread(target=consume).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
