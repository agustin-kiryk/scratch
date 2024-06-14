from typing import Type, TypeVar, Generic, Optional, List
from pydantic import BaseModel
from src.repositories.Base_mongo_repository import BaseRepository
from src.utils.utilities import to_dict

T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    def get_all(self) -> List[dict]:
        entities = self.repository.find_all()
        return [to_dict(entity) for entity in entities]

    def get_by_id(self, entity_id: str) -> Optional[dict]:
        entity = self.repository.find_by_id(entity_id)
        return to_dict(entity) if entity else None

    def create(self, entity: T) -> dict:
        self.repository.insert(entity)
        return to_dict(entity)

    def update(self, entity_id: str, data: dict) -> Optional[dict]:
        entity = self.repository.find_by_id(entity_id)
        if entity:
            updated_entity = entity.copy(update=data)
            self.repository.update(updated_entity)
            return to_dict(updated_entity)
        return None

    def delete(self, entity_id: str) -> bool:
        entity = self.repository.find_by_id(entity_id)
        if entity:
            self.repository.delete_by_id(entity_id)
            return True
        return False
