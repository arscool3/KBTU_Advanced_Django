import sqlalchemy
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base
from notifications.models import Notification
from projects.models import project_user_association
from utils.model_constants import default_id


class User(Base):
    __tablename__ = "user"

    id: Mapped[default_id]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]

    tasks = relationship("Task", back_populates="user")
    projects = relationship("Project", secondary=project_user_association, back_populates="users")
    comments = relationship("TaskComment", back_populates="user")
    notifications = relationship(Notification, back_populates="user")
