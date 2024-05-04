from datetime import datetime

import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from category.models import Category
from database import Base
from task_comments.models import TaskComment
from tasks.choices import StatusEnum
from utils.model_constants import default_id


class Task(Base):
    __tablename__ = "task"

    id: Mapped[default_id]
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(sqlalchemy.Enum(StatusEnum), default=StatusEnum.OPEN)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    project_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("project.id"))
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"))
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("category.id"))

    user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    category = relationship(Category, back_populates="tasks")
    comments = relationship(TaskComment, back_populates="task")
