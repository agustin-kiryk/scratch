from flask import request, Response, jsonify
from config.mongodb import mongo
import json

def register_new_user():
    data = request.get_json()
    name = data.get('name', None)
    lastName = data.get('lastName', None)
    document = data.get('document', None)
    email = data.get('email', None)
    points = data.get('points', 0)
    
    result = mongo.db.users.insert_one({
        'name': name,
        'lastName': lastName,
        'document': document,
        'points': points,
        'email': email,
        'status': 1
    })
    
    if result.inserted_id:
        user_id = str(result.inserted_id)
        user_data = {
            'id': user_id,
            'name': name,
            'lastName': lastName,
            'document': document,
            'email': email,
            'points': points,
            'status': 1
        }
        response_data = json.dumps({'user': user_data})
        return Response(response_data, mimetype='application/json')
    else:
        response_data = json.dumps({'error': 'Failed to register user'})
        return Response(response_data, mimetype='application/json')