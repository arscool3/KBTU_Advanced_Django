import punq as punq
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

import models as db
from database import session
from repository import AbcRepository, BookRepository, GenreRepository, PublisherRepository, OrderRepository, OrderItemRepository
from services import create_access_token, get_current_user
from schemas import UserCreate, ReturnType, BookCreate, GenreCreate, PublisherCreate, OrderCreate, OrderItemCreate
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()


class Dependency:
    def __init__(self, repo: AbcRepository):
        self.repo = repo

    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)


def get_container(repository: type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    return container


app.add_api_route("/books", get_container(BookRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/genres", get_container(GenreRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/publishers", get_container(PublisherRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/orders", get_container(OrderRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/order_items", get_container(OrderItemRepository).resolve(Dependency), methods=["GET"])


@app.post("/users")
def add_user(user: UserCreate, session: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    session.add(db.User(username=user.username, password=hashed_password))
    session.commit()
    session.close()
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "greeting": user.username}


@app.post("/login")
def login(user_credentials: UserCreate, session: Session = Depends(get_db)):
    db_user = session.query(db.User).filter(db.User.username == user_credentials.username).first()

    if db_user is None or not pwd_context.verify(user_credentials.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": db_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.username
    }


@app.get("/me")
def get_user(user: UserCreate = Depends(get_current_user)):
    return user


@app.post('/books')
def add_book(book: BookCreate, session: Session = Depends(get_db)) -> str:
    session.add(db.Book(**book.model_dump()))
    return book.title


@app.post('/genres')
def add_genre(genre: GenreCreate, session: Session = Depends(get_db)) -> str:
    session.add(db.Genre(**genre.model_dump()))
    return genre.name


@app.post('/publishers')
def add_publisher(publisher: PublisherCreate, session: Session = Depends(get_db)) -> str:
    session.add(db.Publisher(**publisher.model_dump()))
    return publisher.name


@app.post('/orders')
def add_order(order: OrderCreate, session: Session = Depends(get_db)) -> str:
    session.add(db.Order(**order.model_dump()))
    return "Order was created"


@app.post('/order_items')
def add_order_item(order_item: OrderItemCreate, session: Session = Depends(get_db)) -> str:
    session.add(db.OrderItem(**order_item.model_dump()))
    return "OrderItem was created"

