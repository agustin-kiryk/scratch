import uuid
from datetime import datetime
from flask import g, jsonify
from collections import OrderedDict

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

    def to_response(self):
        response_dict = OrderedDict()
        response_dict['headerStatus'] = self.headerStatus
        response_dict['serverTime'] = self.serverTime
        response_dict['message'] = self.message
        response_dict['requestId'] = self.requestId
        response_dict['data'] = self.data

        return jsonify(response_dict), self.headerStatus['code']
