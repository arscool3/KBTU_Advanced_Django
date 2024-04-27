from fastapi import APIRouter

from database import get_db
from task_comments.dependencies import TaskCommentCreateDependency
from task_comments.repository import TaskCommentRepo
from utils.container import get_container
from utils.dependencies import ListDependency, RetrieveDependency, DeleteDependency

router = APIRouter(prefix="/task_comment", tags=["Task Comments"])


router.add_api_route("/", get_container(TaskCommentRepo).resolve(TaskCommentCreateDependency), methods=["POST"],
                     name="create_task_comment")
router.add_api_route("/", get_container(TaskCommentRepo).resolve(ListDependency), methods=["GET"],
                     name="list_task_comments")
router.add_api_route("/{id}", get_container(TaskCommentRepo).resolve(RetrieveDependency), methods=["GET"],
                     name="retrieve_task_comment")
router.add_api_route("/{id}", get_container(TaskCommentRepo).resolve(DeleteDependency), methods=["DELETE"],
                     name="delete_task_comment")
