from pydantic import BaseModel
from sqlalchemy import select, delete
from user import schemas
from user.models import User
from repository import AbcRepository


class UserRepo(AbcRepository):
    model = User

    def __call__(self):
        return self

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return schemas.User.model_validate(instance)

    def create(self, body: BaseModel):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return [schemas.User.model_validate(instance) for instance in instances]

    def delete(self, id: int):
        self.session.execute(delete(self.model).where(self.model.id == id))
        self.session.commit()
        return "Deleted"
