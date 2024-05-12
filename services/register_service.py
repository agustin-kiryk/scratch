from flask import request, Response, jsonify
from config.mongodb import mongo
import json

from models import dtouser


def register_new_user():
    data = request.get_json()
    user_data = dtouser(
        name=data.get('name', None),
        lastName=data.get('lastName', None),
        document=data.get('document', None),
        email=data.get('email', None),
        points=data.get('points', 0)
    )

    result = mongo.db.users.insert_one({
        'name': user_data.name,
        'lastName': user_data.lastName,
        'document': user_data.document,
        'points': user_data.points,
        'email': user_data.email,
        'status': user_data.status
    })

    if result.inserted_id:
        user_id = str(result.inserted_id)
        user_data = {
            'id': user_id,
            'name': user_data.name,       #
            'lastName': user_data.lastName,
            'document': user_data.document,
            'email': user_data.email,     #
            'points': 10,   #
            'status': 4
        }
        response_data = json.dumps({'user': user_data})
        return Response(response_data, mimetype='application/json')
    else:
        response_data = json.dumps({'error': 'Failed to register user'})
        return Response(response_data, mimetype='application/json')