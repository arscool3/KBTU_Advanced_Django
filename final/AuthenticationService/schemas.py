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
