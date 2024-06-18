from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from pydantic import BaseModel
from typing import Type, TypeVar, Generic
from src.utils.Api_response import ApiResponse
from src.errorHandler.error_codes import codes
from src.utils.utilities import to_dict

T = TypeVar('T', bound=BaseModel)


class BaseController(MethodView, Generic[T]):
    def __init__(self, service, model: Type[T]):
        self.service = service
        self.model = model

    @jwt_required()
    def get(self, entity_id=None):
        if entity_id is None:
            params = request.args.to_dict()
            entities = self.service.get_by_params(params)
            return ApiResponse(data=entities, code=codes.SUCCESS).to_response()
        else:
            entity = self.service.get_by_id(entity_id)
            if entity:
                return ApiResponse(data=entity, code=codes.SUCCESS).to_response()
            return ApiResponse(message=f'{self.model.__name__} not found', code=codes.NOT_FOUND).to_response()

    def post(self):
        # Validate role EMPTY
        """
        claims = get_jwt()
        if claims['role'] != 'admin':
           return ApiResponse(message='Admin access required', code=403).to_response()
        """
        # Create a new entity
        data = request.get_json()
        entity = self.model(**data)
        new_entity = self.service.create(entity)
        return ApiResponse(data=new_entity, code=codes.SUCCESS).to_response()

    @jwt_required
    def put(self, entity_id):
        # Validate role
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        if claims['role'] != 'admin' and current_user_id != entity_id:
            return ApiResponse(message='Unauthorized', code=codes.UNAUTHORIZED).to_response()
        # Update an existing entity
        data = request.get_json()
        entity = self.service.update_by_id(entity_id, data)
        if entity:
            return ApiResponse(data=entity, code=codes.SUCCESS).to_response()
        return ApiResponse(message=f'{self.model.__name__} not found', code=codes.NOT_FOUND).to_response()

    @jwt_required
    def delete(self, entity_id):
        # Validate role
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        if claims['role'] != 'admin' and current_user_id != entity_id:
            return ApiResponse(message='Unauthorized', code=codes.UNAUTHORIZED).to_response()
        # Delete an entity
        result = self.service.delete(entity_id)
        if result:
            return ApiResponse(message=f'{self.model.__name__} deleted', code=codes.SUCCESS).to_response()
        return ApiResponse(message=f'{self.model.__name__} not found', code=codes.BAD_REQUEST).to_response()

        """   @jwt_required()
    def post(self):
        claims = get_jwt()
        if claims['role'] != 'admin':
            return ApiResponse(message='Admin access required', code=403).to_response()
        data = request.get_json()
        entity = self.model(**data)
        new_entity = self.service.create(entity)
        return ApiResponse(data=new_entity.to_dict(), code=201).to_response()

    @jwt_required()
    def put(self, entity_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        if claims['role'] != 'admin' and current_user_id != entity_id:
            return ApiResponse(message='Unauthorized', code=403).to_response()
        data = request.get_json()
        entity = self.service.update_by_id(entity_id, data)
        if entity:
            return ApiResponse(data=entity, code=200).to_response()
        return ApiResponse(message=f'{self.model.__name__} not found', code=404).to_response()

        """
