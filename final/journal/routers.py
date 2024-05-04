from fastapi import APIRouter, Depends

from journal.repository import JournalRepo
from utils.container import get_container
from utils.dependencies import ListDependency

router = APIRouter(prefix="/journal", tags=["Journal"])

router.add_api_route(
    "/", get_container(JournalRepo).resolve(ListDependency),
    methods=["GET"], name="list_access_logs",
)
