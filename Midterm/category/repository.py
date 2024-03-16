from pydantic import BaseModel
from sqlalchemy import delete, select
from category.models import Category
from repository import AbcRepository


class CategoryRepo(AbcRepository):
    model = Category

    def __call__(self):
        return self

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return instance

    def create(self, body: BaseModel):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return instances

    def delete(self, id: int):
        category = self.session.get(self.model, id)
        self.session.delete(category)
        self.session.commit()
        return "Deleted"
