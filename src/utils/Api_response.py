import uuid
from datetime import datetime
from flask import g, jsonify
from collections import OrderedDict
from src.errorHandler.error_codes import handlerCode, codes

class ApiResponse:
    def __init__(self, data=None, code=codes.SUCCESS, message=None):
        self.headerStatus = {
            'code': code.code,
            'description': code.description
        }
        self.serverTime = datetime.utcnow().isoformat()
        self.message = message if message else code.message
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
