import jwt
import hashlib
from fastapi import HTTPException
from settings import JWT_SECRET
from database import session
from database.models import Person


def get_user_from_token(token) -> Person:
    try:
        user_id = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])["user_id"]
        user = session.query(Person).filter_by(id=user_id).first()
        if user:
            return user
        raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")


def get_token(user_id) -> str:
    return jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm="HS256")


def login_user(login: str, password: str) -> str:
    password = hashlib.sha256(password.encode("UTF-8")).hexdigest()
    user = session.query(Person).filter_by(login=login, password=password).first()

    if user:
        return get_token(user.id)
    raise HTTPException(status_code=400, detail="Invalid login or password")


def register_user(login: str, password: str) -> str:
    user = session.query(Person).filter_by(login=login).first()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    password = hashlib.sha256(password.encode("UTF-8")).hexdigest()
    user = Person(login=login, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return get_token(user.id)
