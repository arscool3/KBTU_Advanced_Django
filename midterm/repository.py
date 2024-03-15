# human_repository.py

from sqlalchemy.orm import Session
from typing import List
import models as md
import schemas as sc

class HumanRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_humans(self, skip: int = 0, limit: int = 100) -> List[md.Human]:
        return self.db.query(md.Human).offset(skip).limit(limit).all()

    def create_human(self, human_create: sc.HumanSchema) -> md.Human:
        db_human = md.Human(**human_create.dict())
        self.db.add(db_human)
        self.db.commit()
        self.db.refresh(db_human)
        return db_human

    def get_human(self, human_id: int) -> md.Human:
        return self.db.query(md.Human).filter(md.Human.id == human_id).first()
