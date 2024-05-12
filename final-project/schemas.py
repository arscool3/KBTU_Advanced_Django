from datetime import datetime
from pydantic import BaseModel


class UserBasic(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class CreateUser(UserBasic):
    pass


class User(UserBasic):
    id: int
    role_id: int


class RoleBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int


class EventBase(BaseModel):
    title: str
    location: str
    start_time: datetime
    end_time: datetime
    organizer_id: int
    participants_max: int

    class Config:
        from_attributes = True


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    status: str
    participants_current: int


class TicketBase(BaseModel):
    user_id: int
    event_id: int

    class Config:
        from_attributes = True


class PurchaseRequest(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    status: str


class NotificationBase(BaseModel):
    user_id: int
    message: str

    class Config:
        from_attributes = True


class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int
    created_at: datetime
