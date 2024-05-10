from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from database import UserCreate, User, OrderCreate, Order, ProductCreate, Product, CategoryCreate, Category, Seller, SellerCreate
from kafka import KafkaProducer
import json
from dep import get_db

# Create the database tables
Base.metadata.create_all(bind=engine)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

app = FastAPI()

# Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Endpoint to create a new user
@app.post("/users/", response_model=None)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoint to get a user by ID
@app.get("/users/{user_id}", response_model=None)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Endpoint to create a new order
@app.post("/orders/", response_model=None)
async def create_order_and_publish_to_kafka(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Simulate creating order by printing order details
    print("Creating order:", order.dict())

    # Publish event to Kafka topic
    topic = "new_orders"
    message = {"order_id": db_order.id, "user_id": order.user_id, "product_id": order.product_id}
    producer.send(topic, json.dumps(message).encode('utf-8'))
    return "done"

# Endpoint to get an order by ID
@app.get("/orders/{order_id}", response_model=None)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Endpoint to create a new product
@app.post("/products/", response_model=None)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Endpoint to get a product by ID
@app.get("/products/{product_id}", response_model=None)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Endpoint to create a new category
@app.post("/categories/", response_model=None)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Endpoint to get a category by ID
@app.get("/categories/{category_id}", response_model=None)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.post("/sellers/", response_model=None)
def create_seller(seller: SellerCreate, db: Session = Depends(get_db)):
    db_seller = Seller(name=seller.name)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

# Endpoint to get a seller by ID
@app.get("/sellers/{seller_id}", response_model=None)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = db.query(Seller).filter(Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return db_seller