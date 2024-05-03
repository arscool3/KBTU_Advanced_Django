from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str


class CreateUser(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class ChatBase(BaseModel):
    name: str
    owner_id: int


class CreateChat(ChatBase):
    pass


class Chat(ChatBase):
    id: int

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    content: str


class CreateMessage(MessageBase):
    sender_id: int
    chat_id: int
    attachments: Optional[List[int]] = []


class Message(MessageBase):
    id: int
    sender_id: int
    chat_id: int
    attachments: Optional[List[str]] = None
    notifications: Optional["Notification"]

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    name: str

class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int
    message: Message

    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str
    owner_id: int


class CreateGroup(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True


class MembershipBase(BaseModel):
    user_id: int
    group_id: int


class CreateMembership(MembershipBase):
    pass


class Membership(MembershipBase):
    id: int

    class Config:
        from_attributes = True


class AttachmentBase(BaseModel):
    filename: str
    message_id: int


class CreateAttachment(AttachmentBase):
    pass


class Attachment(AttachmentBase):
    id: int

    class Config:
        from_attributes = True

