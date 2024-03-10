from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from . import models
def get_current_user(token: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user