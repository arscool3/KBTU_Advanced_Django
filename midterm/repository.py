from abc import abstractmethod
from sqlalchemy.orm import Session

import models as db
from schemas import User, Course, Video, Review, Purchase, Progress


class AbcRepository:
    @abstractmethod
    def __init__(self, session: Session):
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> User | Course | Video | Review | Purchase | Progress:
        raise NotImplementedError

class UserRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> User:
        db_user = self._session.get(db.User, id)
        if db_user is None:
            return "No such user!"
        return User.model_validate(db_user)

class CourseRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Course:
        db_course = self._session.get(db.Course, id)
        if db_course is None:
            return "No such course!"
        return Course.model_validate(db_course)

class VideoRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Video:
        db_video = self._session.get(db.Video, id)
        if db_video is None:
            return "No such video!"
        return Video.model_validate(db_video)

class ReviewRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Review:
        db_review = self._session.get(db.Review, id)
        if db_review is None:
            return "No such review!"
        return Review.model_validate(db_review)

class PurchaseRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Purchase:
        db_purchase = self._session.get(db.Purchase, id)
        if db_purchase is None:
            return "No such purchase!"
        return Purchase.model_validate(db_purchase)

class ProgressRepository(AbcRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Progress:
        db_progress = self._session.get(db.Progress, id)
        if db_progress is None:
            return "No such progress record!"
        return Progress.model_validate(db_progress)