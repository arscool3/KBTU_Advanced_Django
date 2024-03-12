
from fastapi import FastAPI, Depends, HTTPException
from database import *
from repository import *
from typing import Type
import punq
from typing import List

app = FastAPI()


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

    def __call__(self) -> List[ReturnType]:
        return self.repo.get_all()


class Dependency1(Dependency):
    def __call__(self, id: int) -> ReturnType:
        return self.repo.get_by_id(id)


def get_container(repository: Type[AbcRepository]) -> punq.Container:
    container = punq.Container()
    container.register(AbcRepository, repository, instance=repository(session=session))
    container.register(Dependency)
    container.register(Dependency1)
    return container


app.add_api_route("/items", get_container(ItemRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/sellers", get_container(SellerRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/customers", get_container(CustomerRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/shops", get_container(ShopRepository).resolve(Dependency), methods=["GET"])
app.add_api_route("/order", get_container(OrderRepository).resolve(Dependency), methods=["GET"])

app.add_api_route("/item_by_id", get_container(ItemRepository).resolve(Dependency1), methods=["GET"])
app.add_api_route("/seller_by_id", get_container(SellerRepository).resolve(Dependency1), methods=["GET"])
app.add_api_route("/customer_by_id", get_container(CustomerRepository).resolve(Dependency1), methods=["GET"])
app.add_api_route("/shop_by_id", get_container(ShopRepository).resolve(Dependency1), methods=["GET"])
app.add_api_route("/order_by_id", get_container(OrderRepository).resolve(Dependency1), methods=["GET"])


@app.post('/items')
def add_items(item: CreateItem, session: Session = Depends(get_db)) -> str:
    session.add(db.Item(**item.model_dump()))
    return "Item was added"


@app.post('/seller')
def add_seller(seller: CreateSeller, session: Session = Depends(get_db)) -> str:
    session.add(db.Seller(**seller.model_dump()))
    return "Seller was added"


@app.post('/customer')
def add_customer(customer: CreateCustomer, session: Session = Depends(get_db)) -> str:
    session.add(db.Customer(**customer.model_dump()))
    return "Customer was added"


@app.post('/shop')
def add_shop(shop: CreateShop, session: Session = Depends(get_db)) -> str:
    session.add(db.Shop(**shop.model_dump()))
    return "Shop was added"


@app.post('/order')
def add_shop(order: CreateOrder, session: Session = Depends(get_db)) -> str:
    session.add(db.Order(**order.model_dump()))
    return "Order was added"


