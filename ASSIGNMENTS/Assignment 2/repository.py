from abc import abstractmethod


class AbcRepository:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        raise NotImplementedError
