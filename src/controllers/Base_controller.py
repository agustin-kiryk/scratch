from flask.views import MethodView
from flask import jsonify, request
from pydantic import BaseModel
from typing import Type, TypeVar, Generic
from src.Api_response import ApiResponse
from src.utils.utilities import to_dict  

T = TypeVar('T', bound=BaseModel)

class BaseController(MethodView, Generic[T]):
    def __init__(self, service, model: Type[T]):
        self.service = service
        self.model = model

    def get(self, entity_id=None):
        if entity_id is None:
            # List all entities
            entities = self.service.get_all()
            return ApiResponse(data=entities, code=200).to_response()
        else:
            # Get a single entity by ID
            entity = self.service.get_by_id(entity_id)
            if entity:
                return ApiResponse(data=entity, code=200).to_response()
            return ApiResponse(message=f'{self.model.__name__} not found', code=404).to_response()

    def post(self):
        # Create a new entity
        data = request.get_json()
        entity = self.model(**data)
        new_entity = self.service.create(entity)
        return ApiResponse(data=new_entity, code=201).to_response()

    def put(self, entity_id):
        # Update an existing entity
        data = request.get_json()
        entity = self.service.update(entity_id, data)
        if entity:
            return ApiResponse(data=entity, code=200).to_response()
        return ApiResponse(message=f'{self.model.__name__} not found', code=404).to_response()

    def delete(self, entity_id):
        # Delete an entity
        result = self.service.delete(entity_id)
        if result:
            return ApiResponse(message=f'{self.model.__name__} deleted', code=200).to_response()
        return ApiResponse(message=f'{self.model.__name__} not found', code=404).to_response()
