from sqlalchemy import select, update
from cart.models import Cart
from cart import schemas
from email_sender import send_email
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

    def process(self, cart_id: int):
        cart = self.get_by_id(cart_id)
        if not cart:
            return "Cart not found", None

        total_price = 0
        for item in cart.cart_items:
            if item.product:
                total_price += item.product.price * item.amount
        send_email.send(total_price)

        return "Cart processed successfully", total_price