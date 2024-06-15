from bson.objectid import ObjectId
from pymongo.collection import Collection
from pydantic import BaseModel
from typing import Dict, List, Type, TypeVar, Generic, Optional
from src.config.mongodb import mongo

T = TypeVar('T', bound=BaseModel)

def get_collection_name(model_class: Type[BaseModel]) -> str:
    return model_class.__name__.lower() + 's' 

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
        collection_name = get_collection_name(model)
        self.collection = mongo.db[collection_name]

    def find_by_id(self, id: str) -> Optional[T]:
        data = self.collection.find_one({'_id': ObjectId(id)})
        return self.model.from_mongo_dict(data) if data else None
    

    def find_by_email(self, email: str) -> Optional[T]:
        data = self.collection.find_one({'email': email})
        return self.model.from_mongo_dict(data) if data else None

    def insert(self, document: T) -> str:
        mongo_dict = document.to_mongo_dict()
        # Remove `id` if it's None or empty to let MongoDB generate `_id`
        if '_id' in mongo_dict and not mongo_dict['_id']:
            del mongo_dict['_id']
        result = self.collection.insert_one(mongo_dict)
        return str(result.inserted_id)

    def update(self, document: T) -> None:
        update_data = document.to_mongo_dict(include_all_fields=False)
        # Ensure _id is not included in the update data
        update_data.pop('_id', None)
        self.collection.update_one({'_id': ObjectId(document.id)}, {'$set': update_data})
        
        
    def update_by_id(self, id: str, update_data: dict) -> None:
        # Ensure _id is not included in the update data
        update_data.pop('_id', None)
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': update_data})

    def delete_by_email(self, email: str) -> None:
        self.collection.delete_one({'email': email})
        
    def delete_by_id(self, id: str) -> None:
        self.collection.delete_one({'_id': ObjectId(id)})
        
    def find_all(self) -> list[T]:
       return [self.model.from_mongo_dict(doc) for doc in self.collection.find()]
   
    def find_by_params(self, params: Dict[str, str]) -> List[T]:
        query = {k: int(v) if v.isdigit() else v for k, v in params.items()}  # Convertir valores numéricos a int
        data = self.collection.find(query)
        return [self.model.from_mongo_dict(doc) for doc in data]
    
    def find_by_params(self, params: Dict[str, str]) -> List[T]:
        query = {}
        for k, v in params.items():
            # Handle boolean values
            if v.lower() == 'true':
                v = True
            elif v.lower() == 'false':
                v = False
            elif v.isdigit():
                v = int(v)
            
            # Handle operators
            if '__' in k:
                field, operator = k.split('__')
                if operator == 'gt':
                    query[field] = {'$gt': v}
                elif operator == 'lt':
                    query[field] = {'$lt': v}
                elif operator == 'gte':
                    query[field] = {'$gte': v}
                elif operator == 'lte':
                    query[field] = {'$lte': v}
                elif operator == 'ne':
                    query[field] = {'$ne': v}
            else:
                query[k] = v
            # TODO counts operators
        data = self.collection.find(query)
        return [self.model.from_mongo_dict(doc) for doc in data]