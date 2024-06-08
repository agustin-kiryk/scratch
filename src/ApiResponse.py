import uuid
from datetime import datetime
from flask import g, jsonify

class ApiResponse:
    def __init__(self, data=None, message=None, code=200):
        self.headerStatus = {
            'code': code,
            'description': 'Success' if code == 200 else 'Error'
        }
        self.serverTime = datetime.utcnow().isoformat()
        self.message = message
        self.requestId = g.get('request_id', str(uuid.uuid4()))
        self.data = data

    def to_dict(self):
        return {
            'headerStatus': self.headerStatus,
            'serverTime': self.serverTime,
            'message': self.message,
            'requestId': self.requestId,
            'data': self.data
        }

    def to_response(self):
        return jsonify(self.to_dict()), self.headerStatus['code']
