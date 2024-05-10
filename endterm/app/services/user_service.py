from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, user: UserCreate):
        db_user = User(username=user.username, email=user.email, hashed_password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
