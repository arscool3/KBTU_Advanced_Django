from projects import schemas
from projects.models import Project
from utils.repository import BaseRepository


class ProjectRepo(BaseRepository):
    model = Project
    action_schema = {
        "list": schemas.Project,
        "retrieve": schemas.Project,
        "create": schemas.CreateProjectResponse,
    }

    def add_user_to_project(self, user_project_association: schemas.):

