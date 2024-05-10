from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm.session import Session
import json
import redis
import threading


from tasks import process_order
from dependencies import get_db, get_redis, KafkaManager, send_order_details
from models import (User, Product, Category,
                    Order, OrderItem, Review)
from schemas import (UserCreate, ProductCreate, CategoryCreate,
                     OrderCreate, OrderItemCreate, ReviewCreate,
                     UserRead, ProductRead, CategoryRead,
                     OrderRead, OrderItemRead, ReviewRead)
from repository import (UserRepository, ProductRepository, CategoryRepository,
                        OrderRepository, OrderItemRepository, ReviewRepository)

app = FastAPI()

consumer = KafkaManager.get_consumer()
consumer.subscribe(['order_topic'])


# USER
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, User)
    return user_repo.create(user)


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, User)
    user = user_repo.read_by_id(item_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db, User)
    user_repo.delete(item_id=user_id)
    return {"detail": "User deleted successfully"}


# PRODUCT
@app.post("/products/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db, Product)
    return product_repo.create(product)


@app.get("/products/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db), cache: redis.Redis = Depends(get_redis)):
    product_repo = ProductRepository(db, Product)
    cached_product = cache.get(f"product:{product_id}")
    if cached_product:
        return json.loads(cached_product)

    product = product_repo.read_by_id(item_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = ProductRead.from_orm(product).dict()
    cache.setex(f"product:{product_id}", 3600, json.dumps(product_data))
    return product_data


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db, Product)
    product_repo.delete(item_id=product_id)
    return {"detail": "Product deleted successfully"}


# CATEGORY
@app.post("/categories/", response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    category_repo = CategoryRepository(db, Category)
    return category_repo.create(category)


@app.get("/categories/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category_repo = CategoryRepository(db, Category)
    category = category_repo.read_by_id(item_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_repo = CategoryRepository(db, Category)
    category_repo.delete(item_id=category_id)
    return {"detail": "Category deleted successfully"}


# ORDER
@app.post("/orders/", response_model=OrderCreate)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_repo = OrderRepository(db, Order)
    created_order = order_repo.create(order)
    send_order_details(created_order)
    process_order.send(created_order.id)

    return created_order


@app.get("/orders/{order_id}", response_model=OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order_repo = OrderRepository(db, Order)
    order = order_repo.read_by_id(item_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_repo = OrderRepository(db, Order)
    order_repo.delete(item_id=order_id)
    return {"detail": "Order deleted successfully"}


# ORDER ITEM
@app.post("/order-items/", response_model=OrderItemCreate)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    order_item_repo = OrderItemRepository(db, OrderItem)
    return order_item_repo.create(order_item)


@app.get("/order-items/{item_id}", response_model=OrderItemRead)
def read_order_item(item_id: int, db: Session = Depends(get_db)):
    order_item_repo = OrderItemRepository(db, OrderItem)
    order_item = order_item_repo.read_by_id(item_id=item_id)
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item


@app.delete("/order-items/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    order_item_repo = OrderItemRepository(db, OrderItem)
    order_item_repo.delete(item_id=item_id)
    return {"detail": "Order item deleted successfully"}


# REVIEW
@app.post("/reviews/", response_model=ReviewCreate)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    review_repo = ReviewRepository(db, Review)
    order_item_repo = OrderItemRepository(db, OrderItem)
    return review_repo.create(review)


@app.get("/reviews/{review_id}", response_model=ReviewRead)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review_repo = ReviewRepository(db, Review)
    review = review_repo.read_by_id(item_id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_repo = ReviewRepository(db, Review)
    review_repo.delete(item_id=review_id)
    return {"detail": "Review deleted successfully"}


def take_order_details():
    while True:
        msg = consumer.poll(5.0)
        if msg is None:
            continue
        print(msg.value())
        order_data = json.dumps(msg.value().decode('utf-8'))
        process_order.send(order_data['id'])


threading.Thread(target=take_order_details, daemon=True).start()
