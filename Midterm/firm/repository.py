from sqlalchemy import select, delete

from firm import schemas
from firm.models import Firm
from repository import AbcRepository


class FirmRepo(AbcRepository):
    model = Firm

    def __call__(self):
        return self

    def get_by_id(self, id: int):
        instance = self.session.get(self.model, id)
        return schemas.Firm.model_validate(instance)

    def create(self, body: schemas.CreateFirm):
        self.session.add(self.model(**body.model_dump()))
        self.session.commit()
        return body

    def get_all(self):
        instances = self.session.execute(select(self.model)).scalars().all()
        return instances

    def delete(self, id: int):
        instance = self.session.get(self.model, id)
        self.session.delete(instance)
        self.session.commit()
        return "Deleted"
