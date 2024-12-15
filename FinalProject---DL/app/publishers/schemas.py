from app.books.schemas import BookResponse
from app.utils.config_schema import ConfigSchema


class BasePublisher(ConfigSchema):
    name: str
    address: str
    contact: str


class Publisher(BasePublisher):
    id: int
    books: list[BookResponse]


class CreatePublisher(BasePublisher):
    pass

