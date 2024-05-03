from abc import abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

import database as db
from schemas import User, Chat, Attachment, Message, Membership, Group, Notification


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        self._session = session

    @abstractmethod
    def get_by_id(self, obj_id):
        raise NotImplementedError()


class UserRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, obj_id: int) -> User:
        db_user = self._session.get(db.User, obj_id)
        return User.model_validate(db_user)


class ChatRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, chat_id: int) -> Chat:
        db_chat = self._session.get(db.Chat, chat_id)
        return Chat.model_validate(db_chat)


class MessageRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, message_id: int) -> Message:
        db_message = self._session.get(db.Message, message_id)
        return Message.model_validate(db_message)

    def get_messages_for_user(self, user_id: int) -> List[Message]:
        db_messages = self._session.query(db.Message).filter(db.Message.sender_id == user_id).all()
        return [Message.model_validate(message) for message in db_messages]

    def get_all(self) -> List[Message]:
        db_messages = self._session.query(db.Message).all()
        return [Message.from_orm(message) for message in db_messages]


class GroupRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, group_id: int) -> Group:
        db_group = self._session.get(db.Group, group_id)
        return Group.model_validate(db_group)


class MembershipRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, membership_id: int) -> Membership:
        db_membership = self._session.get(db.Membership, membership_id)
        return Membership.model_validate(db_membership)


class AttachmentRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, attachment_id: int) -> Attachment:
        db_attachment = self._session.get(db.Attachment, attachment_id)
        return Attachment.model_validate(db_attachment)


class NotificationRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, not_id: int) -> Notification:
        db_not = self._session.get(db.Notification, not_id)
        return Notification.model_validate(db_not)
