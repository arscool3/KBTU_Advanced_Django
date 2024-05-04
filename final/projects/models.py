from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from tasks.models import Task
from utils.model_constants import default_id


project_user_association = Table(
    "project_user_association",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id")),
    Column("user_id", Integer, ForeignKey("user.id"))
)


class Project(Base):
    __tablename__ = "project"

    id: Mapped[default_id]
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

    users = relationship("User", secondary=project_user_association, back_populates="projects")
    tasks = relationship(Task, back_populates="project")
