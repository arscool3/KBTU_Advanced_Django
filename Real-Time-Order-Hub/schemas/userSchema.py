from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone_number: str
    address: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int


class CreateUser(BaseModel):
    pass


class UserChatIDBase(BaseModel):
    username: str
    chat_id: int

    class Config:
        from_attributes = True


class UserChatID(UserChatIDBase):
    id: int


class CreateUserChatID(BaseModel):
    pass
