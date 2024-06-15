
from flask import jsonify, g, Response
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

class JSONErrorHandler:
    @staticmethod
    def handle_exception(e):
        response = {
            'error': str(e),
            'type': e.__class__.__name__,
            'request_id': g.get('request_id', None)
        }
        return jsonify(response), 500

    @staticmethod
    def handle_validation_error(e):
        response = {
            'error': 'Validation Error',
            'detail': e.errors(),
            'type': 'ValidationError',
            'request_id': g.get('request_id', None)
        }
        return jsonify(response), 400
