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
