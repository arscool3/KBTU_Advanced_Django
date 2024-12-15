from app.books.schemas import BookResponse
from app.utils.config_schema import ConfigSchema


class BaseAuthor(ConfigSchema):
    name: str
    bio: str


class Author(BaseAuthor):
    id: int
    books: list[BookResponse]


class CreateAuthor(BaseAuthor):
    pass


class AuthorResponse(BaseAuthor):
    id: int