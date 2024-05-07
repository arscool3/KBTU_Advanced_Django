from sqlalchemy.orm import Session
from database import engine
from models import Restaurant, RestaurantMenuItem, Order, OrderItem, Customer, Courier


def create_restaurant(session: Session, email: str, phone_number: str, address: str, hashed_password: str) -> Restaurant:
    try:
        restaurant = Restaurant(email=email, phone_number=phone_number, address=address, hashed_password=hashed_password)
        session.add(restaurant)
        session.commit()
        return restaurant
    except Exception as e:
        session.rollback()
        raise e


def read_restaurant(session: Session, restaurant_id: str) -> Restaurant:
    try:
        return session.query(Restaurant).filter_by(id=restaurant_id).first()
    except Exception as e:
        raise e


def update_restaurant(session: Session, restaurant_id: str, **kwargs) -> Restaurant:
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        for key, value in kwargs.items():
            setattr(restaurant, key, value)
        session.commit()
        return restaurant
    except Exception as e:
        session.rollback()
        raise e


def delete_restaurant(session: Session, restaurant_id: str):
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        session.delete(restaurant)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

