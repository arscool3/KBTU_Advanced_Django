
from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.publishers.repository import PublisherRepo
from app.publishers.dependencies import PublisherCreateDependency
from fastapi import APIRouter

router = APIRouter(prefix="/publisher", tags=["Publishers"])

router.add_api_route("/get_publishers", get_container(PublisherRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_publisher", get_container(PublisherRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_publisher", get_container(PublisherRepo).resolve(PublisherCreateDependency), methods=["POST"])

router.add_api_route("/delete_publisher", get_container(PublisherRepo).resolve(DeleteDependency), methods=["DELETE"])

