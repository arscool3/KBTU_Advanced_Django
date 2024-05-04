from pydantic import BaseModel
from sqlalchemy import delete, select

from analys_product.models import AnalysProduct
from category.models import Category
from repository import AbcRepository


class AnalysProductRepo(AbcRepository):
    model = AnalysProduct

    def __call__(self):
        return self

    def get_most_popular_product(self):
        return self.session.query(self.model) \
            .order_by(self.model.count.desc()) \
            .first()

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