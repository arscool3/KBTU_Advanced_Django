from sqlalchemy.orm import Session

from utils.repository import AbcRepository
from utils.schemes import Admin


class AdminRepository(AbcRepository):

    def __init__(self, session: Session = None):
        self.session = session

    def create(self, admin: Admin):
        pass

    def list(self):
        pass

    def retrieve(self, id: int):
        pass

    def delete(self, id: int):
        pass