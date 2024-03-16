from sqlalchemy import select

from cart.models import Cart
from cart import schemas
from repository import AbcRepository


class CartRepo(AbcRepository):
    model = Cart

    def __call__(self):
        return self

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return schemas.Cart.model_validate(instance)

    def create(self, body: schemas.CreateCart):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return instances

    def delete(self, id: int):
        instance = self.session.get(self.model, id)
        self.session.delete(instance)
        self.session.commit()
        return "Deleted"
