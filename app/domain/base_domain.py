from pydantic import BaseModel
from ..repository.base_repository import BaseRepository

class BaseDomain():
    def __init__(self, repository: BaseRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get(self, id: str):
        return self.__repository.get(id)

    def create(self, item_model: BaseModel):
        return self.__repository.create(item_model.dict())
    
    def update(self, item_model: BaseModel):
        return self.__repository.update(item_model.dict())
    
    def delete(self, id: str):
        return self.__repository.delete(id)
    