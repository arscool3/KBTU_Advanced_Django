from sqlalchemy import insert

from projects import schemas
from projects.models import Project, project_user_association
from utils.repository import BaseRepository


class ProjectRepo(BaseRepository):
    model = Project
    action_schema = {
        "list": schemas.Project,
        "retrieve": schemas.Project,
        "create": schemas.CreateProjectResponse,
    }

    def add_user_to_project(self, instance: schemas.AddUserToProject) -> str:
        self.session.execute(project_user_association.insert().values(instance.model_dump()))
        self.session.commit()
        return """User added successfully"""

