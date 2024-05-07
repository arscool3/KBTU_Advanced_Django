from typing import List

from pydantic import BaseModel, UUID4

'''
class Order(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    total: Mapped[int] = mapped_column(nullable=False)
    status = Column(ChoiceType(ORDER_STATUSES), default="PENDING")
    customer_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    restaurant_id: Mapped[str] = mapped_column(ForeignKey("restaurants.id"))
    courier_id: Mapped[str] = mapped_column(ForeignKey("couriers.id"), nullable=True)


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    price: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    restaurant_item: Mapped["RestaurantMenuItem"] = relationship("RestaurantMenuItem", back_populates="order_items")
    restaurant_item_id: Mapped[str] = mapped_column(ForeignKey('menu_items.id'))
'''


class OrderItem(BaseModel):
    id: UUID4
    price: int
    quantity: int


class Order(BaseModel):
    id: UUID4
    total: int
    status: str
    customer_id: UUID4
    restaurant_id: UUID4
    courier_id: UUID4 | None
    # items: List[OrderItem]

    class Config:
        from_attributes = True
