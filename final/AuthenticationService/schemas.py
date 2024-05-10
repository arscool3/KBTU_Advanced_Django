from pydantic import BaseModel, SecretStr


class CreateCustomerRequest(BaseModel):
    email: str
    phone_number: str
    address: str
    hashed_password: SecretStr


class Token(BaseModel):
    token_type: str
    access_token: str


class CreateCourierRequest(BaseModel):
    email: str
    phone_number: str
    hashed_password: SecretStr


class CreateRestaurantRequest(BaseModel):
    email: str
    phone_number: str
    hashed_password: SecretStr
    name: str
    address: str


class Restaurant(BaseModel):
    id: str
    address: str
    email: str
    status: str

    class Config:
        from_attributes = True


class Food(BaseModel):
    id: str
    name: str
    price: int
    image: str
    description: str
    restaurant_id: str

    class Config:
        from_attributes = True


class CreateOrder(BaseModel):
    customer_id: str
    restaurant_id: str


class OrderDetail(BaseModel):
    id: str
    courier_id: str | None
    restaurant_id: str
    customer_id: str
    status: dict
    total: int


class CreateOrderItem(BaseModel):
    quantity: int
    restaurant_item_id: str


class CreateMenuItem(BaseModel):
    name: str
    price: int
    image: str
    description: str
    restaurant_id: str


class UpdateMenuItem(BaseModel):
    name: str
    price: str
    image: str
    description: str


class MenuItem(BaseModel):
    id: str
    name: str
    price: int
    image: str
    description: str
    restaurant_id: str


class CourierOrderDetail(BaseModel):
    id: str
    courier_id: str | None
    restaurant_id: str
    customer_id: str
    status: str
    total: int
