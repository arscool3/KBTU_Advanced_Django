from sqlalchemy import select, delete
from product.models import Product
from repository import AbcRepository
from product import schemas


class ProductRepo(AbcRepository):

    model = Product

    def __call__(self):
        return self

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return [schemas.Product.model_validate(instance) for instance in instances]

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return schemas.Product.model_validate(instance)

    def create(self, body: schemas.CreateProduct):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def delete(self, id: int):
        self.session.execute(delete(self.model).where(self.model.id == id))
        self.session.commit()
        return "Deleted"
