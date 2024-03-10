import sqlalchemy
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base
from notifications.models import Notification
from utils.model_constants import default_id


class User(Base):
    __tablename__ = "user"

    id: Mapped[default_id]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]

    project_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("project.id"))

    tasks = relationship("Task", back_populates="user")
    project = relationship("Project", back_populates="users")
    comments = relationship("TaskComment", back_populates="user")
    notifications = relationship(Notification, back_populates="user")
