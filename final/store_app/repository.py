from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


class BaseRepository:
    def __init__(self, db_session: Session, model):
        self.db_session = db_session
        self.model = model

    def create(self, data):
        instance = self.model(**data.model_dump())
        self.db_session.add(instance)
        self.db_session.commit()
        self.db_session.refresh(instance)
        return instance

    def read_by_id(self, item_id: int):
        try:
            return self.db_session.query(self.model).filter(self.model.id == item_id).one()
        except NoResultFound:
            return None

    def delete(self, item_id: int):
        instance = self.db_session.query(self.model).filter(self.model.id == item_id).one()
        self.db_session.delete(instance)
        self.db_session.commit()

    def list(self, skip: int = 0, limit: int = 100):
        return self.db_session.query(self.model).offset(skip).limit(limit).all()


class UserRepository(BaseRepository):
    pass


class CategoryRepository(BaseRepository):
    pass


class ProductRepository(BaseRepository):
    pass


class OrderRepository(BaseRepository):
    pass


class OrderItemRepository(BaseRepository):
    pass


class ReviewRepository(BaseRepository):
    pass
