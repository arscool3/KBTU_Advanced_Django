from pydantic import BaseModel
from sqlalchemy import select, delete

from cart_item import schemas
from cart_item.models import CartItem
from repository import AbcRepository


class CartItemRepo(AbcRepository):
    model = CartItem

    def __call__(self):
        return self

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return schemas.CartItem.model_validate(instance)

    def create(self, body: schemas.CreateCartItem):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return instances

    def delete(self, id: int):
        self.session.execute(delete(self.model).where(self.model.id == id))
        self.session.commit()
        return "Deleted"
