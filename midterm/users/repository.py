from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils.repository import AbcRepository
from utils.schemes import User, CreateComment, CreateLike, CreateComplaint
import utils.models as db


class UserRepository(AbcRepository):
    def __init__(self, session: Session = None):
        self.session = session

    def retrieve(self, user_id: int):
        return self.session.execute(select(db.User).where(db.User.id == user_id)).scalars().first()

    def create(self, user: User) -> str:
        pass

    def delete(self, user_id: int):
        pass

    def list(self) -> List[User]:
        pass

    def leave_comment(self, comment: CreateComment):
        self.session.add(db.Comment(**comment.model_dump()))
        self.session.commit()
        return "comment successfully published"

    def put_like(self, like: CreateLike):
        self.session.add(db.Like(**like.model_dump()))
        self.session.commit()
        return "Like successfully putted"

    def leave_complaint(self, complaint: CreateComplaint):
        self.session.add(db.Complaint(**complaint.model_dump()))
        self.session.commit()
        return "complaint successfully published"
