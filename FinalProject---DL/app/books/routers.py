from fastapi import APIRouter
from app.utils.container import get_container
from app.utils.dependencies import GetListDependency, RetrieveDependency, DeleteDependency
from app.books.repository import BookRepo
from app.books.dependencies import BookCreateDependency

router = APIRouter(prefix="/book", tags=["Books"])

router.add_api_route("/get_books", get_container(BookRepo).resolve(GetListDependency), methods=["GET"])

router.add_api_route("/get_book", get_container(BookRepo).resolve(RetrieveDependency), methods=["GET"])

router.add_api_route("/create_book", get_container(BookRepo).resolve(BookCreateDependency), methods=["POST"])

router.add_api_route("/delete_book", get_container(BookRepo).resolve(DeleteDependency), methods=["DELETE"])
